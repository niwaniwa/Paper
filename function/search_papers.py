from function.def_argument import get_args
import os
import feedparser
from datetime import datetime


def make_query(args):
    # 元のqueryを作成
    query = ""
    # categoryのqueryを作成
    query_cat = "all:{}".format(args.context)
    max_results = "max_results={max_results}".format(max_results=args.number)
    query += query_cat

    query += " AND " + query_date

    # 作成されたクエリを表示
    print("作成されたクエリ：\n{}\n".format(query))

    self.query = query

def search_feedparser(args):
    # ベースとなるURLを作成
    base_url = "https://export.arxiv.org/api/query?search_query="
    # クエリを指定
    query = "all:" + args.context
    # 検索件数
    max_results = args.number
    # 結果を新しいものから順にソートする
    sort_results = "&sortBy=lastUpdatedDate&sortOrder=descending&max_results={max_results}".format(max_results=max_results)

    d = feedparser.parse(base_url + query + sort_results)

    results = []

    # entriesに検索結果が格納されている
    for entry in d.entries:
        # id
        # 例: 'http://arxiv.org/abs/1909.07581v2' ← ID + v2 みたいに"vn"としてバージョン情報がついているので"v"以前を取り出す
        arxiv_id = os.path.basename(entry.id).split("v")[0]
        # タイトル
        title = entry.title
        # リンクURL
        link = entry.link
        # サマリー. 改行を削除
        summary = entry.summary.replace("\n", "")

        # 第一版提出日時
        # time.struct_time 形式で保存されているのでdatetime形式に変更（https://cortyuming.hateblo.jp/entry/20100919/p1）
        published = datetime(*entry.published_parsed[:6])
        # 更新日時
        updated = datetime(*entry.updated_parsed[:6])
        # バージョン
        version = int(link[-1])
        # 著者
        authors = dict(authors=[author["name"] for author in entry.authors])
        # カテゴリー
        categories = dict(categories=[tags["term"] for tags in entry.tags])
        # コメント
        # コメントがない場合もあるので、try~exceptで処理
        try:
            comment = entry.arxiv_comment
        except AttributeError:
            comment = None
        
        # 論文情報を格納
        paper = {
            "arxiv_id": arxiv_id,
            "title": title,
            "link": link,
            "summary": summary,
            "published": published,
            "updated": updated,
            "version": version,
            "authors": authors,
            "categories": categories,
            "comment": comment,
        }   

        results.append(paper)

    return results

def download_pdf(all_results):
    # PDFのダウンロード
    for r in all_results:
        paper = next(arxiv.Client().results(arxiv.Search(id_list=["9201301v1"])))
        # Download the PDF to a specified directory with a custom filename.
        paper.download_pdf(dirpath="./data", filename= r.id + ".pdf")
