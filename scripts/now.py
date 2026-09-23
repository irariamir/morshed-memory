#!/usr/bin/env python3
"""
now.py — تاریخ و زمان واقعی امروز (شمسی + میلادی).
مرشد باید در ابتدای هر جلسه این را اجرا کند تا تاریخ همیشه به‌روز باشد.
هرگز تاریخ را حدس نزن — همیشه از این استفاده کن.
    python3 scripts/now.py
"""
import datetime
try:
    import jdatetime
except ImportError:
    import subprocess, sys
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "jdatetime"])
    import jdatetime

JDAYS = ['شنبه','یکشنبه','دوشنبه','سه‌شنبه','چهارشنبه','پنجشنبه','جمعه']
JMONTHS = ['فروردین','اردیبهشت','خرداد','تیر','مرداد','شهریور',
           'مهر','آبان','آذر','دی','بهمن','اسفند']

def today_info():
    now = datetime.datetime.now()
    j = jdatetime.date.fromgregorian(date=now.date())
    return {
        "gregorian": now.strftime('%Y-%m-%d'),
        "time": now.strftime('%H:%M'),
        "jalali": j.strftime('%Y/%m/%d'),
        "weekday": JDAYS[j.weekday()],
        "pretty": f"{JDAYS[j.weekday()]} {j.day} {JMONTHS[j.month-1]} {j.year}",
        "j": j,
    }

if __name__ == "__main__":
    i = today_info()
    print(f"امروز: {i['pretty']}  (ساعت {i['time']})")
    print(f"شمسی: {i['jalali']} | میلادی: {i['gregorian']}")
