import os
import re
import whois
import datetime
from google import genai
from google.genai import types
from dotenv import load_dotenv

# 1. 環境設定
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 2. ツール（手足）の定義
def get_whois_info(domain: str):
    if not re.match(r"^[a-zA-Z0-9\-\.]+$", domain):
        return "無効なドメイン形式です。"
    """指定されたドメインの登録日や所有者情報を取得します。"""
    try:
        w = whois.whois(domain)
        return f"ドメイン: {domain}, 登録日: {w.creation_date}, 登録者: {w.registrar}"
    except Exception as e:
        return f"情報を取得できませんでした: {str(e)}"

# 3. メイン関数
def run_my_agent(user_query):
    today = datetime.date.today()
    system_instruction = f"今日は {today} です。あなたは高度なサイバーセキュリティ・アナリストです。提供されたツールを使ってURLを調査し、詐欺の可能性がある場合はその理由を論理的に説明してください。"
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_query,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[get_whois_info],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False)
        )
    )
    return response.text