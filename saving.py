import os

def extract_file_name(save_as):
    file_name,extention = os.path.splitext(os.path.basename(save_as))
    return file_name

def save_in_file(save_as,response):
    try:
        with open(save_as,mode='wb') as file:
            file.write(response.content)
            file_name = extract_file_name(save_as)
            print(f'Saved as {file_name} at {save_as}')
    except IOError as e:
        print(f'Error saving the file: {e}')