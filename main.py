from datetime import datetime
import time
from function.def_argument import get_args
from function.search_papers import search_feedparser
from function.def_abstruct import get_summary

def main():
    # 引数の定義
    args = get_args()
    # 表示
    print(args.context)
    print(args.number)
    # 結果の保存用リスト
    messages = []

    # 結果を取得してメッセージを生成
    results = search_feedparser(args=args)
    for i, result in enumerate(results):
        message = "今日の論文です！ " + str(i+1) + "本目\n" + get_summary(result=result)
        print("message:", message)
        messages.append(message)  # メッセージをリストに追加

    # 実行した日時を取得してファイル名に使う
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{current_time}.md"

    # すべてのメッセージをまとめて .md ファイルに書き込み
    with open(file_name, "w", encoding="utf-8") as f:
        for message in messages:
            f.write(message + "\n\n")  # 各メッセージをファイルに書き込む

if __name__ == "__main__":
    main()

