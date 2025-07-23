# Python Railway Template - Selenium Standalone Chromium

Selenium Standalone Chromium を使用した Remote WebDriver スクレイピングアプリケーションのテンプレートです。

## 🚀 特徴

- **Selenium Standalone Chromium**: 安定したローカル Docker 環境
- **Remote WebDriver**: スケーラブルな分離アーキテクチャ
- **ARM64 (M1 Mac) 対応**: seleniarm イメージを使用
- **色付きログ**: ANSI色とアイコンによる美しいログ出力
- **モジュラー設計**: 保守性の高いコード構造
- **定数管理**: 一元的な設定値管理
- **汎用的なスクレイパークラス**: 再利用可能な WebDriver 管理

## 📁 プロジェクト構造

```
src/
├── main.py              # メインエントリーポイント
├── scraper.py           # WebDriver管理クラスとスクレイピング関数
├── constants.py         # 定数管理（設定値、メッセージ等）
├── utils/
│   └── logger.py        # 色付きロガー
├── __init__.py
tests/
└── test_main.py         # テストファイル
docker-compose.yml       # Selenium Standalone構成
Dockerfile               # アプリケーションコンテナ
Makefile                 # 便利なコマンド集
```

## 🎯 設計思想

### クラス設計の分離
- **`StandaloneChromiumScraper`**: WebDriverの管理に特化した汎用クラス
  - 接続・切断の管理
  - 基本的なWebDriver操作（`get_page`, `find_element`, `take_screenshot`など）
  - Context Managerによる安全なリソース管理

- **外部関数**: 特定の業務ロジック
  - `scrape_test_page()`: テストページ固有のスクレイピングロジック
  - クラスとビジネスロジックの責任分離

### 定数管理
- **`constants.py`**: 全ての設定値を一箇所で管理
  - Selenium設定（URL、ブラウザ、タイムアウト）
  - ブラウザオプション（ウィンドウサイズ、User-Agent）
  - ログ設定（色、アイコン、ANSI制御コード）
  - メッセージテンプレート（エラー、成功メッセージ）

## 🛠️ 使用方法

### 基本使用例

```python
from scraper import StandaloneChromiumScraper, scrape_test_page

# 汎用的なWebDriver管理
with StandaloneChromiumScraper() as scraper:
    # ページ取得
    scraper.get_page("https://example.com")
    
    # 要素検索
    element = scraper.find_element(By.TAG_NAME, "h1")
    
    # ページ情報取得
    page_info = scraper.get_page_info()
    
    # スクリーンショット
    scraper.take_screenshot("example.png")

# 特定の業務ロジック
with StandaloneChromiumScraper() as scraper:
    result = scrape_test_page(scraper)
    print(result)
```

### Docker での実行

```bash
# スクレイピング実行（Selenium起動 + アプリ実行 + ログ表示）
make scrape

# Selenium Standalone のみ起動
make start-selenium

# ログ表示
make logs
```

### ローカル開発

```bash
# 依存関係インストール
uv sync

# Python実行
python -m src.main
```

## ⚙️ 設定

### 環境変数

```bash
SELENIUM_BROWSER=chrome          # chrome または firefox
SELENIUM_REMOTE_URL=http://selenium:4444  # Docker環境
# SELENIUM_REMOTE_URL=http://localhost:4444  # ローカル環境
```

### ブラウザオプション

`src/constants.py` で設定をカスタマイズ:

```python
# Chrome設定
CHROME_WINDOW_SIZE = "1920,1080"
CHROME_USER_AGENT = "Mozilla/5.0 ..."

# Firefox設定  
FIREFOX_WINDOW_WIDTH = "1920"
FIREFOX_WINDOW_HEIGHT = "1080"

# タイムアウト
DEFAULT_TIMEOUT = 10  # 秒
```

## 🔧 カスタマイズ

### 新しいスクレイピング関数の追加

```python
def scrape_custom_site(scraper: StandaloneChromiumScraper) -> dict:
    """カスタムサイトのスクレイピング"""
    scraper.get_page("https://custom-site.com")
    scraper.wait_for_element(By.CLASS_NAME, "content")
    
    # 業務ロジック
    data = {}
    elements = scraper.find_elements(By.CSS_SELECTOR, ".item")
    for element in elements:
        data[element.get_attribute("id")] = element.text
    
    return data
```

### 定数の追加

```python
# constants.py に追加
CUSTOM_SITE_URL = "https://custom-site.com"
CUSTOM_TIMEOUT = 15
CUSTOM_ERROR_MSG = "Custom site scraping failed: {}"
```

## 📊 ログ出力

色付きログで実行状況を視覚的に確認:

```
✅ 2025-01-23 12:23:51 - INFO - Connected successfully! Browser: chrome 124.0
🕷️ 2025-01-23 12:23:51 - INFO - Navigating to: https://httpbin.org/html  
📸 2025-01-23 12:23:54 - INFO - Screenshot saved: reports/test_screenshot.png
✅ 2025-01-23 12:23:54 - INFO - Test completed successfully!
```

## 🧪 テスト

```bash
# Docker内でテスト実行
docker run --rm python-railway-template-python-app python -m pytest tests/ -v

# ローカルでテスト実行
uv run pytest tests/ -v
```

## 🚢 Railway デプロイ

1. GitHub にプッシュ
2. Railway でプロジェクト作成
3. 環境変数設定:
   ```
   SELENIUM_REMOTE_URL=https://your-browserless-endpoint
   SELENIUM_BROWSER=chrome
   ```

## 🔍 トラブルシューティング

### よくある問題

1. **接続エラー**: Selenium Standalone が起動しているか確認
   ```bash
   docker-compose up selenium-chrome
   ```

2. **ARM64 (M1 Mac) での問題**: `seleniarm` イメージを使用
   ```yaml
   # docker-compose.yml
   image: seleniarm/standalone-chromium:latest
   ```

3. **要素が見つからない**: 適切な待機を追加
   ```python
   scraper.wait_for_element(By.ID, "target-element")
   ```

### 設定確認

```bash
# Selenium Grid 状態確認
curl http://localhost:4444/wd/hub/status

# VNC で画面確認 
open vnc://localhost:5900
```

## 📄 ライセンス

MIT License

## 🤝 貢献

1. Fork the project
2. Create your feature branch
3. Commit your changes  
4. Push to the branch
5. Open a Pull Request
