import streamlit as st
import requests
from pytube import YouTube
from pytube import Search

# OpenWeatherMap API Key
api_key = "4e5f1dbfe280ccb6c3576630c8488dc4"
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://img.freepik.com/free-vector/flat-design-monsoon-season-clouds-illustration_23-2149424294.jpg");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Function to search YouTube and fetch multiple unique video URLs using pytube
def get_youtube_video_urls(query, num_results=3):
    try:
        # Use pytube Search to search YouTube for videos based on the query
        search = Search(query)
        search_results = search.results[:num_results]  # Limit to num_results
        
        video_urls = []
        for result in search_results:
            video_urls.append(f"https://www.youtube.com/watch?v={result.video_id}")
        
        return video_urls
    except Exception as e:
        st.error(f"Error fetching YouTube videos: {e}")
        return []

# Function to fetch weather based on city input
def get_weather(city):
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID={api_key}"
    weather = requests.get(weather_url)
    return weather.json()

# Streamlit UI
st.title("Weather-Based Song Suggestion")

# Input for city name
city = st.text_input("Enter the name of the city", "London")

# Initialize video URLs and current index in session state if not already done
if "video_urls" not in st.session_state:
    st.session_state.video_urls = []  # List to store video URLs
    st.session_state.current_song_index = 0  # Current index of the video being played

# Check if city input is provided
if city:
    # Get weather data
    weather_data = get_weather(city)

    if weather_data.get("cod") != 200:  # In case of error (invalid city)
        st.error(f"Could not fetch weather for {city}. Please try again.")
    else:
        # Extract weather condition
        weather_condition = weather_data["weather"][0]["main"]
        st.write(f"Weather in {city}: {weather_condition}")

        # Formulate a search query based on weather condition
        if weather_condition == "Clear":
            query = "sunny music relaxing hindi song"
        elif weather_condition == "Clouds":
            query = "cloudy relaxing music hindi song"
        elif weather_condition == "Rain":
            query = "rainy relaxing music hindi song"
        elif weather_condition == "Snow":
            query = "snow relaxing music hindi song"
        elif weather_condition == "Thunderstorm":
            query = "thunderstorm music hindi song"
        elif weather_condition == "Drizzle":
            query = "drizzle relaxing music hindi song"
        else:
            query = "weather relaxing music hindi song"

        # If video_urls is empty, fetch new videos
        if not st.session_state.video_urls:
            st.session_state.video_urls = get_youtube_video_urls(query)

        # Check if video URLs exist
        if st.session_state.video_urls:
            # Get the current video URL based on the index
            current_video_url = st.session_state.video_urls[st.session_state.current_song_index]
            st.write(f"Playing YouTube video for: {query}")
            st.video(current_video_url)

            # "Previous" and "Next" buttons to change songs
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Previous"):
                    # Move to the previous song in the list
                    st.session_state.current_song_index = (st.session_state.current_song_index - 1) % len(st.session_state.video_urls)
            with col2:
                if st.button("Next"):
                    # Move to the next song in the list
                    st.session_state.current_song_index = (st.session_state.current_song_index + 1) % len(st.session_state.video_urls)
        else:
            # Fallback video if no result found for weather-based query
            fallback_video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # A fallback video (e.g., Rick Astley's Never Gonna Give You Up)
            st.write(f"Couldn't find a video for the weather condition. Playing a fallback video.")
            st.video(fallback_video_url)
