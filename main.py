from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from playwright.async_api import async_playwright
from pathlib import Path
import os

app = FastAPI()

# 静的ファイルディレクトリを絶対パスで設定
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    index_path = STATIC_DIR / "index.html"
    if not index_path.is_file():
        raise HTTPException(status_code=404, detail="Index file not found")
    html = index_path.read_text(encoding="utf-8")
    return html

@app.post("/search")
async def execute_search(request: Request):
    data = await request.json()
    property_name = data.get("propertyName")
    if not property_name:
        raise HTTPException(status_code=400, detail="物件名を入力してください")

    SEARCH_URL = "https://www.e-mansion.co.jp/"
    SEARCH_INPUT = "#InputBox"
    SEARCH_BUTTON = "button.search-submit"
    RESULT_SELECTOR = ".search-results"

    # 環境変数HEADLESS_MODEが"true"ならheadlessモードを有効にする
    headless_mode = os.getenv("HEADLESS_MODE", "true").lower() == "true"

    browser = None
    context = None
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=headless_mode)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(SEARCH_URL)
            await page.fill(SEARCH_INPUT, property_name)
            await page.click(SEARCH_BUTTON)
            await page.wait_for_selector(RESULT_SELECTOR)
            result_html = await page.inner_html(RESULT_SELECTOR)
    except Exception as e:
        # 本番は詳細ログは控え、開発時のみ詳細返却（環境変数DEBUG_MODEで制御）
        debug_mode = os.getenv("DEBUG_MODE", "false").lower() == "true"
        detail = f"検索処理中にエラーが発生しました: {str(e)}" if debug_mode else "内部エラーが発生しました"
        raise HTTPException(status_code=500, detail=detail)
    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()

    # result_htmlには生のHTMLが含まれるため、XSS対策はクライアント側で実施推奨

    return {
        "status": "success",
        "propertyName": property_name,
        "resultHtml": result_html
    }
