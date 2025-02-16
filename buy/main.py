import subprocess
import requests
import time
import json
import datetime
import logging
from gmgn_trending import fetch_trending_tokens, process_tokens

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Main function to run the trending token scanner.
    """
    logging.info("Starting trending token scanner...")
    while True:
        trending_data = fetch_trending_tokens()
        if trending_data:
            process_tokens(trending_data)
        else:
            logging.warning("Failed to fetch trending tokens. Retrying...")

        time.sleep(1) # Wait for 1 second before next API call


if __name__ == "__main__":
    main()