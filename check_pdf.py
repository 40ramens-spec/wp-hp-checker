import requests
import os

# --- 設定 ---
# あなたのサイトURLに書き換えてください
WP_API_URL = "https://www.jmdm.co.jp/wp-json/wp/v2/media?mime_type=application/pdf&per_page=1"
WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
ID_FILE = "last_id.txt"

def main():
    # 1. WordPressから最新1件を取得
    response = requests.get(WP_API_URL)
    
    # 正常に取得できたかチェック
    if response.status_code != 200:
        print(f"エラー: サイトにアクセスできません (Status: {response.status_code})")
        return

    try:
        res = response.json()
    except Exception:
        print("エラー: JSONデータが空か、形式が正しくありません。URLを確認してください。")
        return

    if not res:
        print("通知なし: PDFが1件も見つかりませんでした。")
        return
    
    # ...以下の処理はそのまま

if __name__ == "__main__":
    main()
