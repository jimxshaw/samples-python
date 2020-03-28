import requests

request = requests.get("https://api.exchangeratesapi.io/latest?symbols=USD")

print(request)
