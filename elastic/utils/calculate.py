import json
from time import sleep
from redis import Redis


r = Redis(decode_responses=True)


def calc():
    while True:
        try:
            members = r.spop("elastic:consumption", count=100)
            if not members:
                break
            for member in members:
                item = json.loads(member)
                count = item.pop("金额")
                date = item.pop("日期时间")
                type_spend = item.pop("操作类型")
                addr = item.pop("设备名称")
                res = r.zscore("elastic:rank", json.dumps(item))

                if "消费" in type_spend:
                    if res is None:
                        r.zadd("elastic:rank", {item["学号"]: int(count)})
                    else:
                        r.zincrby("elastic:rank", int(count), item["学号"])
                r.sadd("elastic:student", json.dumps(item))
        except Exception:
            r.sadd("elastic:consumption", *members)


def extract_student():
    members = r.smembers("elastic:")
    for member in members:
        item = json.loads(member)
        # gender = "m" if item["性别"] == "男" else "f"
        search = item["学院"]
        r.sadd(f"elastic:{search}", json.dumps(item, ensure_ascii=False))


if __name__ == "__main__":
    extract_student()