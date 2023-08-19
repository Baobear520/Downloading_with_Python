import requests, os
from saving import save_in_file
from tqdm import tqdm

def main():
    users_url = "https://databank.worldbank.org/data/download/WDI_CSV.zip"
    print('Downloading file ...')
    response =  get_response(url=users_url)
    if check_response(response):
        save_as = "WDI_CSV.zip"
        save_in_file(save_as,response)


def get_response(url):
    return requests.get(url,stream=True)

def check_response(response):
    if response.status_code == 200:
        return True
    else:
        print(f'Failed to download the file. Status code: {response.status_code}')


def extract_file_name(save_as):
    file_name,extention = os.path.splitext(os.path.basename(save_as))
    return file_name

def save_in_file(save_as,response):
    try:
        with open(save_as,mode='wb') as file,tqdm (
            desc=save_as, total=int(response.headers.get('content-length', 0)), 
            unit='B', unit_scale=True
    ) as bar:
            for chunk in response.iter_content(chunk_size=10 * 1024):
                bar.update(len(chunk))
                file.write(chunk)
        print('Downloaded successfully!')       
        file_name = extract_file_name(save_as)
        print(f'Saved as {file_name} at {save_as}')
    except IOError as e:
        print(f'Error saving the file: {e}')


if __name__ == '__main__':
    main()

