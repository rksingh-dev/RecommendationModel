import streamlit as st
import pickle
import numpy as np
import os
import requests
from typing import List, Tuple

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="centered")

@st.cache_resource(show_spinner=False)
def load_data():
    with open('movie_list.pkl', 'rb') as f:
        movie_data = pickle.load(f)
    with open('similarity.pkl', 'rb') as f:
        similarity_matrix = pickle.load(f)

   
    num_movies = similarity_matrix.shape[0]
    titles_dict = movie_data['title']

    
    titles: List[str] = [titles_dict[i] for i in range(num_movies)]

   
    title_to_indices = {}
    for idx, title in enumerate(titles):
        title_to_indices.setdefault(title, []).append(idx)

    return titles, title_to_indices, similarity_matrix, movie_data


@st.cache_data(show_spinner=False)
def fetch_poster_url(title: str, api_key: str) -> str | None:
    if not api_key:
        return None
    try:
        resp = requests.get(
            "http://www.omdbapi.com/",
            params={"t": title, "apikey": api_key},
            timeout=6,
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
        if data.get("Response") == "True":
            poster = data.get("Poster")
            if poster and poster != "N/A":
                return poster
    except Exception:
        return None
    return None


def get_recommendations(selected_index: int, similarity_matrix: np.ndarray, titles: List[str], top_k: int = 10) -> List[Tuple[str, float, int]]:
    scores = similarity_matrix[selected_index]
    
    sorted_indices = np.argsort(scores)[::-1]

    recommendations: List[Tuple[str, float, int]] = []
    for idx in sorted_indices:
        if idx == selected_index:
            continue
        recommendations.append((titles[idx], float(scores[idx]), int(idx)))
        if len(recommendations) >= top_k:
            break
    return recommendations


def main():
    st.title("🎬 Movie Recommendation")
    st.caption("Pick a movie to see similar movies, with posters fetched from OMDb.")

  
    default_key = "a42bd021" 
    try:
        
        if hasattr(st, 'secrets') and st.secrets:
            default_key = st.secrets.get("OMDB_API_KEY", default_key)
    except Exception:
       
        default_key = os.getenv("OMDB_API_KEY", default_key)

    api_key = st.sidebar.text_input("OMDb API Key", value=default_key, type="password")
    st.sidebar.caption("Using OMDb to retrieve movie posters.")

    try:
        titles, title_to_indices, similarity_matrix, movie_data = load_data()
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        st.stop()

  
    selected_title = st.selectbox("Choose a movie", options=titles, index=0)

   
    candidate_indices = title_to_indices.get(selected_title, [])
    selected_index = candidate_indices[0] if candidate_indices else 0
    if len(candidate_indices) > 1:
        selected_index = st.selectbox(
            "Multiple entries found for this title. Choose which one:",
            options=candidate_indices,
            format_func=lambda i: f"Index {i}",
        )

    top_k = st.slider("How many recommendations?", min_value=5, max_value=20, value=10, step=1)

    if st.button("Recommend"):
        recs = get_recommendations(selected_index, similarity_matrix, titles, top_k=top_k)

        st.subheader("Similar movies")
        st.write(f"Based on: {selected_title}")

       
        num_cols = 5 if top_k >= 10 else 3
        cols = st.columns(num_cols)
        for i, (title, score, idx) in enumerate(recs):
            col = cols[i % num_cols]
            with col:
                poster_url = fetch_poster_url(title, api_key)
                if poster_url:
                    st.image(poster_url, use_column_width=True)
                st.markdown(f"**{title}**")
                st.caption(f"Similarity: {score:.3f}")

        
        with st.expander("Show as table"):
            st.dataframe(
                {
                    "Rank": list(range(1, len(recs) + 1)),
                    "Title": [r[0] for r in recs],
                    "Similarity": [round(r[1], 4) for r in recs],
                },
                hide_index=True,
            )

       
        with st.expander("Show tags for selected movie"):
            tags_dict = movie_data.get('tags', {})
            if selected_index in tags_dict:
                tags = tags_dict[selected_index]
                st.write(", ".join(tags[:200]))
            else:
                st.write("No tags available.")


if __name__ == "__main__":
    main()
