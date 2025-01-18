from io import BytesIO
from bs4 import BeautifulSoup
import requests
import logging
from urllib.parse import urljoin
import app as Suleiman 

# Configure logging
logging.basicConfig(
    filename="image_scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def execute(message):
    """
    Scrapes images from Bing based on the search term and returns the first 5 images as BytesIO objects.
    
    :param search_term: Search term to fetch images.
    :return: List of dictionaries containing success status and image data or error message.
    """
    if not message.strip():
        return [{"success": False, "data": "❌ Please provide a valid search term."}]

    url = f"https://www.bing.com/images/search?q={message}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    logging.info(f"Fetching URL: {url}")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch webpage: {e}")
        return [{"success": False, "data": f"🚨 Failed to fetch webpage: {str(e)}"}]
    
    soup = BeautifulSoup(response.content, 'html.parser')
    image_tags = soup.find_all('img', class_=['mimg', 'rms_img', 'vimgld'])
    if not image_tags:
        return [{"success": False, "data": "🚨 No images found for the search term."}]

    images = []
    for i, img_tag in enumerate(image_tags[9:14]):  # Fetch the first 5 images
        src = img_tag.get('src') or img_tag.get('data-src')
        if not src:
            continue
        src = urljoin("https://www.bing.com", src)

        try:
            img_response = requests.get(src, headers=headers)
            img_response.raise_for_status()
            image_data = BytesIO(img_response.content)
            images.append({"success": True, "data": image_data})
            logging.info(f"Image {i + 1} fetched successfully from: {src}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch image {i + 1} from {src}: {e}")
            images.append({"success": False, "data": f"🚨 Failed to fetch image {i + 1}: {str(e)}"})
            response = Suleiman.upload_image_to_graph(images)
                        Suleiman.send_message(sender_id, response)
    
