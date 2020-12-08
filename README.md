# bookCrawler
Crawls through pages of Oxford University's library list and scrapes book data for collection

## Technologies
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [Selenium](https://selenium-python.readthedocs.io/installation.html)

## Local Setup 
1. Install all dependencies 

`pip install selenium`

`pip install beautifulsoup4`

2. Insert executable file path (chrome_path)

`chrome_path = " "` 

3. Create folders to store Json files
- title_to_urls
- book_data

4. Run the script
`python3 crawler.py`

