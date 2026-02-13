from playwright.sync_api import sync_playwright

def scraping_all_results(links):
    for i in range(len(links)):
    

        pass
    # pd frame


def scrapping_all_links(url, pages=5):
    with sync_playwright() as P:
        browser = P.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(url, wait_until="domcontentloaded", timeout=30000)

        selector_results = "div.docsum-wrap a.docsum-link"
        selector_load_more = "button.more"

        page.wait_for_selector(selector_results)

        for i in range(pages):

            button = page.query_selector(selector_load_more)
            if not button:
                print("No more button found.")
                break

            # عدد النتائج قبل الضغط
            previous_count = len(page.query_selector_all(selector_results))

            button.click()

            # استنى لحد ما عدد النتائج يزيد
            page.wait_for_load_state(
               "networkidle"
            )

        # بعد ما خلصنا load more
        results = page.query_selector_all(selector_results)

        links = []
        for result in results:
            href = result.get_attribute("href")
            if href:
                full_link = "https://pmc.ncbi.nlm.nih.gov" + href
                links.append(full_link)

        browser.close()
        return links


if __name__ == "__main__":
    url = "https://pmc.ncbi.nlm.nih.gov/search/?term=mental+health"
    links = scrapping_all_links(url=url)
    

    for link in links:
        print(link)
