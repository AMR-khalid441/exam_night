from playwright.sync_api import sync_playwright


def testing_playwright(url, max_clicks=5):

    all_links = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()

        print("Opening first page...")
        page.goto(url, wait_until="networkidle", timeout=30000)

        # استنى أول نتائج تظهر
        results_selector = "div.docsum-wrap a.docsum-link"
        page.wait_for_selector(results_selector)

        for click_number in range(max_clicks):

            print(f"Clicking Show More {click_number + 1}")

            button = page.query_selector("button.more")
            if not button:
                print("No more button found, stopping.")
                break

            # احسب عدد النتائج قبل الضغط
            previous_count = len(page.query_selector_all(results_selector))

            button.click()

            # استنى لحد ما عدد النتائج يزيد
            page.wait_for_function(
                f"document.querySelectorAll('{results_selector}').length > {previous_count}"
            )

        # بعد ما خلصنا ضغط — نجيب كل اللينكات
        results = page.query_selector_all(results_selector)

        for result in results:
            href = result.get_attribute("href")
            if href:
                full_url = "https://pmc.ncbi.nlm.nih.gov" + href
                all_links.append(full_url)

        browser.close()

    return all_links


if __name__ == "__main__":
    url = "https://pmc.ncbi.nlm.nih.gov/search/?term=mental+health"
    links = testing_playwright(url=url, max_clicks=5)
    print(f"Collected {len(links)} links")
    print(links)
 