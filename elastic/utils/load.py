import json
from time import sleep
from redis import Redis


r = Redis(decode_responses=True)

jid = set()
with open(f"../docs/caseanalysiscorelawer.dat", mode="r", encoding="utf-8") as f:
    for line in f:
        if not r.sismember("itslaw:crawled", line.strip()):
            jid.add(line)
with open(f"../docs/caseanalysiscorelawer2.dat", mode="w", encoding="utf-8") as f:
    f.write("".join(jid))