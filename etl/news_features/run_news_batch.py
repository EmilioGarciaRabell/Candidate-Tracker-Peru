import sys

import get_latest_news as news

def main():
    if len(sys.argv) < 2:
        print("Usage: run_news_batch.py [morning|evening]")
        raise SystemExit(2)

    mode = sys.argv[1].lower()
    if mode == "morning":
        news.run_morning_batch()
    elif mode == "evening":
        news.run_evening_batch()
    else:
        print("Invalid mode. Use 'morning' or 'evening'")
        raise SystemExit(2)

if __name__ == "__main__":
    main()
