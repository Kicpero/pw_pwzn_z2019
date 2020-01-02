import pathlib
import calendar
import csv
import requests
from typing import Optional, Union, List
from urllib.parse import urljoin
from json import JSONDecodeError
from tqdm.auto import tqdm

API_URL = 'https://www.metaweather.com/api/'


def get_city_data(
        woeid: int, year: int, month: int,
        path: Optional[Union[str, pathlib.Path]] = None,
        timeout: float = 5.
) -> (str, List[str]):
    days = calendar.monthrange(year, month)[1]

    if path is None:
        path = pathlib.Path.cwd()
    else:
        path = pathlib.Path(path)
    path /= f'{woeid}_{year}_{month:02d}'
    path.mkdir(parents=True, exist_ok=True)

    files = []
    for day in tqdm(range(1, days + 1)):
        day_str = f'{year}_{month:02d}_{day:02d}.csv'
        data = download_data(woeid, year, month, day, timeout)
        if data:
            with open(path / day_str, 'w') as _file:
                createFile = csv.DictWriter(_file, delimiter=',', quotechar='"', fieldnames=data[0].keys())
                createFile.writeheader()
                createFile.writerows(data)
            files.append(day_str)
    return str(path), files


def download_data(woeid, year, month, day, timeout):
    location_url = urljoin(API_URL, f'location/{woeid}/{year}/{month}/{day}')

    response = requests.get(location_url, timeout=timeout)
    if response.status_code >= 400:
        raise requests.exceptions.HTTPError

    try:
        data = response.json()
    except JSONDecodeError:
        raise RuntimeError
    return data


if __name__ == '__main__':
    _path = pathlib.Path.cwd()
    expected_path = _path / '523920_2017_03'
    dir_path, file_paths = get_city_data(523920, 2017, 3)
    assert len(file_paths) == 31
    assert pathlib.Path(dir_path).is_dir()
    assert str(expected_path) == dir_path

    expected_path = 'weather_data/523920_2017_03'
    dir_path, file_paths = get_city_data(523920, 2017, 3, path='weather_data')
    assert len(file_paths) == 31
    assert pathlib.Path(dir_path).is_dir()
    assert expected_path == dir_path

    expected_path = 'weather_data/523920_2012_12'
    dir_path, file_paths = get_city_data(523920, 2012, 12, path='weather_data')
    assert len(file_paths) == 0
    assert pathlib.Path(dir_path).is_dir()
    assert expected_path == dir_path
