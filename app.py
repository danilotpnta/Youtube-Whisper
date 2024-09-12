import yt_dlp
import whisper
import gradio as gr
import os

# Function to download the audio from YouTube using yt-dlp
def download_audio(url):
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
            ydl.download([url])
        audio_file = "audio.mp3"
        return audio_file
    except Exception as e:
        return str(e)  # Return the error message for debugging

# Function to transcribe the downloaded audio using Whisper
def transcribe_audio(audio_path):
    model = whisper.load_model("base")  # Use other models like "small", "medium", "large" if necessary
    result = model.transcribe(audio_path)
    return result['text']

# Main function to integrate download and transcription
def transcribe_youtube_video(youtube_url):
    audio_path = download_audio(youtube_url)
    if not os.path.exists(audio_path):  # Check if an error was returned
        return f"Error: {audio_path}"  # Return the error message to the user
    transcription = transcribe_audio(audio_path)
    return transcription

# Gradio interface setup using gradio.components
interface = gr.Interface(
    fn=transcribe_youtube_video,
    inputs=gr.components.Textbox(label="YouTube URL"),
    outputs=gr.components.Textbox(label="Transcription"),
    title="YouTube Video Transcription",
    description="Paste a YouTube video link to get the audio transcribed using Whisper."
)

# Launch the app
if __name__ == "__main__":
    interface.launch(share=True)  # Enables sharing with public link