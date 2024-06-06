import os
import requests
import concurrent.futures 
from datetime import datetime, timedelta

API_KEY = "APIKEY"
APOD_ENDPOINT = 'https://api.nasa.gov/planetary/apod'
OUTPUT_IMAGES = './output'

def get_apod_metadata(start_date: str, end_date: str, api_key: str) -> list:
    url = f"{APOD_ENDPOINT}?api_key={api_key}&start_date={start_date}&end_date={end_date}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def download_image(url: str, path: str):
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as f:
        f.write(response.content)

def download_apod_images(metadata: list):
    if not os.path.exists(OUTPUT_IMAGES):
        os.makedirs(OUTPUT_IMAGES)

    with concurrent.futures.ThreadPoolExecutor() as ex:
        futures = []
        for item in metadata:
            if item['media_type'] == 'image':
                img_url = item['url']
                img_date = item['date']
                img_extension = os.path.splitext(img_url)[1]
                img_path = os.path.join(OUTPUT_IMAGES, f"{img_date}{img_extension}")
                futures.append(ex.submit(download_image, img_url, img_path))
                
        for future in futures:
            future.result()

def main():
    metadata = get_apod_metadata(
        start_date='2021-08-01',
        end_date='2021-09-30',
        api_key=API_KEY,
    )
    download_apod_images(metadata=metadata)

if __name__ == '__main__':
    main()