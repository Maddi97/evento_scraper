from playwright.async_api import async_playwright


async def scrape_with_js(url: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Try with headless=False
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            locale="en-US",
            java_script_enabled=True,
            ignore_https_errors=True,
        )
        page = await context.new_page()

        # Add a delay to simulate human behavior
        await page.goto(str(url), timeout=60000)
        await page.wait_for_timeout(5000)  # wait 5s

        html = await page.content()
        await browser.close()
        return html
