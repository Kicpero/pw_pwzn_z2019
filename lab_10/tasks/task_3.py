import filecmp
import pathlib
from typing import Union
import pandas as pd

API_URL = 'https://www.metaweather.com/api/'


def concat_data(
        path: Union[str, pathlib.Path],
):
    if not isinstance(path, pathlib.Path):
        path = pathlib.Path(path)

    all_data = []

    for file in path.iterdir():
        data = pd.read_csv(file)
        day_data = pd.to_datetime(data['created']).dt.date == pd.to_datetime(data['applicable_date']).dt.date
        all_data.append(data[day_data])

    all_data = pd.concat(all_data)

    save = pd.DataFrame(all_data,
                        columns=['created', 'min_temp', 'the_temp', 'max_temp',
                                 'air_pressure', 'humidity', 'visibility',
                                 'wind_direction_compass', 'wind_direction',
                                 'wind_speed'])
    save.rename({'the_temp': 'temp'}, inplace=True, axis='columns')
    save['created'] = save['created'].apply(lambda x: x[:16])
    save.sort_values('created', inplace=True)
    save.to_csv(f'{path}.csv', index=False)


if __name__ == '__main__':
    concat_data('weather_data/523920_2017_03')
    assert filecmp.cmp(
        'expected_523920_2017_03.csv',
        'weather_data/523920_2017_03.csv'
    )
