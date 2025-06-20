from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
import os

# ----------------- App Setup -------------------
app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tour_recommendation'
mysql = MySQL(app)

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Gemini API Key not found!")

genai.configure(api_key=api_key)
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config
    )
except Exception as e:
    print(f"Failed to load Gemini model: {str(e)}")

# ----------------- Data & Similarity -------------------
df = pd.read_csv('updated_tour_with_hotels.csv')
destinations_list = df['destination'].drop_duplicates().tolist()

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined_features'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
indices = pd.Series(df.index, index=df['destination']).drop_duplicates()

def load_ratings():
    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id, destination, rating FROM ratings")
    data = cur.fetchall()
    cur.close()
    return pd.DataFrame(data, columns=['user_id', 'destination', 'rating'])

# ----------------- Collaborative Filtering -------------------
def user_user_cf(user_id):
    ratings_df = load_ratings()
    user_item = ratings_df.pivot_table(index='user_id', columns='destination', values='rating').fillna(0)
    if user_id not in user_item.index:
        return pd.Series(dtype='float64')
    sim = cosine_similarity(user_item)
    sim_df = pd.DataFrame(sim, index=user_item.index, columns=user_item.index)
    similar_users = sim_df[user_id].sort_values(ascending=False)[1:]
    similar_users = similar_users.reindex(user_item.index).fillna(0)
    weighted = user_item.T.dot(similar_users.values) / (similar_users.sum() + 1e-9)
    rated = user_item.loc[user_id][user_item.loc[user_id] > 0].index
    return weighted.drop(rated, errors='ignore')

def item_item_cf(user_id):
    ratings_df = load_ratings()
    user_item = ratings_df.pivot_table(index='user_id', columns='destination', values='rating').fillna(0)
    if user_id not in user_item.index:
        return pd.Series(dtype='float64')
    item_sim = cosine_similarity(user_item.T)
    item_sim_df = pd.DataFrame(item_sim, index=user_item.columns, columns=user_item.columns)
    user_ratings = user_item.loc[user_id]
    scores = item_sim_df.dot(user_ratings).div(item_sim_df.sum(axis=1))
    rated = user_ratings[user_ratings > 0].index
    return scores.drop(rated, errors='ignore')

def advanced_hybrid_recommend(user_id, user_weight=0.4, item_weight=0.4, content_weight=0.2, top_n=5):
    user_scores = user_user_cf(user_id)
    item_scores = item_item_cf(user_id)

    if user_scores.empty and item_scores.empty:
        return pd.DataFrame(columns=['destination', 'hybrid_score'])

    user_scores = (user_scores - user_scores.min()) / (user_scores.max() - user_scores.min() + 1e-9)
    item_scores = (item_scores - item_scores.min()) / (item_scores.max() - item_scores.min() + 1e-9)
    content_scores = pd.Series(0, index=user_scores.index.union(item_scores.index))

    hybrid_score = user_weight * user_scores.add(0, fill_value=0) + \
                   item_weight * item_scores.add(0, fill_value=0) + \
                   content_weight * content_scores.add(0, fill_value=0)

    return hybrid_score.sort_values(ascending=False).head(top_n).reset_index().rename(columns={0: 'hybrid_score'})

# ----------------- Routes -------------------
@app.route('/')
def home():
    return 'Flask Hybrid Recommender running! Use /register, /login, /rate, /profile.'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect('/profile')
        else:
            return "Invalid login"
    return render_template('login.html')

@app.route('/rate', methods=['GET', 'POST'])
def rate():
    if 'user_id' not in session:
        return redirect('/login')
    if request.method == 'POST':
        destination = request.form['destination']
        rating = int(request.form['rating'])
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO ratings (user_id, destination, rating) VALUES (%s, %s, %s)",
                    (session['user_id'], destination, rating))
        mysql.connection.commit()
        cur.close()
        return redirect('/profile')
    return render_template('rate.html', destinations=destinations_list)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']
    cur = mysql.connection.cursor()

    # Get username
    cur.execute("SELECT username FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    username = user[0] if user else "User"

    # Get user ratings
    cur.execute("SELECT destination, rating, id FROM ratings WHERE user_id = %s", (user_id,))
    user_ratings = cur.fetchall()
    cur.close()

    # Run hybrid recommender
    recs = advanced_hybrid_recommend(user_id)

    # Fallback for new users
    if recs.empty:
        top_destinations = df[['destination', 'Hotel Name', 'Hotel Rating']].dropna().drop_duplicates(subset=['destination'])
        top_destinations = top_destinations.sort_values('Hotel Rating', ascending=False).head(5)
        recs = pd.DataFrame({'destination': top_destinations['destination'].tolist(), 'hybrid_score': [0]*5})

    # Prepare hotel suggestions
    hotel_recommendations = []
    for dest in recs['destination']:
        hotels = df[df['destination'].str.lower().str.strip() == dest.lower().strip()][['Hotel Name', 'Hotel Rating']].dropna()
        hotels = hotels.drop_duplicates(subset=['Hotel Name'])
        hotels = hotels.sort_values('Hotel Rating', ascending=False).head(4)
        hotel_recommendations.append({
            'destination': dest,
            'hotels': hotels.to_dict(orient='records')
        })

    return render_template('profile.html',
                           username=username,
                           user_ratings=user_ratings,
                           hotel_recommendations=hotel_recommendations)

@app.route('/edit_rating/<int:rating_id>', methods=['GET', 'POST'])
def edit_rating(rating_id):
    if 'user_id' not in session:
        return redirect('/login')
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        new_rating = int(request.form['rating'])
        cur.execute("UPDATE ratings SET rating = %s WHERE id = %s AND user_id = %s",
                    (new_rating, rating_id, session['user_id']))
        mysql.connection.commit()
        cur.close()
        return redirect('/profile')
    cur.execute("SELECT destination, rating FROM ratings WHERE id = %s AND user_id = %s", (rating_id, session['user_id']))
    data = cur.fetchone()
    cur.close()
    if not data:
        return "Rating not found"
    return render_template('edit_rating.html', destination=data[0], rating=data[1], rating_id=rating_id)

@app.route('/delete_rating/<int:rating_id>')
def delete_rating(rating_id):
    if 'user_id' not in session:
        return redirect('/login')
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM ratings WHERE id = %s AND user_id = %s", (rating_id, session['user_id']))
    mysql.connection.commit()
    cur.close()
    return redirect('/profile')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect('/login')

@app.route('/criteria_display', methods=['POST'])
def submit():
    user_answer = request.form.get('answer')
    place = request.form.get('destination')

    if user_answer == 'YES':
        chat_session = model.start_chat(history=[{"role": "user", "parts": [{"text": f"{user_answer}"}]}])
        response = chat_session.send_message(
            f"Please provide travel criteria for {place}, including the best time to visit, estimated cost, and duration. "
            f"Make sure the output is formatted as follows:\n\n"
            f"Travel Criteria for {place}:\n\n"
            f"Best time to visit: [best time to visit info]\n\n"
            f"Estimated cost: [estimated cost info]\n\n"
            f"Duration: [duration info]\n\n"
            f"Show this output only in Bengali and make sure each section is on a new line with a blank line between them."
        )
        recommendation = response.text.strip()
        return render_template('criteria_display.html', sum=recommendation, destination=place)
    else:
        return render_template('criteria_display.html', sum='ধন্যবাদ')

# ----------------- Run App -------------------
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
