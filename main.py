import requests
from .saving import save_in_file


def main():
    url = "https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD"
    query_parameters = {"downloadformat": "csv"}
    
    print('Downloading file ...')
    response = get_response(url,query_parameters)
    if check_response(response):
        save_as = "Desktop/gdp_by_country2.zip"
        save_in_file(save_as,response)



def get_response(url, query_parameters):
    return requests.get(url, query_parameters)

def check_response(response):
    if response.status_code == 200:
        print('Downloaded successfully!')
        return True
    else:
        print(f'Failed to download the file. Status code: {response.status_code}')
        return False
    
main()

