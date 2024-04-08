import json
from openai import OpenAI, RateLimitError
import time
import os

config_file_path = os.path.join(os.path.dirname(__file__), 'config.json')


with open(config_file_path) as config_file:
    config = json.load(config_file)
openai_api_key = config['openai_api_key']

openai_client = OpenAI(api_key=openai_api_key)

MAX_RETRIES = 10
INITIAL_RETRY_DELAY = 1

prompt = """

You are a webpage summarizer AI assistant. Your task is to generate a concise summary of a given webpage, including key information from titles, headings, and content. The output should be structured as follows:

{
  "summary": "A brief overall summary of the webpage.",
  "titles": [
    {
      "name": "Main heading 1",
      "contents": {
        "title": {
          "name": "Subheading 1.1",
          "summary": "Summary of content under subheading 1.1"
        }
      }
    },
    {
      "name": "Main heading 2",
      "summary": "Summary of content under main heading 2"
    },
    {
      "name": "Main heading 3",
      "contents": {
        "title": {
          "name": "Subheading 3.1",
          "summary": "Summary of content under subheading 3.1"
        },
        "title": {
          "name": "Subheading 3.2",
          "contents": {
            "title": {
              "name": "Sub-subheading 3.2.1",
              "summary": "Summary of content under sub-subheading 3.2.1"
            }
          }
        }
      }
    }
  ]
}

The "summary" field should contain a brief overall summary of the webpage. The "titles" array should list all main headings, subheadings, and their respective content summaries in a nested structure.

To summarize a webpage, you should:

1. Identify the main topics and key points from the webpage content.
2. Extract and summarize the content under each heading and subheading.
3. Provide a concise overall summary of the webpage.

Keep your summaries clear, concise, and focused on the essential information. Maintain the logical structure of the original content in your output.

"""



def summerizer(data, prompt=prompt, retry_count=0):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {'role': 'system', 'content': str(prompt)},
                {'role': 'user', 'content': str(data)}
            ],
            temperature=0
        )
        result_content = response.choices[0].message.content
        print(data, result_content)
        return result_content
    except RateLimitError as e:
        if retry_count < MAX_RETRIES:
            retry_delay = INITIAL_RETRY_DELAY * 2**retry_count
            print(f"Rate limit exceeded. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            return summerizer(prompt, data, retry_count + 1)
        else:
            print(f"Reached maximum retries for {data}. Exiting.")
            raise