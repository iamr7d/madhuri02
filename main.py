import io
import pygame
import streamlit as st
from pyht import Client
from pyht.client import TTSOptions
from pydub import AudioSegment

# Initialize pygame for music playback
pygame.init()
pygame.mixer.init()

# Streamlit sidebar inputs for user credentials and file name
with st.sidebar:
    st.header("PlayHT Settings")
    user_id = st.text_input("Enter your PlayHT User ID:", "EFBFJScUv8UUpZR5c5TbQvrTwfj2")
    api_key = st.text_input("Enter your PlayHT API Key:", "f5ac6befb13a49f3a741ae05fe6a18f8")
    day = st.text_input("Enter the day (e.g., 01 for the first day):", "01")
    tts_number = st.text_input("Enter the TTS number:", "01")
    speed = st.slider("Select Speech Speed:", min_value=0.5, max_value=2.0, value=0.9, step=0.1)

# Initialize pyht client with user credentials
pyht_client = Client(
    user_id=user_id,
    api_key=api_key
)

def text_to_speech_realtime(text, speed):
    """Convert text to speech and save it as an MP3 file using pyht."""
    options = TTSOptions(
        voice="s3://voice-cloning-zero-shot/f3c22a65-87e8-441f-aea5-10a1c201e522/original/manifest.json",
        speed=speed
    )
    audio_data = io.BytesIO()
    
    # Fetch the TTS audio data chunk by chunk
    for chunk in pyht_client.tts(text, options):
        audio_data.write(chunk)
    
    audio_data.seek(0)
    
    # Convert the audio data to MP3 format
    filename = f"{day}{tts_number}DUKRAD.mp3"
    audio = AudioSegment.from_file(io.BytesIO(audio_data.getvalue()), format="wav")
    audio.export(filename, format="mp3")
    
    # Return the filename and the audio data for playback
    return filename, audio_data

# Streamlit app layout
st.title("Text to Speech with PlayHT")
user_input = st.text_input("Enter the text you want to convert to speech:")

if st.button("Convert to Speech"):
    if user_input:
        st.write(f"Converting the following text: {user_input}")
        filename, audio_data = text_to_speech_realtime(user_input, speed)
        
        st.success(f"Audio saved as {filename}")
        
        # Provide playback for the generated TTS audio
        st.audio(audio_data, format="audio/mp3")
        
        # Provide a download link for the audio file
        with open(filename, "rb") as f:
            st.download_button(
                label="Download Audio",
                data=f,
                file_name=filename,
                mime="audio/mpeg"
            )
    else:
        st.warning("Please enter some text!")

# File uploader for music files
st.sidebar.header("Upload Music")
uploaded_file = st.sidebar.file_uploader("Choose a music file (MP3 only):", type="mp3")

if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    temp_file_path = "temp_music.mp3"
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.read())

    # Load and play the uploaded music file
    st.audio(temp_file_path, format="audio/mp3")

    # Optionally, you can play the uploaded music using pygame
    pygame.mixer.music.load(temp_file_path)
    pygame.mixer.music.play(loops=-1)  # Loop the music
