🎬 Hybrid Movie Recommendation System

A Hybrid Movie Recommender built using:

Content-Based Filtering (Genre similarity)

Demographic Filtering (Age + Occupation)

Popularity-Based Scoring

Streamlit Web Application

📌 Project Overview

This system recommends movies to a new user based on:

🎯 Preferred Genres

👤 Age Group

💼 Occupation

It combines three components:

Genre Similarity Score (Cosine-based manual similarity)

Demographic Score (Average ratings from similar users)

Popularity Score (Average movie rating overall)

Final Score:

Final Score = 
0.7 * Genre Score +
0.1 * Demographic Score +
0.2 * Popularity Score


📂 Project Structure

movie-recommender/
│
├── main.py
├── eda_training.ipynb
├── README.md
│
├── data/
│   ├── movies.csv
│   ├── ratings.csv
│   └── users.csv
│
└── requirements.txt


🔧 Installation

Clone the repository

git clone <your-repo-url>
cd movie-recommender

Install dependencies

pip install -r requirements.txt

If you don’t have requirements.txt, install manually:

pip install streamlit pandas numpy
▶️ Run the App
streamlit run main.py

The app will open in your browser.