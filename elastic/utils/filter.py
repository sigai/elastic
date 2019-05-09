# -*- coding: UTF-8 -*-
__author__ = "Sigai"
from pathlib import Path

def duplicate(path):
    print(f"[+] {path.name}")
    phones = set()
    with path.open(mode="r", encoding="utf-8") as f:
        for line in f:
            if line.strip().isdigit():
                phones.add(line)
    with path.open(mode="w", encoding="utf-8") as t:
        t.write("".join(phones))

if __name__ == '__main__':
    money = {"贷", "款", "钱"}
    path = Path("../doc/")
    for p in path.iterdir():
        if set(p.name).intersection(money):
            duplicate(p)
    