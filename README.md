# Autonomous Phishing Analyst Agent

## 概要
LLM（大規模言語モデル）エージェント技術を活用し、入力されたURLの危険性を自律的に判定する分析ツール。単なる文字列マッチングではなく、WHOIS情報等の外部データをAIが自ら取得・解釈し、論理的な根拠に基づいたリスク評価を行う。

## 特徴
- **自律的ツール利用 (Tool Use)**: Google Gemini API (GenAI SDK) を用い、必要に応じて `python-whois` を呼び出すエージェント機能を実装。
- **動的コンテキスト注入**: LLMの弱点である時間感覚の欠如に対し、実行時の時刻をシステムプロンプトに動的に埋め込むことで、ドメイン登録日の新旧を正確に判定。
- **推論プロセスの可視化**: AIがどのような根拠（ドメインの存続期間、登録者の信頼性等）で詐欺と判断したか、その推論過程を提示。

## 技術スタック
- **Language**: Python 3.13
- **Framework**: Django 5.x / 6.x
- **AI Model**: Gemini 2.5 Flash
- **Libraries**: `google-genai`, `python-whois`, `python-dotenv`, `re` (Regular Expression)

## セキュリティ対策 (Security by Design)
本プロジェクトでは開発初期段階から以下の脆弱性対策を講じている。　

- **OSコマンドインジェクション対策**: 
  `whois` コマンド実行前に、正規表現を用いたホワイトリスト形式のバリデーションを実装。
  `re.match(r"^[a-zA-Z0-9\-\.]+$", domain)` により、不正な記号（`;`, `&`, `|` 等）を含む入力を完全に遮断。
- **プロンプトインジェクションへの配慮**: 
  システムプロンプトの厳格化による命令の固守、および自動関数呼び出し（Automatic Function Calling）の権限最小化を検討。
- **環境変数の厳格な管理**: 
  APIキー等の機密情報は `.env` ファイルにて管理し、`.gitignore` 設定によりリモートリポジトリへの流出を防止。（当たり前だが、セキュリティ初心者レベルの自分に対しては最初に意識すべき点）

## セットアップ
1. リポジトリをクローン
2. 仮想環境の作成と起動
   ```bash
   python3 -m venv venv
   source venv/bin/activate
3. 依存ライブラリのインストール
   ```bash
   pip install django google-genai python-whois python-dotenv
4. .env ファイルの作成
   ```bash
   GEMINI_API_KEY=あなたのAPIキー
5. サーバーの起動
   ```bash
   python manage.py runserver