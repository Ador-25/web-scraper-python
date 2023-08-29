import requests
from bs4 import BeautifulSoup


def print_webpage_contents(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract and print the visible text content
        visible_text = soup.get_text()
        print(visible_text.strip())

    except requests.exceptions.RequestException as e:
        print("Error:", e)

# Example usage
url = "http://www.northsouth.edu/"  # Replace with the desired URL
print_webpage_contents(url)
