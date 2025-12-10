import sys

import get_latest_news as news

def main():
    if len(sys.argv) < 2:
        print("Usage: daily script")
        raise SystemExit(2)

    mode = sys.argv[1].lower()
    if mode == "daily":
        news.news_daily_script()
    else:
        print("Invalid mode. Use daily")
        raise SystemExit(2)

if __name__ == "__main__":
    main()
