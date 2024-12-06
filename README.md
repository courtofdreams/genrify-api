# Genre Recommendation System

This project is a genre recommendation system and API. It uses TF-IDF for similarity calculations, compared with spotify genre list (all_spotify_genres.txt) and adjusts recommendations based on artist popularity and listening count.

Note: This project is a part of Info 202 - Information Organization and Retrieval.

## Features

- Identify undiscovered genres
- Calculate genre similarity using TF-IDF
- Adjust recommendations based on artist popularity
- Boost genres with matching prefixes, I co

## APIs

Genre Recommendation: POST /recommend-genre

- It takes user data, a list of genres, the genre hierarchy, and precomputed genre vectors to generate genre recommendations, Then calculates the popularity of each genre based on user data. It identifies genres that the user has not yet explored, using TF-IDF and cosine similarity to find genres similar to those the user has explored. It adjusts the recommendations based on genre popularity and boosts genres with matching prefixes, Then returns the top N unique genre recommendations.

## Requirements

- Python
- Flask
- Flask-CORS
- scikit-learn

## Installation

1. Clone the repository:
2. Create a virtual environment (Optional)
3. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Run the Flask application:

   ```sh
   python app.py
   ```

2. The application will be available at `http://0.0.0.0:8080/`.

## API Endpoints

### `POST /recommend-genre`
Note: I retrieved artist' followers just to use it to compared if its relevant to popularity or not, and it is relevant, so I use only popularity for the calculation.

Request body:

```json
{
  "ArtistSpotifyID1": {
    "listeningCount": 1,
    "genres": ["edm", "pop dance", "progressive electro house"],
    "popularity": 77,
    "follower": 3866287
  },
    "ArtistSpotifyID2": {
    "listeningCount": 1,
    "genres": ["k-pop", "pop dance"],
    "popularity": 22,
    "follower": 3866287
  }
}
```


Response: 
    
```json
{
    "recommendedGenres": ["pop dance", "progressive electro house", "edm"]
}
```