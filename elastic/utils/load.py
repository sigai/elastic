import json
from time import sleep
from redis import Redis


r = Redis(decode_responses=True)

def load(filename):
    with open(f"../docs/{filename}.dat", mode="r", encoding="utf-8") as f:
        for line in f:
            r.sadd(f"elastic:{filename}", line.strip())

def extract_student():
    members = r.srandmember("elastic:consumption", number=10)
    for member in members:
        item = json.loads(member)
        count = item.pop("金额")
        date = item.pop("日期时间")
        type_spend = item.pop("操作类型")
        addr = item.pop("设备名称")
        res = r.zscore("elastic:rank", json.dumps(item))
        print(res, count)


if __name__ == "__main__":
    load("consumption")