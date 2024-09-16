import whisper
import gradio as gr
import os

import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="torch")

from download_video import download_mp3_selenium 

# Function to download the audio, title, and thumbnail from YouTube
def download_video_info(url):
    try:
        # Call the function to download video and get title, thumbnail, and logs
        title, thumbnail_url, logs_output = download_mp3_selenium(url)
        audio_file = "downloaded_video.mp4"  # Path to the downloaded audio (MP4)

        return audio_file, title, thumbnail_url, logs_output
    except Exception as e:
        return None, None, None, str(e)

# Function to transcribe the downloaded audio using Whisper
def transcribe_audio(audio_path, model_size="base"):
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)
    return result['text']

# Split logic: First fetch title, thumbnail, and logs, then transcribe
def get_video_info_and_transcribe(youtube_url, model_size="base"):
    # Fetch title, thumbnail, and logs first
    audio_path, title, thumbnail_url, logs_output = download_video_info(youtube_url)
    
    # If fetching video info fails
    if not audio_path or not os.path.exists(audio_path):
        return gr.update(value=f"Error fetching video: {thumbnail_url}"), None, None, gr.update(value=logs_output)

    # Show title and thumbnail to the user while the transcription is happening
    title_output = gr.update(value=title)
    
    # Show the thumbnail if available
    if thumbnail_url:
        thumbnail_output = gr.update(value=thumbnail_url)
    else:
        thumbnail_output = gr.update(visible=False)  # Hide if no thumbnail
    
    # Start transcription
    transcription = transcribe_audio(audio_path, model_size)

    return title_output, thumbnail_output, gr.update(value=transcription), gr.update(value=logs_output)

# Gradio interface setup using gradio.components
with gr.Blocks() as interface:
    with gr.Row():
        youtube_url = gr.Textbox(label="YouTube Link", elem_id="yt_link", scale=5)
        model_size = gr.Dropdown(choices=["tiny", "base", "small", "medium", "large"], label="Model Size", value="base", scale=1)
    
    title_output = gr.Textbox(label="Video Title", interactive=False)

    with gr.Row():
        thumbnail_output = gr.Image(label="Thumbnail", interactive=False, scale=1)
        transcription_output = gr.Textbox(label="Transcription", interactive=False, scale=1)
    
    logs_output = gr.Textbox(label="ChromeDriver Logs", interactive=False)

    transcribe_button = gr.Button("Transcribe")

    transcribe_button.click(
        get_video_info_and_transcribe, 
        inputs=[youtube_url, model_size],
        outputs=[title_output, thumbnail_output, transcription_output, logs_output]
    )

# Launch the app
if __name__ == "__main__":
    interface.launch(share=True)