from fastapi import FastAPI

app = FastAPI()

@app.post("/search")
async def execute_search(request: Request):
    data = await request.json()
    property_name = data.get("propertyName")
    if not property_name:
        raise HTTPException(status_code=400, detail="物件名を入力してください")

    SEARCH_URL = "https://www.e-mansion.co.jp/"
    SEARCH_INPUT = "#InputBox"
    SEARCH_BUTTON = "button.search-submit"
    # 検索結果ページの主要エリア（実際の検索結果に合わせて要修正）
    RESULT_SELECTOR = ".search-results"

    # 本番環境（Render等）ではheadless=True必須、開発時はFalseで動作確認
    headless_mode = False

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless_mode)
        context = await browser.new_context()
        page = await context.new_page()
        try:
            await page.goto(SEARCH_URL)
            await page.fill(SEARCH_INPUT, property_name)
            await page.click(SEARCH_BUTTON)
            # 検索結果が表示されるまで待機（セレクタは実際の検索結果エリアに合わせる）
            await page.wait_for_selector(RESULT_SELECTOR)
            result_html = await page.inner_html(RESULT_SELECTOR)
            print("=== 検索結果HTML（抜粋） ===")
            print(result_html[:1000])
        except Exception as e:
            await context.close()
            await browser.close()
            raise HTTPException(status_code=500, detail=f"検索処理中にエラーが発生しました: {str(e)}")
        await context.close()
        await browser.close()

    return {
        "status": "success",
        "propertyName": property_name,
        "resultHtml": result_html
    }
