import streamlit as st
import requests
import pandas as pd


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def fetch_movie_details(movie_id):
    api_key = '8265bd1679663a7ea12ac168da84d2e8'
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    data = response.json()

    description = data['overview']
    ratings = data['vote_average']
    release_date = data['release_date']

    # Fetching cast and crew details
    credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}"
    credits_response = requests.get(credits_url)
    credits_data = credits_response.json()

    cast = []
    for actor in credits_data['cast']:
        cast.append(actor['name'])

    crew = []
    for member in credits_data['crew']:
        if member['job'] == 'Director':
            crew.append(member['name'])

    return description, ratings, release_date, cast, crew


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_name = []
    recommended_movie_poster = []
    recommended_movie_description = []
    recommended_movie_rating = []
    recommended_movie_timeline = []
    recommended_movie_cast = []
    recommended_movie_crew = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_poster.append(fetch_poster(movie_id))
        recommended_movie_name.append(movies.iloc[i[0]].title)
        description, ratings, release_date, cast, crew = fetch_movie_details(movie_id)
        recommended_movie_description.append(description)
        recommended_movie_rating.append(ratings)
        recommended_movie_timeline.append(release_date)
        recommended_movie_cast.append(cast)
        recommended_movie_crew.append(crew)

    return (
        recommended_movie_name,
        recommended_movie_poster,
        recommended_movie_description,
        recommended_movie_rating,
        recommended_movie_timeline,
        recommended_movie_cast,
        recommended_movie_crew
    )


movies = pd.read_pickle('movie_list.pkl')
similarity = pd.read_pickle('similarity.pkl')

movie_list = movies['title'].values

# st.set_page_config(page_title='Movie Recommender System', page_icon='🎬')

# Set page header
st.header('Movie Recommender System')

# Add some spacing
st.write('')

# Create a sidebar for user inputs
with st.sidebar:
    # Add a title and description for the sidebar
    st.title('Preferences')

    # Add a dropdown for movie selection
    selected_movie = st.selectbox('Select a movie', movie_list)

    # Add a button to trigger recommendations
    show_recommendations = st.button('Recommendations', key='show_recommendations_button',
                                     help='Click to show recommendations')

    # Apply custom CSS style to the button
    button_style = """
        <style>
        .show-recommendations-button {
            background-color: white !important;
            color: black !important;
        }
        </style>
    """

st.subheader('Movie List')
st.write(movies)

# Display recommendations if button is clicked
if show_recommendations:
    st.subheader('\nRecommendations\n')
    # Fetch recommended movies
    (
        recommended_movie_names,
        recommended_movie_posters,
        recommended_movie_descriptions,
        recommended_movie_ratings,
        recommended_movie_timelines,
        recommended_movie_casts,
        recommended_movie_crews
    ) = recommend(selected_movie)

    # Display recommendation details in a grid layout
    num_recommendations = len(recommended_movie_names)
    num_columns = 2  # Updated to display only two movies per row
    num_rows = (num_recommendations + num_columns - 1) // num_columns

    col_width = int(12 / num_columns)
    row_height = 350

    container_style = 'padding: 10px; background-color: #222222; color: #FFFFFF; margin: 10px;'

    with st.container():
        for i in range(num_rows):
            row = st.columns(num_columns)
            for j in range(num_columns):
                index = i * num_columns + j
                if index < num_recommendations:
                    with row[j]:
                        with st.container():
                            st.image(recommended_movie_posters[index], use_column_width=True)
                            st.caption(f'<h3 style="font-size: 24px;">{recommended_movie_names[index]}</h3>', unsafe_allow_html=True)

                            st.markdown(f"<p style='font-size: 14px;'>{recommended_movie_descriptions[index]}</p>", unsafe_allow_html=True)
                            rating = recommended_movie_ratings[index]
                            rating_stars = '★' * int(rating) + '☆' * (5 - int(rating))
                            st.markdown(f"<p style='font-size: 14px;color: yellow;'>{rating_stars}</p>", unsafe_allow_html=True)
                            st.markdown(f"<p style='font-size: 14px;'>Timeline: {recommended_movie_timelines[index]}</p>", unsafe_allow_html=True)

                            cast_column, crew_column = st.columns(2)  # Create two columns for cast and crew

                            with cast_column:
                                st.markdown("<h4 style='font-size: 16px;'>Cast:</h4>", unsafe_allow_html=True)
                                for cast_member in recommended_movie_casts[index][:3]:  # Display top 3 cast members
                                    st.markdown(f"<p style='font-size: 14px;'>- {cast_member}</p>", unsafe_allow_html=True)

                            with crew_column:
                                st.markdown("<h4 style='font-size: 16px;'>Crew:</h4>", unsafe_allow_html=True)
                                for crew_member in recommended_movie_crews[index][:3]:  # Display top 3 crew members
                                    st.markdown(f"<p style='font-size: 14px;'>- {crew_member}</p>", unsafe_allow_html=True)






