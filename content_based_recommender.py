import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load your dataset
df = pd.read_csv('updated_tour_with_hotels.csv')

# Step 1: TF-IDF Vectorization on combined_features
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined_features'])

# Step 2: Compute Cosine Similarity Matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Step 3: Build a reverse map of destination names to index
indices = pd.Series(df.index, index=df['destination']).drop_duplicates()

# Step 4: Recommendation Function
def recommend(destination_name, top_n=5):
    if destination_name not in indices:
        return f"Destination '{destination_name}' not found in dataset."

    # Get the index of the given destination
    idx = indices[destination_name]

    # Get the pairwise similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort destinations based on similarity score
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get top_n similar destinations (excluding itself)
    sim_scores = sim_scores[1:top_n+1]

    # Fetch destination indices
    destination_indices = [i[0] for i in sim_scores]

    # Return the top recommended destinations
    return df[['destination', 'location', 'category', 'Hotel Name', 'Hotel Rating']].iloc[destination_indices]

# Example Usage with User Input
if __name__ == "__main__":
    user_input = input("Enter a destination name: ")
    print(f"\nRecommended Places similar to '{user_input}':\n")
    print(recommend(user_input))
