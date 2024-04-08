import sys
import os
from urllib.parse import urlparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import requests
from bs4 import BeautifulSoup
from utils.web_scraper_utils import scrape_from_link

url = "https://en.wikipedia.org/wiki/Java_(programming_language)"

def test_scrape_from_link_valid_url():
    data = scrape_from_link(url)
    print(data)

  

test_scrape_from_link_valid_url()
def test_scrape_from_link_invalid_url():
    invalid_url = "invalid_url"
    with pytest.raises(ValueError):
        scrape_from_link(invalid_url)

# def test_scrape_from_link_request_error(monkeypatch):
#     def mock_get(*args, **kwargs):
#         raise requests.exceptions.RequestException("Mock Request Exception")

#     monkeypatch.setattr(requests, "get", mock_get)

#     with pytest.raises(requests.exceptions.RequestException):
#         scrape_from_link([url])
