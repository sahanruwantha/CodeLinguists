from googlesearch import search
from requests.exceptions import RequestException


def extract_https_links(query):
    https_links = []

    try:
        for url in search(query):
            if url.startswith('https://'):
                https_links.append(url)
    except RequestException as e:
        print(f"An error occurred: {e}")
        return None

    return https_links



