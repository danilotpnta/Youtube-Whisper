# Youtube-Whisper
A simple Gradio app that transcribes YouTube videos by extracting audio and using OpenAI’s Whisper model for transcription. Paste a YouTube link and get the video’s audio transcribed into text.

<div align="center">   
<video
    src="assets/demo.m4v" loop autoplay muted playsinline></video>
</div>

## Requirements

- Conda installed (for managing environments)
- Python 3.9 or above
- **FFmpeg** installed (required for audio conversion)

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/danilotpnta/Youtube-Whisper.git
cd Youtube-Whisper
```

### Step 2: Install FFmpeg

You need FFmpeg for processing the audio. Install it based on your operating system:

- **macOS**: Install FFmpeg via Homebrew:
  ```bash
  brew install ffmpeg
  ```

- **Ubuntu/Linux**: Install FFmpeg via apt:
  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```

- **Windows**: 
  - Download FFmpeg from the official website: [FFmpeg Download](https://ffmpeg.org/download.html).
  - Extract the files and add the `bin` folder to your system’s PATH environment variable. For detailed instructions on adding FFmpeg to PATH, you can follow [this guide](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/).

Verify the installation by running:
```bash
ffmpeg -version
```

### Step 3: Create and Activate the Conda Environment

To set up the environment using the provided `environment.yml` file:

```bash
conda env create -f environment.yml
```

Once the environment is created, activate it with:

```bash
conda activate yt-whisper
```

### Step 4: Run the App

Once the environment is active, you can launch the Gradio app with:

```bash
python app.py
```

This will start a local server for the app, and you can access it by visiting the URL printed in the terminal (usually `http://localhost:7860/`).

### Troubleshooting

1. **FFmpeg Not Found**: 
   If you see an error related to `ffmpeg not found`, ensure FFmpeg is installed and added to your system's PATH. You can also specify its location manually in the script by setting `ffmpeg_location`.

2. **Pytube Errors**:
   If you encounter issues with `pytube`, ensure you’re using the `yt-dlp` version and that your URL is correctly formatted.

3. **Update Dependencies**:
   Ensure that `pip` and `conda` are up to date:
   ```bash
   conda update conda
   pip install --upgrade pip
   ```
