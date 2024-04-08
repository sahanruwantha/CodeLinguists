from utils.google_search import extract_https_links
from utils.web_scraper_utils import scrape_from_link
from InferenceAPI.utils.openai_summerizer import perform_openai_inference

# Example usage
def main():
    search_query = input("Enter your search query: ")
    search_results = extract_https_links(search_query)

    if search_results is not None:
        if search_results:
            for search_result in search_results:
                print(search_result)
            scraped_data = scrape_from_link(search_results[:1])
            scraped_data = perform_openai_inference(scraped_data)
            print(scraped_data)
            
        else:
            print("No HTTPS links found.")
    else:
        print("Failed to retrieve search results.")
    

if __name__ == "__main__":
    main()
