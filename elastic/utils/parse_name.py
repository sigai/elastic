from pathlib import Path

from redis import Redis
import jieba

r = Redis(decode_responses=True)

def format_name(path):
    with path.open(mode="r", encoding="utf-8") as f:
        for phone, text in zip(*[iter(f)]*2):
            print(phone.strip(), text.strip())
            print(", ".join(jieba.cut(text)))
            break

def merge(path):
    with path.open(mode="r", encoding="utf-8") as f:
        for phone, text in zip(*[iter(f)]*2):
            r.sadd(phone.strip(), text.strip())

if __name__ == '__main__':
    # 小赢卡贷, 有借, 小赢理财, 润信小贷
    files = {"润信小贷"}
    path = Path("../docs/")
    for p in path.iterdir():
        if p.stem in files:
            merge(p)
