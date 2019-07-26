import json
import sys
import time
import re

from flask.json import jsonify
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()

# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--window-size=1366x768")
# chrome_options.add_argument("--no-sandbox")

second_search = []
text_to_be_returned = {
    "first_search": [[], []],
    "second_search": [[], []]
}
urls = []

browser = webdriver.Chrome(ChromeDriverManager().install(), 0, chrome_options)


def main():

    search_term = 'where to buy a car'

    # clean arrays before starting so same results aren't returned

    text_to_be_returned["first_search"][0].clear()
    text_to_be_returned["first_search"][1].clear()

    text_to_be_returned["second_search"][0].clear()
    text_to_be_returned["second_search"][1].clear()

    second_search.clear()

    # populate the array for the next search results
    start_scraper(search_term)

    for j in range(len(second_search)):
        search_term = second_search[j]
        start_scraper(search_term)

    scraped_results = format_results()

    return scraped_results


def start_scraper(search_term):

    browser.get('https://www.google.com/search?q=' + search_term)
    time.sleep(3)
    questions = browser.find_elements_by_class_name('related-question-pair')

    for i in questions[:4]:  # only take the first 4

        second_search.append(i.text)
        text_to_be_returned["questions"][0].append(i.text)

        i.click()
        time.sleep(1)

        more = i.find_element_by_class_name('gy6Qzb').text

        try:
            url = re.findall(r'(https?://[^\s]+)', more)[0]
            more = more.replace(url, '')
        except Exception:
            url = re.findall(r'(https?://[^\s]+)', more)

        urls.append(url)
        text_to_be_returned["questions"][1].append(more)


def format_results():

    text_minus_escapes = [w.replace('\n', ' ')
                          for w in text_to_be_returned["questions"][1]]

    dictionary = dict(
        zip(text_to_be_returned["questions"][0], zip(text_minus_escapes, urls)))
    with open('result.json', 'w') as fp:
        json.dump(dictionary, fp)

    return dictionary


if __name__ == '__main__':
    main()
