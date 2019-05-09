import json
import re
from time import sleep

from redis import Redis


r = Redis()

def split():
    pattern = re.compile(r"【(\w+)】")
    for _ in range(1000):
        members = r.spop("elastic:sms", count=1000)
        if not members:
            break
        for each in members:
            item = json.loads(each)
            content = item["smsContent"]
            res = pattern.findall(content)
            if res:
                service = res[0]
                r.sadd(f"elastic:{service}", each)
            else:
                r.sadd("elastic:other", each)

if __name__ == '__main__':
    split()
