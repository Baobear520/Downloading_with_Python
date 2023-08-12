import os
from tqdm import tqdm

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