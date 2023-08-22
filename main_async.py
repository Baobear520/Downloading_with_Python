import os
import asyncio, logging
import aiohttp
from tqdm import tqdm
from config_logging import logger
from url_templates import urls



async def main():
    logger.info('Starting...')
    tasks = [download_file(url) for url in urls]
    await asyncio.gather(*tasks)
    logger.info('All files have been downloaded successfully!')


async def download_file(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if "content-disposition" in response.headers:
                header = response.headers["content-disposition"]
                filename = header.split("filename=")[1]
            else:
                filename = url.split("/")[-1]
            cwd = os.getcwd()
            file_path = os.path.join(cwd, 'downloads', filename)
            total_size = int(response.headers.get('content-length'),0)
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename,) as pbar:
                with open(file=file_path, mode="wb") as file:
                    while True:
                        chunk = await response.content.read()
                        if not chunk:
                            break
                        file.write(chunk)
                        pbar.update(len(chunk))

if __name__ == "__main__":
    asyncio.run(main())