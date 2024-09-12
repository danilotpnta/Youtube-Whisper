# Youtube-Whisper
A simple Gradio app that transcribes YouTube videos by extracting audio and using OpenAI’s Whisper model for transcription. Paste a YouTube link and get the video’s audio transcribed into text.

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/danilotpnta/Youtube-Whisper.git
cd Youtube-Whisper
```

### Step 2: Create and Activate the Conda Environment

To set up the environment using the provided `environment.yml` file:

```bash
conda env create -f environment.yml
```

Once the environment is created, activate it with:

```bash
conda activate yt-whisper
```

### Step 3: Run the App

Once the environment is active, you can launch the Gradio app with:

```bash
python app.py
```

This will start a local server for the app, and you can access it by visiting the URL printed in the terminal (usually `http://localhost:7860/`).

### Troubleshooting

If you encounter any issues during installation, ensure that `pip` and `conda` are up to date:

```bash
conda update conda
pip install --upgrade pip
