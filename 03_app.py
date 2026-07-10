import streamlit as st
import pandas as pd
import joblib

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="🎬 Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# ---------------------------------------------------
# Custom CSS
# ---------------------------------------------------

st.markdown("""
<style>

.stApp{
    background: linear-gradient(to bottom,#0f172a,#020617);
}

.main-title{
    font-size:50px;
    text-align:center;
    font-weight:bold;
    color:#E50914;
}

.sub-title{
    text-align:center;
    color:white;
    font-size:20px;
    margin-bottom:30px;
}

.movie-card{
    background:#1E293B;
    padding:12px;
    border-radius:12px;
    text-align:center;
    color:white;
    font-size:18px;
    font-weight:bold;
    margin-top:8px;
    box-shadow:0px 0px 10px rgba(255,255,255,0.1);
}

div.stButton > button{
    width:100%;
    background-color:#E50914;
    color:white;
    border:none;
    border-radius:10px;
    height:50px;
    font-size:18px;
    font-weight:bold;
}

div.stButton > button:hover{
    background:#ff2d3f;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Title
# ---------------------------------------------------

st.markdown("""
<div class="main-title">
🎬 Movie Recommendation System
</div>

<div class="sub-title">
Discover movies similar to your favourite movie using AI
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Load Dataset
# ---------------------------------------------------

df = pd.read_csv("cleaned_data.csv")
df.reset_index(drop=True, inplace=True)

similarities = joblib.load("similarity.joblib")

movies = df["title"].tolist()

# ---------------------------------------------------
# Helper Functions
# ---------------------------------------------------

def get_name_by_index(i):
    if 0 <= i < len(df):
        return df.loc[i, "title"]
    return ""


def get_index_from_name(name):

    clean_name = name.strip().lower().replace(" ", "").replace("-", "")

    match = df[
        df["title"]
        .str.lower()
        .str.replace(" ", "", regex=False)
        .str.replace("-", "", regex=False)
        == clean_name
    ]

    if not match.empty:
        return match.index[0]

    return -1

# ---------------------------------------------------
# Movie Selection
# ---------------------------------------------------

st.markdown("### 🎥 Select Your Favourite Movie")

name = st.selectbox(
    "",
    movies,
    index=0
)

st.markdown(f"""
## 🎬 Selected Movie

### **{name}**

⭐ Click the **Recommend Movies** button to discover five similar movies.
""")

# ---------------------------------------------------
# Recommend Button
# ---------------------------------------------------

if st.button("🎬 Recommend Movies"):

    index = get_index_from_name(name)

    if index == -1:

        st.error("Movie not found.")

    else:

        similarity_indexes = list(enumerate(similarities[index]))

        similarity_indexes = sorted(
            similarity_indexes,
            key=lambda x: x[1],
            reverse=True
        )

        st.divider()

        st.success(f"Top 5 recommendations for **{name}**")

        cols = st.columns(5)

        for i in range(1, 6):

            movie_index = similarity_indexes[i][0]

            movie_name = get_name_by_index(movie_index)

            with cols[i-1]:

                st.markdown(
                    f"""
                    <div class="movie-card">
                    🎬<br><br>
                    {movie_name}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# ---------------------------------------------------
# Footer
# ---------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:gray; font-size:16px;">
        🎬 Movie Recommendation System <br>
        Built with ❤️ using <b>Streamlit</b>, <b>Joblib</b>, <b>Pandas</b>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

with st.sidebar:

    st.title("🎬 About")

    st.write("""
This Movie Recommendation System recommends movies similar to your selected movie using **Content-Based Filtering**.

### Technologies Used
- 🐍 Python
- 🎈 Streamlit
- 📊 Pandas
- 🤖 Scikit-learn
- 💾 Joblib

### Recommendation Algorithm
Recommendations are generated using **Cosine Similarity** on movie features.

---
Created by **Madhura Koshti**
""")