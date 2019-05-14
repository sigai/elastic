import json
from time import sleep
from redis import Redis


r = Redis(decode_responses=True)

def dump(name):
    filename = name[8:]
    while True:
        members = r.spop(name, count=100)
        if not members:
            break
        else:
            try:
                with open(f"../docs/{filename}.dat", mode="a", encoding="utf-8") as f:
                    for each in members:
                        item = json.loads(each)
                        f.write(f"{json.dumps(item, ensure_ascii=False)}\n")
            except Exception:
                r.sadd(name, *members)


if __name__ == '__main__':
    for each in r.keys():
        dump(each)