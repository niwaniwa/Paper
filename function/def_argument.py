import sys
import argparse

def get_args():
    # オブジェクト生成
    parser = argparse.ArgumentParser()

    # 引数設定
    if sys.stdin.isatty():
        parser.add_argument("context", help="please set me", type=str)
        parser.add_argument("number", help="please set me", type=int)

    # 結果を受ける
    args = parser.parse_args()

    return(args)

def main():
    args = get_args()

    print(args.context)
    print(args.number)

if __name__ == '__main__':
    main()

