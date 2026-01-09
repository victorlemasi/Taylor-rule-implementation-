import requests

api_key = '70c9dbf5724a4cf:flttmrn6awqmk8e'

# Test Mexico data
print("Testing Mexico economic data:")
url = "https://api.tradingeconomics.com/country/mexico"
params = {"c": api_key}
response = requests.get(url, params=params)
print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    if data:
        print(f"Number of indicators: {len(data)}")
        # Find relevant indicators
        for item in data:
            if any(keyword in item.get('Category', '').lower() for keyword in ['inflation', 'cpi', 'unemployment', 'gdp']):
                print(f"\nCategory: {item.get('Category')}")
                print(f"  Latest Value: {item.get('LatestValue')}")
                print(f"  Previous Value: {item.get('PreviousValue')}")
                print(f"  Unit: {item.get('Unit')}")
    else:
        print("No data returned")
else:
    print(f"Error: {response.text}")
