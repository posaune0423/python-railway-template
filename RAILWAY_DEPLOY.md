# 🚂 Railway Deployment Guide

10分おきにcronで実行されるSeleniumスクレイピングアプリをRailwayにデプロイする手順です。

## 📋 前提条件

1. **GitHubアカウント**: コードをGitHubリポジトリにプッシュ済み
2. **Railwayアカウント**: [Railway.app](https://railway.app)でアカウント作成
3. **ブラウザレスサービス**: [Browserless.io](https://browserless.io)などの外部サービス（推奨）

## 🛠️ 1. Browserless.io設定（推奨）

### 1.1 アカウント作成
1. [Browserless.io](https://browserless.io)でアカウント作成
2. フリープランでも月1000回まで利用可能
3. APIトークンを取得

### 1.2 接続URLの確認
```
wss://chrome.browserless.io/
```
または独自のドメインを使用している場合は、そのドメインを使用

## 🚀 2. Railwayデプロイ手順

### 2.1 プロジェクト作成
1. [Railway Dashboard](https://railway.app/dashboard)にログイン
2. **"New Project"** をクリック
3. **"Deploy from GitHub repo"** を選択
4. リポジトリを選択

### 2.2 環境変数設定
Railwayダッシュボードで以下の環境変数を設定：

| 変数名 | 値 | 説明 |
|--------|----|----|
| `SELENIUM_REMOTE_URL` | `wss://chrome.browserless.io/` | Browserless.ioのURL |
| `SELENIUM_BROWSER` | `chrome` | 使用ブラウザ |
| `BROWSERLESS_TOKEN` | `your-api-token` | Browserless APIトークン（必要に応じて） |

### 2.3 Cron設定
1. Railwayダッシュボードでサービスを選択
2. **"Settings"** タブを開く
3. **"Cron"** セクションで以下を設定：
   ```
   Schedule: */10 * * * *
   Command: python -m src.main
   ```

または、すでに`railway.toml`に設定済みのため、デプロイ時に自動適用されます。

## ⚙️ 3. 設定の詳細

### 3.1 Cron式の説明
```
*/10 * * * *
```
- `*/10`: 10分ごと
- `*`: 毎時
- `*`: 毎日
- `*`: 毎月
- `*`: 全曜日

### 3.2 タイムゾーン
- Railway cronはUTC時間で動作
- 日本時間から9時間引いた時間で実行

### 3.3 実行制限
- Railway cronは最短5分間隔
- 10分間隔は問題なく動作

## 🔍 4. デプロイ後の確認

### 4.1 ログ確認
```bash
# Railway CLIをインストール
npm install -g @railway/cli

# ログイン
railway login

# プロジェクトに接続
railway link

# ログ確認
railway logs
```

### 4.2 手動実行テスト
```bash
# ワンタイム実行でテスト
railway run python -m src.main
```

### 4.3 実行状況の確認
Railwayダッシュボードの**"Deployments"**タブでcron実行履歴を確認できます。

## 🎯 5. コスト最適化

### 5.1 Railwayコスト
- **Starter Plan**: $5/月（500時間まで）
- **Pro Plan**: $20/月（無制限）

### 5.2 Browserless.ioコスト
- **Free Plan**: 1000リクエスト/月
- **Starter Plan**: $29/月（10,000リクエスト）

### 5.3 10分間隔での月間実行回数
```
1日 = 144回実行（24時間 × 6回/時間）
1ヶ月 = 4,320回実行（30日 × 144回）
```
→ Browserless.io Starterプランが必要

## 🐛 6. トラブルシューティング

### 6.1 よくあるエラー

**エラー**: `Connection refused`
```bash
# 環境変数確認
railway variables

# 正しいURLを設定
railway variables set SELENIUM_REMOTE_URL=wss://chrome.browserless.io/
```

**エラー**: `Cron not triggering`
```bash
# railway.tomlの設定確認
cat railway.toml

# 再デプロイ
git push origin main
```

**エラー**: `Screenshot save failed`
```bash
# Railway環境では/tmpディレクトリを使用
railway variables set SCREENSHOT_DIR=/tmp/reports
```

### 6.2 デバッグ用環境変数
```bash
# ログレベルを詳細に
railway variables set LOG_LEVEL=DEBUG

# タイムアウトを延長
railway variables set DEFAULT_TIMEOUT=30
```

## 📊 7. 監視とアラート

### 7.1 Railway通知設定
1. Railwayダッシュボード → Settings → Notifications
2. 失敗時の通知を有効化
3. SlackやDiscordと連携可能

### 7.2 外部監視サービス
- [UptimeRobot](https://uptimerobot.com/): ヘルスチェック用
- [Cronitor](https://cronitor.io/): Cron実行監視用

## 🔄 8. アップデートとメンテナンス

### 8.1 コード更新
```bash
# ローカルで変更
git add .
git commit -m "Update scraping logic"
git push origin main

# Railwayが自動デプロイ
```

### 8.2 設定変更
```bash
# Railway CLI経由
railway variables set SELENIUM_BROWSER=firefox

# または、ダッシュボードで直接変更
```

## ✅ 9. 完了チェックリスト

- [ ] GitHubリポジトリにコードをプッシュ
- [ ] Browserless.ioアカウント作成とトークン取得
- [ ] Railwayプロジェクト作成
- [ ] 環境変数設定（`SELENIUM_REMOTE_URL`, `SELENIUM_BROWSER`）
- [ ] Cron設定確認（`*/10 * * * *`）
- [ ] 手動実行テスト成功
- [ ] ログ確認で正常動作を確認
- [ ] 通知設定（任意）

## 🎉 完了！

これで10分おきにスクレイピングが自動実行されるRailwayアプリが完成です！

ダッシュボードでログを確認し、正常に動作していることを確認してください。 
