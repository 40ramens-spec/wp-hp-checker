import requests
import os

# --- 設定 ---
# あなたのサイトURLに書き換えてください
WP_API_URL = "https://www.jmdm.co.jp/wp-json/wp/v2/media?mime_type=application/pdf&per_page=1&orderby=date&order=desc"
WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
ID_FILE = "last_id.txt"

def main():
    # 1. WordPressから最新1件を取得
    res = requests.get(WP_API_URL).json()
    if not res: return
    
    item = res[0]
    curr_id = str(item['id'])
    pdf_url = item['source_url']
    pdf_title = item['title']['rendered']

    # 2. 前回のIDを読み込み
    last_id = ""
    if os.path.exists(ID_FILE):
        with open(ID_FILE, "r") as f:
            last_id = f.read().strip()

    # 3. IDが違えば（＝更新されていれば）通知
    if curr_id != last_id:
        text = f"<!here> *新しいPDFが公開されました！*\n*タイトル:* {pdf_title}\n*リンク:* {pdf_url}"
        requests.post(WEBHOOK_URL, json={"text": text})
        
        # 今回のIDを保存
        with open(ID_FILE, "w") as f:
            f.write(curr_id)

if __name__ == "__main__":
    main()
