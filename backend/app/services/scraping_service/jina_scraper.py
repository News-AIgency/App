import requests
import validators
from validators import ValidationError

def check_url(url: str) -> bool:
    result = validators.url(url)
    
    if isinstance(result, ValidationError):
        return False
    
    return result

def jina_scrape(scrape_url: str) -> (str | None):
    if not check_url(scrape_url):
       raise ValueError('The argument is not a valid URL')
    
    url = f'https://r.jina.ai/{scrape_url}'
    headers = {
        'Authorization': 'Bearer jina_4bf764a7ecb14279909a0de3932925edzjw867nnXuzflFhXYoikwLJGL7eH',
        'X-Timeout': '5'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        raise Exception(status_code=500, detail=str(e))