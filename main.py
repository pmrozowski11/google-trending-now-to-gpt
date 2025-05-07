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
            context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36")
            page = await context.new_page()
            await page.goto("https://trends.google.com/trending?geo=PL&category=6", timeout=60000)
            
            # Poczekaj na jakikolwiek tekst z trendów
            await page.wait_for_selector("div.feed-item span.title", timeout=60000)

            items = await page.query_selector_all("div.feed-item")
            trendy = []
            for item in items[:10]:
                title_el = await item.query_selector("span.title")
                if title_el:
                    title = await title_el.inner_text()
                    trendy.append(title.strip())
            await browser.close()
            return {"trendy": trendy}
    except Exception as e:
        return {"error": str(e)}

