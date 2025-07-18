from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from playwright.sync_api import sync_playwright
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
    # フロントからの入力を取得
    data = await request.json()
    property_name = data.get("propertyName")
    if not property_name:
        raise HTTPException(status_code=400, detail="物件名を入力してください")

    # ここに実際の検索サイトURL・セレクタを設定
    SEARCH_URL = "https://example.com/search"  # ←実際の検索ページURLに変更
    SEARCH_INPUT = 'input[name="q"]'
    SEARCH_BUTTON = 'button[type="submit"]'
    RESULT_SELECTOR = ".result-list"  # 検索結果が表示されるセレクタ

    # Playwrightで検索実行（ヘッドフルモードで画面表示）
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # ←ユーザーに見える形で起動
        context = browser.new_context()
        page = context.new_page()
        page.goto(SEARCH_URL)
        # 検索ボックスに物件名を入力
        page.fill(SEARCH_INPUT, property_name)
        # 検索ボタンクリック
        page.click(SEARCH_BUTTON)
        # 検索結果が表示されるまで待機
        page.wait_for_selector(RESULT_SELECTOR)
        # 検索結果のHTMLを取得（次のステップでスレッドリンク抽出用）
        result_html = page.inner_html(RESULT_SELECTOR)
        context.close()
        browser.close()

    return {
        "status": "success",
        "propertyName": property_name,
        "resultHtml": result_html  # ←次のステップでスレッドリンク抽出用
    }
