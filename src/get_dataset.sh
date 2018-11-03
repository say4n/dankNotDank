# Download dataset

echo "Scraping reddit ..."
python3 data/scraper.py

echo "Preprocessing data ..."
python3 data/preprocess.py

echo "Downloading memes ..."
python3 data/downloader.py
