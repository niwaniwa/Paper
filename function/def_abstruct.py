import os
from openai import OpenAI

#OpenAIのapiキー
os.environ["OPENAI_API_KEY"] = ''

def get_summary(result):
    system = """与えられた論文の要点を3点のみでまとめ、以下のフォーマットで日本語で出力してください。```
    タイトルの日本語訳
    ・要点1
    ・要点2
    ・要点3
    ```"""

    text = f'title: {result["title"]}\nbody: {result["summary"]}'
    # クライアントの準備
    client = OpenAI()
    # arxiv APIで最新の論文情報を取得する
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {'role': 'system', 'content': system},
            {'role': 'user', 'content': text}
        ],
        temperature=0.25,
    )

    summary = response.choices[0].message.content
    title_en = result['title']
    title, *body = summary.split('\n')
    body = '\n'.join(body)
    date_str = result['published'].strftime("%Y-%m-%d %H:%M:%S")
    message = f"発行日: {date_str}\n{result['arxiv_id']}\n{title_en}\n{title}\n{body}\n"

    return message
