import yt_dlp as youtube_dl
import requests

def download_mp3_yt_dlp(youtube_url):
    # Set up yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloaded_video.%(ext)s',
        'quiet': False,
        'no_warnings': True,
        'progress_hooks': [lambda d: print(f"Downloading {d['filename']}: {d['_percent_str']}")],
    }

    # Extract video info including title and thumbnail
    with youtube_dl.YoutubeDL() as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        title = info_dict.get('title', 'Unknown Title')
        thumbnail_url = info_dict.get('thumbnail', None)

    # Download the MP3 using yt-dlp
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    # Fetch the thumbnail for display
    if thumbnail_url:
        response = requests.get(thumbnail_url)
        if response.status_code == 200:
            with open('thumbnail.jpg', 'wb') as f:
                f.write(response.content)
            print(f"Thumbnail downloaded successfully.")
        else:
            print(f"Failed to download thumbnail. HTTP Status Code: {response.status_code}")

    # Return the title and thumbnail URL
    return title, thumbnail_url

# Example usage:
# youtube_url = "https://youtu.be/MAZyQ-38b8M?si=q0dai-wF6FQz6MGN"
# title, thumbnail_url = download_mp3_yt_dlp(youtube_url)
# print(f"Title: {title}")
# print(f"Thumbnail: {thumbnail_url}")
