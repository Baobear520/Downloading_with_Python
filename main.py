import requests
from saving import save_in_file


def main():
    users_url = "https://databank.worldbank.org/data/download/WDI_CSV.zip"
    #query_parameters = {"downloadformat": "csv"}
    
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
    
main()

