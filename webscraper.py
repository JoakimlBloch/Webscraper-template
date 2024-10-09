import requests
import bs4 as BeautifulSoup
import pandas as pd
import csv
from requests.exceptions import HTTPError, SSLError

# here you can define translations for specific letters or characters you might encounter on your websites you need to scrape
# as example here is a version of the Slovakian and Czech alphabet translated to english alphabet letters for easier scraping
char_translation = {
    "á": "a",
    "ý": "y",
    "ú": "u",
    "é": "e",
    "í": "i",
    "ž": "z",
    "š": "s",
    "ů": "u",
    "ó": "o",
    "ř": "r",
    "č": "c",
    "ň": "n",
    "ď": "d",
    "ĺ": "l",
    "ť": "t",
    "š": "s",
    "ú": "u"  
}

# function to clean website text and keywords
def clean(text):
    text = text.lower()

    for char in char_translation:
        text = text.replace(char, char_translation[char])

    return text

# list of keywords to scrape
keywords = [
    'here you would put your list of keywords you would scrape for on your list of websites'
]

# clean keywords list
clean_keywords = [clean(keyword) for keyword in keywords]

# function to clean website content and count keyword occurrences
def count_keywords_in_content(content, keywords):
    keyword_counts = {keyword: content.count(clean(keyword)) for keyword in keywords}
    return keyword_counts

def clean_and_count_website_content(url, keywords):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print(f"Status code: {response.status_code} for URL: {url}")
        soup = BeautifulSoup.BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        cleaned_text = clean(text)
        keyword_counts = count_keywords_in_content(cleaned_text, keywords)
        return keyword_counts
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} for URL: {url}")
        return {keyword: 0 for keyword in keywords}
    except SSLError as ssl_err:
        print(f"SSL error occurred: {ssl_err} for URL: {url}")
        return {keyword: 0 for keyword in keywords}
    except Exception as err:
        print(f"Other error occurred: {err} for URL: {url}")
        return {keyword: 0 for keyword in keywords}
    
def process_websites_from_csv(df, keywords):
    results = []
    for index, row in df.iterrows():
        url = row['url']
        print(f"Processing website: {url}")
        keyword_counts = clean_and_count_website_content(url, keywords)
        result = {'Website:': url}
        result.update(keyword_counts)
        results.append(result)
    return pd.DataFrame(results)

# load CSV or Excel file with website URLs
csv_websites = pd.read_csv("path_to_CSV_file")
excel_websites = pd.read_excel("path_to_excel_file")

# process websites and get keyword counts/results
csv_results = process_websites_from_csv(csv_websites, clean_keywords)
excel_results = process_websites_from_csv(excel_websites, clean_keywords)

# create output
def create_output(path_csv, path_excel, csv_results, excel_results):
    
    # write csv results in CSV file
    with open(path_csv, 'w', newline='') as file:
        writer = csv.writer(file)

        # write headers
        writer.writerow(['Website:'] + keywords)

        # write data
        for index, row in csv_results.iterrows():
            website = row['Website:']
            counts = [row[keyword] for keyword in clean_keywords]
            writer.writerow([website] + counts)

    # write excel results in CSV file
    with open(path_excel, 'w', newline='') as file:
        writer = csv.writer(file)

        # write headers
        writer.writerow(['Website:'] + keywords)

        # write data
        for index, row in excel_results.iterrows():
            website = row['Website:']
            counts = [row[keyword] for keyword in clean_keywords]
            writer.writerow([website] + counts)

if __name__ == "__main__":
    create_output("output_csv.csv", "output_excel.csv", csv_results, excel_results)

# Print output for done confirmation
print('Scraped websites and saved results in CSV file(s).')