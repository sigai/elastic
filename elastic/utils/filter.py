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
    # 小赢卡贷, 有借, 小赢理财, 润信小贷
    money = {"360借条", "豆豆钱", "信用钱包", "拍拍贷", "我来贷", 
            "应急管家", "点点", "女王节", "贷款精选", "分期花呗",
            "周必下", "花千鼓"}
    games = {"正版传奇", "蓝月王者", "剑荡九天", "霸者屠龙", "毒液传奇", 
            "再战沙巴克", "热血私服", "传奇散人版", "荣耀使者", "金猪传奇",
            "神魔传世", "奇迹归来", "斩月屠龙", "破晓之刃", "秦时纷争"}
    path = Path("../doc/")
    for p in path.iterdir():
        if p.stem in money or p.stem in games:
            duplicate(p)
    