# Scraping Medium Articles

## Code Description
This is a Python script that performs web scraping of Medium articles related to different topics (tokens). It uses the Selenium library to interact with a web browser, the BeautifulSoup library to parse the HTML of web pages, and the re (regular expressions) library to manipulate strings. The code runs in "headless" mode, which means it doesn't display a graphical browser interface during execution.

## Required Libraries

To run the code, you need to have the following Python libraries installed:

- `selenium`: Used for automating interaction with the browser.
- `beautifulsoup4`: Used for parsing HTML web pages.
- `re`: Used for working with regular expressions.
- `json`: Used for reading and writing data in JSON format.
- `unicodedata`: Used for working with Unicode characters.
- 
## Installation

Before running the project, make sure you have the required libraries installed. You can install the libraries using the following command:

```bash
pip install selenium
pip install beautifulsoup4
pip install json
pip install unicodedata
pip install re
pip install time
```

## JSON Structure

The collected data is stored in JSON files with the following structure:
```json
{
    "token": "token_name",
    "link": "article_url",
    "title": "article_title",
    "subtitle": "article_subtitle",
    "autorName": "author_name",
    "imageAutor": "author_image_url",
    "clap": "number_of_claps",
    "response": "number_of_responses",
    "timeForRead": "reading_time",
    "dateCreate": "creation_date",
    "text": ["article_content_in_paragraphs"],
    "tagsPost": ["tags_associated_with_article"]
}
```

## Code Operation
The code begins by defining a list of tokens (topics) related to Medium articles. It then goes through these tokens and performs the following steps:

1. Accesses the profile page for a specific token on Medium and collects links to related articles.
2. For each collected article link, the code scrapes information about the article, such as title, author, number of claps, etc.
3. The article information is stored in a JSON-formatted dictionary.
4. All information is written to a JSON file corresponding to the token.
5. This way, the code allows you to collect information about Medium articles related to different topics and store this information in JSON files for later analysis or processing.
