from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from playwright.async_api import async_playwright
import json
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r", encoding="utf-8") as f:
        html = f.read()
    return html

@app.post("/search")
async def execute_search(request: Request):
    data = await request.json()
    property_name = data.get("propertyName")
    if not property_name:
        raise HTTPException(status_code=400, detail="物件名を入力してください")

    # 実際の検索サイトのURL・セレクタを入れてください
    SEARCH_URL = "https://www.e-mansion.co.jp/"
    SEARCH_INPUT = "#InputBox"
    SEARCH_BUTTON = "button[type='submit']"
    RESULT_SELECTOR = ".result-list"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(SEARCH_URL)
        await page.fill(SEARCH_INPUT, property_name)
        await page.click(SEARCH_BUTTON)
        await page.wait_for_selector(RESULT_SELECTOR)
        result_html = await page.inner_html(RESULT_SELECTOR)
        print("=== 検索結果HTML（抜粋） ===")
        print(result_html[:1000])
        await context.close()
        await browser.close()

    return {
        "status": "success",
        "propertyName": property_name,
        "resultHtml": result_html
    }
