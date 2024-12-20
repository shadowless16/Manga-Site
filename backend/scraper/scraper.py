import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # Import MongoClient for MongoDB

# Connect to MongoDB (Replace with your MongoDB URI if hosted)
client = MongoClient('mongodb://localhost:27017/')
db = client['manga_db']  # Database
collection = db['images']  # Collection for storing image URLs

def store_images_in_db(images):
    """Store images in MongoDB."""
    for image in images:
        collection.update_one({'url': image}, {'$set': {'url': image}}, upsert=True)

def scrape_images_from_site(url):
    """Scrape images from a single manga site and store in DB."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    images = [
        img["data-src"].strip()
        for img in soup.select('div.page-break.no-gaps img[data-src]')
    ]
    store_images_in_db(images)  # Store the images in MongoDB
    return images

def scrape_manga_images():
    """Scrape images from multiple manga sites."""
    sites = {
        "Manga Site A": "https://toonclash.com/manga/the-celestial-returned-from-hell/chapter-188/",
        "Manga Site B": "https://toonclash.com/manga/wan-gu-shen-wang/chapter-446/",
        # Add more site URLs here
    }

    all_images = {}
    for site_name, url in sites.items():
        try:
            all_images[site_name] = scrape_images_from_site(url)
        except Exception as e:
            all_images[site_name] = f"Error: {e}"

    return all_images
