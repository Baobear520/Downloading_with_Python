import requests, os
from tqdm import tqdm
from styles import color_info_message, color_error_message

def main():
    users_url = "https://databank.worldbank.org/data/download/WDI_CSV.zip"
    color_info_message('Downloading file ...')
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
        color_error_message(f'Failed to download the file. Status code: {response.status_code}')


def extract_file_name(save_as):
    file_name,extention = os.path.splitext(os.path.basename(save_as))
    return file_name

def save_in_file(save_as,response):
    cwd = os.getcwd()
    try:
        with open(file=cwd + (f'/downloads/{save_as}'),mode='wb') as file,tqdm (
            desc=save_as, total=int(response.headers.get('content-length', 0)), 
            unit='B', unit_scale=True
    ) as bar:
            for chunk in response.iter_content(chunk_size=10 * 1024):
                bar.update(len(chunk))
                file.write(chunk)
        color_output_message('Downloaded successfully!')       
        file_name = extract_file_name(save_as)
        color_output_message(f'Saved as {file_name} at {os.path.abspath(save_as)}')
    except IOError as e:
        color_error_message(f'Error saving the file: {e}')


if __name__ == '__main__':
    main()

