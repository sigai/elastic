import json
from time import sleep
from redis import Redis


r = Redis(decode_responses=True)

def dump(name):
    filename = name[8:]
    while True:
        members = r.spop(name, count=10000)
        if not members:
            # return
            print("[*] watting for 10 mins to dump...")
            sleep(60*10)
            continue
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