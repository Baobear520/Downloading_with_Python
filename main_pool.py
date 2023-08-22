import requests
import os 
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

from config_logging import logger
from url_templates import urls


def main():
    logger.info('Starting...')
    with ThreadPoolExecutor() as executor:
        executor.map(download_file, urls)
    logger.info('All files have been saved!')


def download_file(url):
    response = requests.get(url, stream=True)
    if "content-disposition" in response.headers:
        content_disposition = response.headers["content-disposition"]
        filename = content_disposition.split("filename=")[1]
    else:
        filename = url.split("/")[-1]
    total_length = int(response.headers.get('content-length'))
    cwd = os.getcwd()
    file_path = os.path.join(cwd, 'downloads', filename)
    try:
        with open(file=file_path, mode="wb") as file:
            with tqdm(desc=filename, total=total_length,
                unit='B', unit_scale=True) as pbar:
                for chunk in response.iter_content(chunk_size=10 * 1024):
                    pbar.update(len(chunk))
                    file.write(chunk)
        logger.info(f"Downloaded {filename} successfully!")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download {url}: {e}")
    except Exception as e:
        logger.exception(f"An error occurred while downloading {url}: {e}")

if __name__ == "__main__":
    main()





