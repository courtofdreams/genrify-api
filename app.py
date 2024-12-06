from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

# Function to read genres from file
def read_genres(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        genres = [line.strip() for line in file if line.strip()]
    return genres

# Function to build a hierarchy from genres
def build_hierarchy(genres):
    hierarchy = {}
    for genre in genres:
        parent_found = False
        for potential_parent in genres:
            if genre != potential_parent and genre.startswith(potential_parent):
                hierarchy.setdefault(potential_parent, []).append(genre)
                parent_found = True
        if not parent_found:
            hierarchy.setdefault(genre, [])
    return hierarchy

def recommend_genres(user_data, genres, hierarchy, top_n=3):
    # Calculate genre popularity
    user_genre_popularity = {}
    for artist_data in user_data.values():
        for genre in artist_data['genres']:
            if genre not in user_genre_popularity:
                user_genre_popularity[genre] = {"total_popularity": 0, "count": 0}
            user_genre_popularity[genre]["total_popularity"] += artist_data["popularity"]
            user_genre_popularity[genre]["count"] += 1
    # Calculate average popularity for each genre
    user_genre_popularity = {
        genre: data["total_popularity"] / data["count"]
        for genre, data in user_genre_popularity.items()
    }
    # Extract user genres
    user_genres = [genre for artist_data in user_data.values() for genre in artist_data["genres"]]
    explored_genres = set(user_genres)

    # Identify undiscovered genres
    undiscovered_genres = [genre for genre in genres if genre not in explored_genres]

    # Use TF-IDF for similarity calculation
    vectorizer = TfidfVectorizer()
    genre_vectors = vectorizer.fit_transform(genres)

    recommendations = []
    for explored_genre in explored_genres:
        if explored_genre in genres:
            explored_vector = vectorizer.transform([explored_genre])
            similarities = cosine_similarity(explored_vector, genre_vectors).flatten()
            sorted_similarities = [
                (genres[i], similarities[i]) for i in range(len(genres))
                if genres[i] in undiscovered_genres
            ]
            recommendations.extend(sorted_similarities)

    # Adjust recommendations by incorporating genre popularity
    weighted_recommendations = []
    for genre, similarity in recommendations:
        genre_popularity = user_genre_popularity.get(genre, 0)  # Default popularity to 0 if unknown
        weighted_score = similarity * 0.7 + genre_popularity * 0.3  # Adjust weights as needed

        # Boost genres with matching prefixes
        if any(genre.startswith(explored.split('-')[0]) for explored in explored_genres):
            weighted_score += 0.2  # Boost score for matching prefixes

        weighted_recommendations.append((genre, weighted_score))

    # Debugging: Print scores for each genre
    print("Debugging Weighted Recommendations:")
    for genre, score in weighted_recommendations:
        print(f"Genre: {genre}, Weighted Score: {score}")

    # Sort and return top N unique recommendations
    weighted_recommendations = sorted(weighted_recommendations, key=lambda x: x[1], reverse=True)
    unique_recommendations = []
    seen_genres = set()
    for genre, score in weighted_recommendations:
        if genre not in seen_genres:
            unique_recommendations.append(genre)
            seen_genres.add(genre)
        if len(unique_recommendations) >= top_n:
            break

    return unique_recommendations
    
def calculate_genre_popularity(user_data):
    genre_popularity = {}
    for artist in user_data.values():
        genres = artist['genres']  # Assuming genres is a list
        popularity = artist.get('popularity', 0)
        for genre in genres:  # Loop through each genre for the artist
            if genre not in genre_popularity:
                genre_popularity[genre] = {"total_popularity": 0, "count": 0}
            genre_popularity[genre]["total_popularity"] += popularity
            genre_popularity[genre]["count"] += 1

    # Calculate average popularity for each genre
    print(genre_popularity)
    return {
        genre: data["total_popularity"] / data["count"]
        for genre, data in genre_popularity.items()
    }


file_path = "all_spotify_genres.txt"
genres = read_genres(file_path)
hierarchy = build_hierarchy(genres)

# Flask API endpoint
@app.route('/recommend-genre', methods=["POST"])
def recommend_genre_api():
    try:
        # Load genres and build hierarchy

        # Parse user data
        user_data = request.json
        if not user_data:
            return jsonify({"error": "No data provided"}), 400

        # Recommend a genre
        recommendation = recommend_genres(user_data, genres, hierarchy)
        if recommendation:
            return jsonify({"genreRecommendation": recommendation}), 200
        else:
            return jsonify({"message": "No new genres to recommend"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
