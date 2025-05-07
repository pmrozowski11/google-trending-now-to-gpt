from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from playwright.async_api import async_playwright

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

@app.get("/trendy")
async def get_trends():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto("https://trends.google.com/trending?geo=PL&category=6", timeout=60000)
            await page.wait_for_selector("div.feed-item")  # główne bloki z tematami
            items = await page.query_selector_all("div.feed-item")
            trendy = []
            for item in items[:10]:  # pobierz tylko top 10
                title_el = await item.query_selector("div.details-top span.title")
                if title_el:
                    title = await title_el.inner_text()
                    trendy.append(title)
            await browser.close()
            return {"trendy": trendy}
    except Exception as e:
        return {"error": str(e)}
