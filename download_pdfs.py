import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_pdfs_from_website(url, download_folder):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    pdf_links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]

    for link in pdf_links:
        file_name = os.path.join(download_folder, link.split("/")[-1])
        with requests.get(link, stream=True) as r:
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded: {file_name}")

# Example usage
website_url = 'https://www.zaft.htw-dresden.de/grundbau/loesungen.html'  # Replace with the target website URL
output_folder = './pdfs'  # Replace with the desired download folder
download_pdfs_from_website(website_url, output_folder)
