# フォームAI自動入力Webアプリ

## 概要
AI（Gemini）でフォーム各項目の意味を自動判別し、固定の入力値を自動でセットするWebアプリです。

## 使い方
1. Render.comにデプロイ
2. APIを叩く（例: POST /analyze-form）
3. 入力対象フォームのHTMLやフィールド情報を送信
4. AIが「どこに何を入力すべきか」をJSONで返す
5. その通りに入力（またはJSスニペット生成）

## 環境変数
- `GEMINI_API_KEY`: Google Gemini APIキー

## 作者
nomura
