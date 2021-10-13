import requests

params = {
    'collection': 'cryptopunks',
    'limit': 1
}

r = requests.get('https://api.opensea.io/api/v1/assets', params=params)

print(r.json())
