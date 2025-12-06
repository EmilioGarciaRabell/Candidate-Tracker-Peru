import sys

import get_latest_news as news

def main():
    if len(sys.argv) < 2:
        print("Usage: run weekly script")
        raise SystemExit(2)

    mode = sys.argv[1].lower()
    if mode == "weekly":
        news.news_weekly_srcipt()
    else:
        print("Invalid mode. Use weekly")
        raise SystemExit(2)

if __name__ == "__main__":
    main()