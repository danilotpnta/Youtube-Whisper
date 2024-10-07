import os
import whisper
import gradio as gr
from download_video import download_mp3_yt_dlp 

import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="torch")

# Function to download the audio, title, and thumbnail from YouTube
def download_video_info(url):
    try:
        # Call the function to download video and get title, thumbnail
        title, thumbnail_url = download_mp3_yt_dlp(url)
        audio_file = "downloaded_video.mp3"  # Path to the downloaded audio (MP3)

        return audio_file, title, thumbnail_url
    except Exception as e:
        return None, None, None, str(e)

# Function to transcribe the downloaded audio using Whisper
def transcribe_audio(audio_path, model_size="base", language="en"):
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path, language=language)
    return result['text']

# Split logic: First fetch title and thumbnail, then transcribe
def get_video_info_and_transcribe(youtube_url, model_size="base", language="en"):
    # Fetch title and thumbnail first
    audio_path, title, thumbnail_url = download_video_info(youtube_url)
    
    # If fetching video info fails
    if not audio_path or not os.path.exists(audio_path):
        return gr.update(value="Error fetching video."), None, None

    # Show title and thumbnail to the user while the transcription is happening
    title_output = gr.update(value=title)
    
    # Show the thumbnail if available
    if thumbnail_url:
        thumbnail_output = gr.update(value=thumbnail_url)
    else:
        thumbnail_output = gr.update(visible=False)  # Hide if no thumbnail
    
    # Start transcription
    transcription = transcribe_audio(audio_path, model_size, language)

    return title_output, thumbnail_output, gr.update(value=transcription)

# Gradio interface setup using gradio.components
with gr.Blocks() as demo:

    title = "<center><h1>YouTube Whisper ⚡️ </h1></center>"
    gr.HTML(title)

    gr.Markdown(
    """
    This tool lets you transcribe YouTube videos in multiple languages using **[Whisper](https://openai.com/research/whisper)**, an open-source speech recognition (ASR) model developed by OpenAI.


    ### Key Features:
    - **Fast transcription**: Using the **base** model, transcribing a **3 minute** video takes approximately **30 seconds**.
    - **Multiple language support**: Choose from **English**, **Spanish**, **French**, and more!
    - **Simple workflow**: 
        1. Paste a YouTube link.
        2. Select the model size and language.
        3. Click "Transcribe" to get the text from the video.

    _Transcription times may vary based on model size and video length._
    """)

    with gr.Row():
        youtube_url = gr.Textbox(label="YouTube Link", elem_id="yt_link", scale=5)
        model_size = gr.Dropdown(choices=["tiny", "base", "small", "medium", "large"], label="Model Size", value="base", scale=1)
        language = gr.Dropdown(choices=["en", "es", "fr", "de", "it", "ja"], label="Language", value="en", scale=1)
    
    title_output = gr.Textbox(label="Video Title", interactive=False)

    with gr.Row():
        thumbnail_output = gr.Image(label="Thumbnail", interactive=False, scale=1)
        transcription_output = gr.Textbox(label="Transcription", interactive=False, scale=1)
    
    transcribe_button = gr.Button("Transcribe")

    transcribe_button.click(
        get_video_info_and_transcribe, 
        inputs=[youtube_url, model_size, language],
        outputs=[title_output, thumbnail_output, transcription_output]
    )

# Launch the app
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
