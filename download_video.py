from playwright.async_api import async_playwright

async def download_mp3_playwright(youtube_url):
    async with async_playwright() as p:
        # Launch browser in headless mode
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
        page = await browser.new_page()

        # Open the YouTube video page
        await page.goto(youtube_url)

        # Scrape the title
        title = await page.title()  # This gives you the video title

        # Scrape the thumbnail (YouTube page has a meta tag for the thumbnail)
        thumbnail_url = await page.get_attribute('meta[property="og:image"]', 'content')

        # Open the YouTube downloader site
        await page.goto("https://yt1d.com/en/")

        # Input the YouTube URL into the downloader
        await page.fill("input#txt-url", youtube_url)
        await page.press("input#txt-url", "Enter")  # Simulate pressing enter

        # Wait for the MP3 download button to appear
        await page.wait_for_selector("button[data-ftype='mp3']")

        # Extract the download URL for the MP3
        download_button = await page.query_selector("button[data-ftype='mp3']")
        onclick_attr = await download_button.get_attribute("onclick")

        # Extract parameters from the JavaScript function call
        params = onclick_attr.split("'")
        if len(params) >= 7:
            mp3_download_url = params[1]  # Extracted base download URL

            # Wait for the JavaScript to modify the link
            await page.wait_for_function(
                """() => document.querySelector('a[href*="googlevideo.com/videoplayback"]')"""
            )

            # Get the final download URL after JavaScript modifications
            final_link = await page.query_selector("a[href*='googlevideo.com/videoplayback']")
            mp3_download_url = await final_link.get_attribute("href")
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
        await browser.close()

        # Return the title and thumbnail for display
        return title, thumbnail_url