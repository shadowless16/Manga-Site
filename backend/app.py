from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS module
from scraper.scraper import scrape_manga_images  # Import the scraper function

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

@app.route('/')
def home():
    return "Welcome to the Manga Scraper API!"

@app.route('/api/manga', methods=['GET'])
def manga_images_endpoint():
    try:
        manga_images = scrape_manga_images()  # Call the scraper function
        return jsonify(manga_images)         # Return JSON response
    except Exception as e:
        return jsonify({"error": f"Failed to scrape images. Error: {e}"}), 500

@app.route('/test')
def test_route():
    return "Test route is working!"

if __name__ == '__main__':
    app.run(debug=True)
