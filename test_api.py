import requests

api_key = '70c9dbf5724a4cf:flttmrn6awqmk8e'
url = f'https://api.tradingeconomics.com/calendar?c={api_key}'
data = requests.get(url).json()
print(data)
