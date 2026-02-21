# 🎬 Hybrid Movie Recommendation System

A Hybrid Movie Recommender built using:

- Content-Based Filtering (Genre Similarity)
- Demographic Filtering (Age + Occupation)
- Popularity-Based Scoring
- Streamlit Web Application

---

## 📌 Project Overview

This system recommends movies to a **new user** based on:

- 🎯 Preferred Genres  
- 👤 Age Group  
- 💼 Occupation  

The model combines three different recommendation strategies:

1. **Genre Similarity Score**
   - Manual cosine similarity using one-hot encoded genres  

2. **Demographic Score**
   - Average ratings from users with the same age group and occupation  

3. **Popularity Score**
   - Overall average rating of each movie  

---

## 🧠 Final Scoring Formula

Final Score =  
0.7 * Genre Score +  
0.1 * Demographic Score +  
0.2 * Popularity Score  

Movies are ranked based on this hybrid weighted score.

---

## 📂 Project Structure

```
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
```

---


## 🔧 Installation

### 1️⃣ Clone the Repository

```
git clone <your-repository-url>
cd movie-recommender
```

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

If you don’t have a `requirements.txt` file, install manually:

```
pip install streamlit pandas numpy
```

---

## ▶️ Run the Application

```
streamlit run main.py
```

The Streamlit app will open automatically in your browser.

---

## 👨‍💻 Author

Vinayak  
Machine Learning Project  