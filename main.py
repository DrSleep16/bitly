import requests
import argparse
import os


def shorten_link(url, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }

    long_url = {
        "long_url": url
    }
    response = requests.post('https://api-ssl.bitly.com/v4/bitlinks', headers=headers, json=long_url)
    response.raise_for_status()
    return response.json()['id']


def get_clicks_count(bitlink, token):
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'

    headers = {
        'Authorization': f'Bearer {token}'
    }

    params = {
        'unit': 'day',
        'units': -1,
    }

    response = requests.get(api_url, headers=headers, params=params)
    response.raise_for_status()
    response_data = response.json()
    clicks_count = response_data.get('total_clicks')
    return clicks_count


def is_bitlink(bitlink, token):
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(api_url, headers=headers)
    return response.ok


if __name__ == '__main__':
    token = os.getenv('BITLY_TOKEN')
    parser = argparse.ArgumentParser()
    parser.add_argument('urls', nargs='+')
    args = parser.parse_args()

    for url in args.urls:
        if is_bitlink(url, token):
            print(f'Количество переходов по ссылке битли "{url}": {get_clicks_count(url, token)}')
        else:
            print(shorten_link(url, token))
