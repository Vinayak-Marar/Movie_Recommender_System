import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Hybrid Movie Recommender", layout="wide")

st.title("🎬 Hybrid Movie Recommendation System")

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():
    movies = pd.read_csv(
        "data/movies.csv",
        names=['movieId','title','genre']
    )

    ratings = pd.read_csv(
        "data/ratings.csv",
        names=['userId','movieId','rating','timestamp']
    )

    users = pd.read_csv(
        "data/users.csv",
        names=['userId','gender','age','occupation','zip-code']
    )

    return movies, ratings, users


movies, ratings, users = load_data()

# =====================================================
# PREPROCESSING (GENRE ONE HOT + POPULARITY)
# =====================================================

@st.cache_data
def preprocess(movies, ratings):

    movies = movies.copy()

    # Extract unique genres
    all_genres = sorted(
        list(set(g for sub in movies['genre'].str.split('|') for g in sub))
    )

    # One-hot encode genres
    for genre in all_genres:
        movies[genre] = movies['genre'].apply(
            lambda x: 1 if genre in x.split('|') else 0
        )

    # Popularity score
    movie_popularity = ratings.groupby('movieId')['rating'].mean().reset_index()
    movie_popularity.columns = ['movieId','popularity_score']

    movies = movies.merge(movie_popularity, on='movieId', how='left')
    movies['popularity_score'] = movies['popularity_score'].fillna(0)

    return movies, all_genres


movies, all_genres = preprocess(movies, ratings)

# =====================================================
# HYBRID FUNCTION (UNCHANGED LOGIC)
# =====================================================

def hybrid_recommend(age, occupation, preferred_genres, top_n=10):

    movies_copy = movies.copy()

    # -------- Genre Score --------
    genre_vector = np.zeros(len(all_genres))

    for i, genre in enumerate(all_genres):
        if genre in preferred_genres:
            genre_vector[i] = 1

    movie_genre_matrix = movies_copy[all_genres].values

    genre_score = movie_genre_matrix.dot(genre_vector)

    genre_score = genre_score / (np.linalg.norm(movie_genre_matrix, axis=1) + 1e-8)


    # -------- Demographic Score --------
    similar_users = users[
        (users['age'] == age) &
        (users['occupation'] == occupation)
    ]['userId']

    demo_ratings = ratings[ratings['userId'].isin(similar_users)]

    demo_score = demo_ratings.groupby('movieId')['rating'].mean()

    movies_copy['demo_score'] = movies_copy['movieId'].map(demo_score)
    movies_copy['demo_score'] = movies_copy['demo_score'].fillna(0)


    # -------- Popularity Score --------
    pop_score = movies_copy['popularity_score'].fillna(0)


    # -------- Final Weighted Score --------
    w1, w2, w3 = 0.7, 0.1, 0.2

    movies_copy['final_score'] = (
        w1 * genre_score +
        w2 * movies_copy['demo_score'] +
        w3 * pop_score
    )

    return movies_copy.sort_values(
        'final_score',
        ascending=False
    )[["title","genre","final_score"]].head(top_n)


# =====================================================
# AGE & OCCUPATION MAPPING
# =====================================================

age_map = {
    "Under 18": 1,
    "18-24": 18,
    "25-34": 25,
    "35-44": 35,
    "45-49": 45,
    "50-55": 50,
    "56+": 56
}

occupation_map = {
    0: "other",
    1: "academic/educator",
    2: "artist",
    3: "clerical/admin",
    4: "college/grad student",
    5: "customer service",
    6: "doctor/health care",
    7: "executive/managerial",
    8: "farmer",
    9: "homemaker",
    10: "K-12 student",
    11: "lawyer",
    12: "programmer",
    13: "retired",
    14: "sales/marketing",
    15: "scientist",
    16: "self-employed",
    17: "technician/engineer",
    18: "tradesman/craftsman",
    19: "unemployed",
    20: "writer"
}

occupation_reverse_map = {v: k for k, v in occupation_map.items()}

# =====================================================
# STREAMLIT UI (NOT SIDEBAR)
# =====================================================

st.subheader("👤 Enter Your Preferences")

col1, col2 = st.columns(2)

with col1:
    selected_age_label = st.selectbox(
        "Select Age Group",
        list(age_map.keys())
    )
    age = age_map[selected_age_label]

with col2:
    selected_occupation_label = st.selectbox(
        "Select Occupation",
        list(occupation_reverse_map.keys())
    )
    occupation = occupation_reverse_map[selected_occupation_label]

preferred_genres = st.multiselect(
    "Select Preferred Genres",
    all_genres
)

top_n = st.slider("Number of Recommendations", 5, 20, 10)

# =====================================================
# RECOMMEND BUTTON
# =====================================================

if st.button("Recommend Movies"):

    if not preferred_genres:
        st.warning("Please select at least one genre.")
    else:
        result = hybrid_recommend(age, occupation, preferred_genres, top_n)

        st.subheader("🎥 Recommended Movies")
        st.dataframe(result, use_container_width=True)