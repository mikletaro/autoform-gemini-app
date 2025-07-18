from fastapi import FastAPI, Request
import json
import google.generativeai as genai
import os

app = FastAPI()

# 環境変数からAPIキーを取得（Renderの環境変数設定にGEMINI_API_KEYを入れる）
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

# 入力データ読み込み
with open("data/user_data.json", "r", encoding="utf-8") as f:
    user_data = json.load(f)

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.post("/analyze-form")
async def analyze_form(request: Request):
    # フォームの各input/select情報を受け取る
    # （例: [{"name":"...","label":"...","type":"..."}, ...]）
    form_fields = await request.json()
    # ここでGeminiに「どのフィールドが何の項目か」を推論させる
    response = ask_gemini_to_guess_field_roles(form_fields, user_data)
    return response

def ask_gemini_to_guess_field_roles(fields, user_data):
    # Gemini用プロンプト生成
    prompt = f"""
    以下の各フォーム項目から、「氏名」「フリガナ」「メール」「電話番号」などの
    個人情報項目を特定し、jsonのどのキー欄に入力すべきか判定してください。
    入力可能なJSONキー一覧: {list(user_data.keys())}
    フォーム項目一覧: {json.dumps(fields, ensure_ascii=False)}
    返答例: {{"氏名に該当": "name", "メールに該当": "email", ...}}
    （該当なしはnull）
    """
    # Gemini API呼び出し（ここはGeminiの実際の呼び出しに書き換え）
    result = genai.generate_content(prompt)
    return result.text

@app.get("/user-data")
def get_user_data():
    return user_data
