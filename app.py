import whisper
import gradio as gr
import os

import subprocess
# Try to install yt-dlp if not available
try:
    subprocess.check_call(["pip", "install", "yt-dlp"])
except subprocess.CalledProcessError as e:
    print(f"Error installing yt-dlp: {e}")

import yt_dlp

# Function to download the audio and extract metadata from YouTube
def download_video_info(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)  # Extract video info
            title = info.get('title', 'Unknown Title')
            thumbnail_url = info.get('thumbnail', '')
            ydl.download([url])  # Download the audio
        audio_file = "audio.mp3"
        return audio_file, title, thumbnail_url
    except Exception as e:
        return None, None, str(e)

# Function to transcribe the downloaded audio using Whisper
def transcribe_audio(audio_path, model_size="base"):
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)
    return result['text']

# Split logic: First fetch title and thumbnail, then transcribe
def get_video_info_and_transcribe(youtube_url, model_size="base"):
    # Fetch title and thumbnail first
    audio_path, title, thumbnail_url = download_video_info(youtube_url)
    
    # If fetching video info fails
    if not audio_path or not os.path.exists(audio_path):
        return gr.update(value=f"Error fetching video: {thumbnail_url}"), None, None, None

    # Show title and thumbnail to the user while the transcription is happening
    title_output = gr.update(value=title)
    thumbnail_output = gr.update(value=thumbnail_url)

    # Start transcription
    transcription = transcribe_audio(audio_path, model_size)

    return title_output, thumbnail_output, gr.update(value=transcription)

# Gradio interface setup using gradio.components
with gr.Blocks() as interface:
    with gr.Row():
        youtube_url = gr.Textbox(label="YouTube Link", elem_id="yt_link", scale=5)
        model_size = gr.Dropdown(choices=["tiny", "base", "small", "medium", "large"], label="Model Size", value="base", scale=1)
    
    title_output = gr.Textbox(label="Video Title", interactive=False)

    with gr.Row():
        thumbnail_output = gr.Image(label="Thumbnail", interactive=False, scale=1)
        transcription_output = gr.Textbox(label="Transcription", interactive=False, scale=1)
    
    transcribe_button = gr.Button("Transcribe")

    transcribe_button.click(
        get_video_info_and_transcribe, 
        inputs=[youtube_url, model_size],
        outputs=[title_output, thumbnail_output, transcription_output]
    )

# Launch the app
if __name__ == "__main__":
    interface.launch(share=True)