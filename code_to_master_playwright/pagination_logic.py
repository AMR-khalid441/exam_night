from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://pmc.ncbi.nlm.nih.gov/search/?term=mental+health")

    # استنى الزرار يظهر
    page.wait_for_selector("button.more")
    

    # دوس عليه
    page.click("button.more")

    page.wait_for_timeout(3000)  # بس عشان تشوف النتيجة قدامك

    browser.close()
