import streamlit as st  # for quick building of web applications
import pickle   # serialization module(converts Python objects to binary serialized files)
import requests # to communicate with websites/APIs through HTTP requests
import base64   # encoding module to convert binary data to text files

# Fetch Poster and Ratings Function
def fetch_movie_details(movie_name):

    url = f"http://www.omdbapi.com/?t={movie_name}&apikey=104a3176"
    data = requests.get(url).json()

    poster = data.get(
        'Poster',
        'https://via.placeholder.com/300x450?text=No+Poster'
    )
    rating = data.get(
        'imdbRating',
        'N/A'
    )

    return poster, rating


# Recommendation Function
def recommend(movie):

    movie_index = movies_list[movies_list['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[movie_index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_ratings = []

    for i in distances[1:6]:

        movie_name = movies_list.iloc[i[0]].title
        poster, rating = fetch_movie_details(movie_name)

        recommended_movies_posters.append(poster)
        recommended_movies_ratings.append(rating)
        recommended_movies.append(movie_name)

    return recommended_movies, recommended_movies_posters,  recommended_movies_ratings


# Addition of background image for the website
def add_bg_from_local(image_file):

    with open(image_file, "rb") as image:
        encoded_string = base64.b64encode(
            image.read()
        ).decode()

    st.markdown(
        f"""
        <style>

        .stApp {{

            background-image:
            linear-gradient(
                rgba(0,0,0,0.7),
                rgba(0,0,0,0.7)
            ),

            url("data:image/jpg;base64,{encoded_string}");

            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        </style>
        """,

        unsafe_allow_html=True
    )

# Function call for background image
add_bg_from_local('background.jpg')

# Streamlit UI
st.title('MOVIE RECOMMENDER SYSTEM')


# Load pickle files
movies_list = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Movie titles
movie_list = movies_list['title'].values

# Dropdown feature
selected_movie = st.selectbox(
    "Select a movie:",
    movie_list
)

# Recommendation button
if st.button("Recommend"):

    names, posters, ratings = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.write("⭐ IMDb:", ratings[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.write("⭐ IMDb:", ratings[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.write("⭐ IMDb:", ratings[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.write("⭐ IMDb:", ratings[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.write("⭐ IMDb:", ratings[4])
        st.image(posters[4])