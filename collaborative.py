# ✅ Collaborative Filtering with MySQL Connection
from flask import Flask
from flask_mysqldb import MySQL
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)

# ✅ MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tour_recommendation'

mysql = MySQL(app)

# ✅ Load ratings data from MySQL
def load_ratings():
    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id, destination, rating FROM ratings")
    data = cur.fetchall()
    cur.close()
    ratings_df = pd.DataFrame(data, columns=['user_id', 'destination', 'rating'])
    return ratings_df

# ✅ User-User Collaborative Filtering
def user_user_cf(target_user_id, top_n=5):
    ratings_df = load_ratings()
    user_item_matrix = ratings_df.pivot_table(index='user_id', columns='destination', values='rating').fillna(0)

    # Calculate cosine similarity between users
    user_similarity = cosine_similarity(user_item_matrix)
    user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)

    # Get similar users
    similar_users = user_similarity_df[target_user_id].sort_values(ascending=False)[1:]

    # Weighted sum of ratings from similar users
    weighted_ratings = user_item_matrix.T.dot(similar_users) / similar_users.sum()

    # Filter out already rated by the target user
    rated_items = user_item_matrix.loc[target_user_id][user_item_matrix.loc[target_user_id] > 0].index
    recommendations = weighted_ratings.drop(rated_items).sort_values(ascending=False).head(top_n)

    return recommendations.reset_index().rename(columns={0: 'predicted_rating'})

# ✅ Item-Item Collaborative Filtering
def item_item_cf(target_user_id, top_n=5):
    ratings_df = load_ratings()
    user_item_matrix = ratings_df.pivot_table(index='user_id', columns='destination', values='rating').fillna(0)

    # Transpose for item similarity
    item_similarity = cosine_similarity(user_item_matrix.T)
    item_similarity_df = pd.DataFrame(item_similarity, index=user_item_matrix.columns, columns=user_item_matrix.columns)

    user_ratings = user_item_matrix.loc[target_user_id]
    scores = item_similarity_df.dot(user_ratings).div(item_similarity_df.sum(axis=1))

    # Filter out already rated
    rated_items = user_ratings[user_ratings > 0].index
    recommendations = scores.drop(rated_items).sort_values(ascending=False).head(top_n)

    return recommendations.reset_index().rename(columns={0: 'predicted_rating'})

# ✅ Example usage inside Flask route or function
@app.route('/user_cf/<int:user_id>')
def user_cf_route(user_id):
    recs = user_user_cf(user_id)
    return recs.to_html()

@app.route('/item_cf/<int:user_id>')
def item_cf_route(user_id):
    recs = item_item_cf(user_id)
    return recs.to_html()

if __name__ == '__main__':
    app.run(debug=True, port=5050)
