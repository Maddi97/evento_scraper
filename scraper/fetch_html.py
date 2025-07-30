import requests

def fetch_html(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise error for bad responses (4xx/5xx)
    return response.text
