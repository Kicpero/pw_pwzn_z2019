import requests
from urllib.parse import urljoin
from json import JSONDecodeError


def get_cities_woeid(query: str, timeout: float = 5.):
    API_URL = 'https://www.metaweather.com/api/'
    location_url = urljoin(API_URL, 'location/search')
    response = requests.get(location_url, params=dict(query=query), timeout=timeout)
    response_dict = {}
    if response.status_code >= 400:
        raise requests.exceptions.HTTPError

    try:
        cities_list = response.json()
    except JSONDecodeError:
        raise RuntimeError

    for city in cities_list:
        response_dict[city['title']] = city['woeid']
    return response_dict


if __name__ == '__main__':
    assert get_cities_woeid('Warszawa') == {}
    assert get_cities_woeid('War') == {
        'Warsaw': 523920,
        'Newark': 2459269,
    }
    try:
        get_cities_woeid('Warszawa', 0.1)
    except Exception as exc:
        isinstance(exc, requests.exceptions.Timeout)
