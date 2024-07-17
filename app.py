import streamlit as st
import pickle
import pandas as pd
import requests

def FetchPoster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=8abb90bf25ef0de101e2e483768c664e&language=en-US'.format(
            movie_id), timeout=20)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def suggest_Movie(curr_movie):
    movie_index = movies[movies['title'] == curr_movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch the poster from API
        recommended_movies_posters.append(FetchPoster(movie_id))
    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selectedMovieName = st.selectbox('Select Your Movie', movies['title'].values)

if st.button('Suggest'):
    names, posters = suggest_Movie(selectedMovieName)

    col1, col2, col3, col4, col5 = st.columns(5)
    # Display movie recommendations in columns
    for i in range(5):
        with locals()[f"col{i + 1}"]:
            st.text(names[i])
            st.image(posters[i], width=150)  # Adjust image width for mobile
    # with col1:
    #     st.text(names[0])
    #     st.image(posters[0])
    # with col2:
    #     st.text(names[1])
    #     st.image(posters[1])
    # with col3:
    #     st.text(names[2])
    #     st.image(posters[2])
    # with col4:
    #     st.text(names[3])
    #     st.image(posters[3])
    # with col5:
    #     st.text(names[4])
    #     st.image(posters[4])
