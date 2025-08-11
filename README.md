# Movie Recommendation System 🎬

A simple, interactive Streamlit app that recommends similar movies based on content similarity.

## Features

- 🔍 **Movie Recommendations:** Select a movie to get a list of similar movies.
- 🖼️ **Movie Posters:** Fetches posters using the OMDb API.
- 📊 **Similarity Scores:** Recommendations are ranked by similarity.
- ⚡ **Fast & Lightweight:** Uses precomputed similarity matrix for instant results.

## How It Works

- The app uses a **content-based filtering** approach.
- Each movie is represented by a set of tags (e.g., genres, keywords).
- A **similarity matrix** (precomputed and stored in `similarity.pkl`) contains pairwise similarity scores between all movies, based on their tags.
- When you select a movie, the app:
  1. Looks up its index in the dataset.
  2. Retrieves the most similar movies using the similarity matrix.
  3. Displays the top recommendations, ranked by similarity score.
- Movie posters are fetched live from the OMDb API using the movie title.

## How to Run

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Start the app:**
   ```
   streamlit run app.py
   ```

3. **(Optional) Set OMDb API Key:**
   - Enter your OMDb API key in the sidebar for poster images.
   - Default key is provided, but you can use your own for better reliability.

## Files

- `app.py` — Main Streamlit app.
- `movie_list.pkl` — Movie metadata and tags.
- `similarity.pkl` — Precomputed similarity matrix.
- `summary_report.py` — Script to analyze and summarize the dataset.
