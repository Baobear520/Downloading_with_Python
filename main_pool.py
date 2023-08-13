from concurrent.futures import ThreadPoolExecutor
import requests, logging
from url_template import urls
from tqdm import tqdm


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_file(url):
    try:
        response = requests.get(url)
        total_length = int(response.headers.get('content-length', 0))

        if "content-disposition" in response.headers:
            content_disposition = response.headers["content-disposition"]
            filename = content_disposition.split("filename=")[1]
        else:
            filename = url.split("/")[-1]

        with open(filename, mode="wb") as file,tqdm(
            desc=filename, total=total_length,
            unit='B', unit_scale=True
        ) as pbar:
            for chunk in response.iter_content(chunk_size=10 * 1024):
                pbar.update(len(chunk))
            file.write(chunk)
        logging.info(f"Downloaded file {filename}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download {url}: {e}")
    except Exception as e:
        logger.exception(f"An error occurred while downloading {url}: {e}")

# Main function to download these files concurrently using multiple threads of execution
def main():
    with ThreadPoolExecutor() as executor:
        executor.map(download_file, urls)

if __name__ == "__main__":
    main()