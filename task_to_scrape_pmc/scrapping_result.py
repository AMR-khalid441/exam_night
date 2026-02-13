from playwright.sync_api import sync_playwright

def scrap_result(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle", timeout=30000)

        # Correct selector for the article title
        result_selector = "#main-content > article > section:nth-child(1) > section.front-matter > div > hgroup > h1"

        try:
            page.wait_for_selector(result_selector, timeout=10000)
            result_text = page.query_selector(result_selector).inner_text()
            print("Article Title:", result_text)
        except Exception as e:
            print("Error: Could not find the selector:", e)

        browser.close()

if __name__ == "__main__":
    scrap_result(url="https://pmc.ncbi.nlm.nih.gov/articles/PMC3126903")
