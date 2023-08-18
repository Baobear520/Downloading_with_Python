from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import requests, logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Main function to download these files concurrently using multiple threads of execution
def main(urls: list):
    logging.info(f'Starting...')
    with ThreadPoolExecutor() as executor:
        executor.map(download_file, urls)
    logging.info(f'All files have been saved!')


def extract_file_names(url):
    with requests.get(url, stream=True) as response:
        if "content-disposition" in response.headers:
            content_disposition = response.headers["content-disposition"]
            filename = content_disposition.split("filename=")[1]
        else:
            filename = url.split("/")[-1]
    return response, filename


def download_file(url):
    response, filename = extract_file_names(url)
    if "content-disposition" in response.headers:
        content_disposition = response.headers["content-disposition"]
        filename = content_disposition.split("filename=")[1]
    else:
        filename = url.split("/")[-1]
    total_length = int(response.headers.get('content-length'),0)

    try:
        with open(filename, mode="wb") as file,tqdm(
            desc=filename, total=total_length,
            unit='B', unit_scale=True
        ) as pbar:
            for chunk in response.iter_content(chunk_size=10 * 1024):
                pbar.update(len(chunk))
                file.write(chunk)
        logging.info(f"Downloaded {filename} successfully!")

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download {url}: {e}")
    except Exception as e:
        logger.exception(f"An error occurred while downloading {url}: {e}")
    


if __name__ == "__main__":
    main()