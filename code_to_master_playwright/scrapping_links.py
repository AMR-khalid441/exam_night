
from playwright.sync_api import sync_playwright, Playwright
from bs4 import BeautifulSoup


# qeury selector .
# get html
# get text
# get link
# so we go to specific selector wait for  it ,then query it
# after quering a selector we usually get_attribute to find the link
# or get_html()
# get text()
# get specific link from specific selector

from playwright.sync_api import sync_playwright, Playwright
from bs4 import BeautifulSoup


# qeury selector .
# get html
# get text
# get link
# so we go to specific selector wait for  it ,then query it
# after quering a selector we usually get_attribute to find the link
# or get_html()
# get text()
# get specific link from specific selector
def testing_playwright(url, max_pages=50):

    all_links = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()

        for page_number in range(1, max_pages + 1):

            paginated_url = f"{url}&page={page_number}"
            print(f"Scraping page {page_number}")

            page.goto(paginated_url, wait_until="networkidle", timeout=30000)
            

            selector = "div.docsum-wrap a.docsum-link"
            page.wait_for_selector(selector)

            results = page.query_selector_all(selector)

            for result in results:
                href = result.get_attribute("href")
                if href:
                    full_url = "https://pmc.ncbi.nlm.nih.gov" + href
                    all_links.append(full_url)

        browser.close()

    return all_links








if __name__ =="__main__":
    url="https://pmc.ncbi.nlm.nih.gov/search/?term=mental+health"
    print(testing_playwright(url=url))
    pass