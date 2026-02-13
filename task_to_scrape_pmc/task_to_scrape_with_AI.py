from playwright.sync_api import sync_playwright
import pandas as pd

BASE_URL = "https://pmc.ncbi.nlm.nih.gov"

def scrapping_all_links(url, pages=5):
    all_links = []

    with sync_playwright() as P:
        browser = P.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=30000)

        selector_results = "div.docsum-wrap a.docsum-link"
        selector_load_more = "button.more"

        page.wait_for_selector(selector_results)

        for _ in range(pages):
            button = page.query_selector(selector_load_more)
            if not button:
                print("No more 'Show More' button found.")
                break

            button.click()
            page.wait_for_timeout(2000)

        results = page.query_selector_all(selector_results)
        for result in results:
            href = result.get_attribute("href")
            if href:
                if href.startswith("http"):
                    full_link = href
                else:
                    full_link = BASE_URL + href
                all_links.append(full_link)

        browser.close()

    return all_links


def scraping_all_results(links):
    articles_data = []

    with sync_playwright() as P:
        browser = P.chromium.launch(headless=False)
        page = browser.new_page()

        for idx, link in enumerate(links):
            print(f"Scraping article {idx+1}/{len(links)}: {link}")
            try:
                page.goto(link, wait_until="domcontentloaded", timeout=30000)

                results_selector = "#main-content > article > section:nth-child(1) > section.front-matter > div > hgroup > h1"
                page.wait_for_selector(results_selector, timeout=5000)
                result_elem = page.query_selector(results_selector)

                result_text = result_elem.inner_text() if result_elem else ""

                articles_data.append({
                    "url": link,
                    "result": result_text
                })

            except Exception as e:
                print(f"Error scraping {link}: {e}")
                continue

        browser.close()

    return articles_data


if __name__ == "__main__":
    url = "https://pmc.ncbi.nlm.nih.gov/search/?term=mental+health"

    links = scrapping_all_links(url=url, pages=3)
    print(f"Collected {len(links)} links")

    data = scraping_all_results(links)

    df = pd.DataFrame(data)
    df.to_csv("articles.csv", index=False)

    print("Saved to articles.csv")
