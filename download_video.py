from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests

def download_mp3_selenium(youtube_url):
    # Set up the Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')  # Disable GPU to ensure it runs in cloud environments
    options.add_argument('--verbose')
    options.add_argument('--log-path=/tmp/chromedriver.log')

    driver = webdriver.Chrome(options=options)

    # Set up WebDriverWait (with a timeout of 10 seconds)
    wait = WebDriverWait(driver, 10)

    # Open the YouTube video page
    driver.get(youtube_url)
    # Wait for the title to be available
    wait.until(EC.title_contains("YouTube"))
    
    # Scrape the title
    title = driver.title  # This gives you the video title

    # Wait for the thumbnail to load and scrape it
    thumbnail_meta = wait.until(EC.presence_of_element_located((By.XPATH, "//meta[@property='og:image']")))
    thumbnail_url = thumbnail_meta.get_attribute('content')

    # Open the YouTube downloader site
    driver.get("https://yt1d.com/en/")
    # Wait until the page is loaded completely by checking an element presence
    wait.until(EC.presence_of_element_located((By.ID, "txt-url")))

    # Input the YouTube URL into the downloader
    input_box = driver.find_element(By.ID, "txt-url")
    input_box.send_keys(youtube_url)
    input_box.send_keys(Keys.RETURN)
    
    # Wait for the MP3 download button to appear
    mp3_download_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-ftype='mp3']")))
    onclick_attr = mp3_download_button.get_attribute("onclick")

    # Extract parameters from the JavaScript function call
    params = onclick_attr.split("'")
    if len(params) >= 7:
        mp3_download_url = params[1]  # Extracted base download URL

        # Wait for the final download URL to be available after JavaScript modifications
        final_link = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='googlevideo.com/videoplayback']")))
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

    with open('/tmp/chromedriver.log', 'r') as log_file:
        log_contents = log_file.read()
        print(log_contents)

    # Return the title and thumbnail for display
    return title, thumbnail_url

# Example usage:
# youtube_url = "https://youtu.be/MAZyQ-38b8M?si=q0dai-wF6FQz6MGN"
# title, thumbnail_url = download_mp3_selenium(youtube_url)
# print(f"Title: {title}")
# print(f"Thumbnail: {thumbnail_url}")