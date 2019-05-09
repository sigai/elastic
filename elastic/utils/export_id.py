import json
from time import sleep
from redis import Redis


r = Redis(decode_responses=True)

def mark_crawled():
    members = r.smembers("elastic:company")
    for each in members:
        item = json.loads(each)
        r.sadd("elastic:crawled", item["_id"])

def dump(name):
    filename = name[8:]
    while True:
        members = r.spop(name, count=100)
        if not members:
            break
        else:
            with open(f"../doc/{filename}.dat", mode="a", encoding="utf-8") as f:
                for each in members:
                    item = json.loads(each)
                    text = item["smsContent"]
                    phone = item["phoneNumbers"]
                    f.write(f"{phone}\n{text}\n")

if __name__ == '__main__':
    for each in r.keys():
        # if r.scard(each) > 1000000:
        #     continue
        if each == "elastic:sms":
            continue
        print(f"dump {each}...")
        dump(each)

