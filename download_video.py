from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import time

def download_mp3_selenium(youtube_url):
    # Set up the Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    # Open the YouTube video page
    driver.get(youtube_url)
    time.sleep(2)  # Wait for the page to load

    # Scrape the title
    title = driver.title  # This gives you the video title

    # Scrape the thumbnail (YouTube page has a meta tag for the thumbnail)
    thumbnail_meta = driver.find_element(By.XPATH, "//meta[@property='og:image']")
    thumbnail_url = thumbnail_meta.get_attribute('content')

    # Open the YouTube downloader site
    driver.get("https://yt1d.com/en/")
    time.sleep(2)  # Wait for the page to load

    # Input the YouTube URL into the downloader
    input_box = driver.find_element(By.ID, "txt-url")
    input_box.send_keys(youtube_url)
    input_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Wait for the download options to load

    # Wait for the MP3 download button to appear
    mp3_download_button = driver.find_element(By.CSS_SELECTOR, "button[data-ftype='mp3']")
    onclick_attr = mp3_download_button.get_attribute("onclick")

    # Extract parameters from the JavaScript function call
    params = onclick_attr.split("'")
    if len(params) >= 7:
        mp3_download_url = params[1]  # Extracted base download URL

        # Wait for the JavaScript to modify the link
        time.sleep(2)  # Allow time for the page to modify the link

        # Get the final download URL after JavaScript modifications
        final_link = driver.find_element(By.CSS_SELECTOR, "a[href*='googlevideo.com/videoplayback']")
        mp3_download_url = final_link.get_attribute("href")
        print(f"Final MP3 Download URL: {mp3_download_url}")

        response = requests.get(mp3_download_url, stream=True)

        # Check if the request was successful
        if response.status_code == 200:
            # Write the video content to a file
            output_file = "downloaded_video.mp4"
            with open(output_file, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print(f"Video downloaded successfully as {output_file}")
        else:
            print(f"Failed to download video. HTTP Status Code: {response.status_code}")

    else:
        print("Failed to extract MP3 download link from the page.")

    # Close the browser
    driver.quit()

    # Return the title and thumbnail for display
    return title, thumbnail_url

# Example usage:
# youtube_url = "https://youtu.be/MAZyQ-38b8M?si=q0dai-wF6FQz6MGN"
# title, thumbnail_url = download_mp3_selenium(youtube_url)
# print(f"Title: {title}")
# print(f"Thumbnail: {thumbnail_url}")