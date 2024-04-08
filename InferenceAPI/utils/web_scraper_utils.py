import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def scrape_from_link(link):
    try:
        parsed_url = urlparse(link)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError(f"Invalid URL: {link}")

        response = requests.get(link)
        response.raise_for_status()  

        soup = BeautifulSoup(response.text, 'html.parser')

        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()

        def process_tag(tag):
            tag_data = {
                'name': tag.name,
                'text': tag.get_text(strip=True),  
                'children': []
            }

            if tag.name and hasattr(tag, 'children'):
                tag_data['children'] = [process_tag(child) for child in tag.children if hasattr(child, 'name')]

            return tag_data

        data = process_tag(soup)

        return data

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending the request: {e}")
    except ValueError as e:
        print(f"Invalid input: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    