import os
import asyncio, logging
import aiohttp
from tqdm import tqdm


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

template_url = (
    "https://api.worldbank.org/v2/en/indicator/"
    "{resource}?downloadformat=csv"
)

urls = [
    # Total population by country
    template_url.format(resource="SP.POP.TOTL"),

    # GDP by country
    template_url.format(resource="NY.GDP.MKTP.CD"),

    # Population density by country
    template_url.format(resource="EN.POP.DNST"),
]

async def main():
    tasks = [download_file(url) for url in urls]
    await asyncio.gather(*tasks)
    logging.info('All files have been downloaded successfully!')


async def download_file(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if "content-disposition" in response.headers:
                header = response.headers["content-disposition"]
                filename = header.split("filename=")[1]
            else:
                filename = url.split("/")[-1]
            cwd = os.getcwd()
            total_size = int(response.headers.get('content-length'),0)
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename,) as pbar:
                with open(file=cwd +(f'/downloads/{filename}'), mode="wb") as file:
                    while True:
                        chunk = await response.content.read()
                        if not chunk:
                            break
                        file.write(chunk)
                        pbar.update(len(chunk))

if __name__ == "__main__":
    asyncio.run(main())