#!/usr/bin/env python3
"""
make_card.py — سازندهٔ کارت عکس برنامهٔ روزانهٔ مرشد (هویت برند آریامیر)

نیازمندی‌ها:
    pip install playwright jdatetime
    python3 -m playwright install chromium
    (روی لینوکس اگر لازم شد: python3 -m playwright install-deps chromium)

استفاده:
    from make_card import make_card
    make_card(
        date_num="۳۱",
        date_full="سه‌شنبه ۳۱ شهریور ۱۴۰۵ · جبران بک‌لاگ",
        tag="فاز آزمون ۱۷ مهر",
        goal="🎯 هدف: ~۱۰ ساعت خالص",
        rows=[
          # (num, dot_color, task, teacher, dur, clock, note)
          ("۱","#EAB308","هندسه — جلسه ۳","استاد واعظین","۱۸۰ دقیقه","۰۷:۰۰ – ۱۰:۰۰","خواص ضرب ماتریس"),
          ...
        ],
        out_path="../plans/cards/plan_card_1405-06-31.png",
    )

رنگ نقطه‌ها (نوع بلوک):
    یادگیری جدید سخت: #EAB308 (زرد) | تثبیت/جزوه: #3ECF8E (سبز)
    تست: #79C0FF (آبی) | مرور/گزارش: #BDA4FF (بنفش)
"""
import base64, os
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
FONTS = BASE / "brand" / "fonts"
LOGO  = BASE / "brand" / "logo-app-green.png"

def _b64(p):
    return base64.b64encode(Path(p).read_bytes()).decode()

def build_html(date_num, date_full, tag, goal, rows,
               title="برنامهٔ امروز", subtitle_en="MORSHED · DAILY PLAN",
               extras=("مرور جزوه‌ها","دفتر اشتباهات")):
    kr=_b64(FONTS/"Kalameh-Regular.woff2"); km=_b64(FONTS/"Kalameh-Medium.woff2")
    ks=_b64(FONTS/"Kalameh-SemiBold.woff2"); kb=_b64(FONTS/"Kalameh-Bold.woff2")
    kbl=_b64(FONTS/"Kalameh-Black.woff2"); logo=_b64(LOGO)
    tr=""
    for num,color,task,teacher,dur,clock,note in rows:
        tr+=f'''<tr>
          <td class="idx">{num}</td>
          <td class="ex"><span class="dot" style="background:{color}"></span><span class="exwrap"><span class="exname">{task}</span><span class="teacher">{teacher}</span></span></td>
          <td class="sr">{dur}</td>
          <td class="tm">{clock}</td>
          <td class="note">{note}</td>
        </tr>'''
    chips="".join(f'<span class="chip">{c}</span>' for c in extras)
    return f'''<!DOCTYPE html><html dir="rtl" lang="fa"><head><meta charset="utf-8"><style>
@font-face{{font-family:'Kalameh';src:url(data:font/woff2;base64,{kr}) format('woff2');font-weight:400}}
@font-face{{font-family:'Kalameh';src:url(data:font/woff2;base64,{km}) format('woff2');font-weight:500}}
@font-face{{font-family:'Kalameh';src:url(data:font/woff2;base64,{ks}) format('woff2');font-weight:600}}
@font-face{{font-family:'Kalameh';src:url(data:font/woff2;base64,{kb}) format('woff2');font-weight:700}}
@font-face{{font-family:'Kalameh';src:url(data:font/woff2;base64,{kbl}) format('woff2');font-weight:900}}
*{{margin:0;padding:0;box-sizing:border-box;font-family:'Kalameh',sans-serif}}
body{{background:#000;width:1600px;padding:60px 70px}}
.head{{display:flex;align-items:center;justify-content:space-between;margin-bottom:40px;flex-direction:row-reverse}}
.head-right{{display:flex;align-items:center;gap:22px;flex-direction:row-reverse}}
.logo{{width:88px;height:88px;border-radius:22px}}
.title-block{{text-align:right}}
.day-en{{font-size:15px;letter-spacing:.28em;color:#3ECF8E;font-weight:700;direction:ltr;text-align:right}}
.title-fa{{font-size:40px;font-weight:900;color:#FAFAFA;line-height:1.15;margin-top:4px}}
.sub-fa{{font-size:19px;color:#898989;font-weight:500;margin-top:6px}}
.head-left{{text-align:left}}
.date-num{{font-size:80px;font-weight:900;color:#3ECF8E;line-height:1}}
.tag{{display:inline-block;border:1.5px solid #3ECF8E;color:#3ECF8E;border-radius:999px;padding:8px 20px;font-size:15px;font-weight:600;margin-top:10px}}
.panel{{background:#0A0A0A;border:1px solid #2E2E2E;border-radius:26px;overflow:hidden}}
table{{width:100%;border-collapse:collapse;table-layout:fixed}}
th{{padding:22px 28px;font-size:14px;color:#898989;font-weight:600;border-bottom:1px solid #2E2E2E;text-align:right}}
th.h-idx,td.idx{{width:64px;text-align:right}}
th.h-ex,td.ex{{width:400px}}
th.h-sr,td.sr{{width:150px}}
th.h-tm,td.tm{{width:190px}}
th.h-note,td.note{{width:auto;text-align:left}}
td{{padding:26px 28px;border-bottom:1px solid #1c1c1c;vertical-align:middle}}
tr:last-child td{{border-bottom:none}}
.idx{{color:#3ECF8E;font-size:28px;font-weight:900}}
.dot{{display:inline-block;width:13px;height:13px;border-radius:50%;margin-left:14px;vertical-align:middle}}
.exwrap{{display:inline-flex;flex-direction:column;vertical-align:middle}}
.exname{{color:#FAFAFA;font-size:23px;font-weight:700;line-height:1.3}}
.teacher{{color:#525252;font-size:15px;font-weight:500;margin-top:3px}}
.sr{{color:#72E3AD;font-size:19px;font-weight:600;text-align:right}}
.tm{{color:#3ECF8E;font-size:19px;font-weight:600;text-align:right;direction:ltr}}
.note{{color:#B4B4B4;font-size:18px;font-weight:400;text-align:left;line-height:1.5}}
.footer{{background:#0d0d0d;padding:26px 32px;display:flex;align-items:center;justify-content:space-between;flex-direction:row-reverse}}
.chips{{display:flex;gap:12px;align-items:center;flex-direction:row-reverse}}
.chip{{background:#121212;border:1px solid #2E2E2E;color:#D4D4D4;border-radius:999px;padding:9px 20px;font-size:16px;font-weight:500}}
.chip-label{{color:#525252;font-size:13px;letter-spacing:.2em;font-weight:700;direction:ltr}}
.goal{{color:#3ECF8E;font-size:17px;font-weight:700}}
.brandline{{margin-top:26px;display:flex;justify-content:space-between;align-items:center;color:#393939;font-size:14px;flex-direction:row-reverse}}
.brandline .site{{color:#525252;direction:ltr;letter-spacing:.1em}}
</style></head><body>
<div class="head">
  <div class="head-right"><img class="logo" src="data:image/png;base64,{logo}">
    <div class="title-block"><div class="day-en">{subtitle_en}</div>
      <div class="title-fa">{title}</div><div class="sub-fa">{date_full}</div></div></div>
  <div class="head-left"><div class="date-num">{date_num}</div><div class="tag">{tag}</div></div>
</div>
<div class="panel"><table><thead><tr>
  <th class="h-idx">#</th><th class="h-ex">برنامه · TASK</th><th class="h-sr">مدت · TIME</th>
  <th class="h-tm">ساعت · CLOCK</th><th class="h-note">نکته · NOTE</th>
</tr></thead><tbody>{tr}</tbody></table>
<div class="footer"><div class="chips">{chips}<span class="chip-label">EXTRAS</span></div>
<div class="goal">{goal}</div></div></div>
<div class="brandline"><span class="site">ariamir.ir</span>
<span>رتبهٔ ۱ کامپیوتر شریف · کنکور ۱۴۰۶</span></div>
</body></html>'''

def make_card(date_num, date_full, tag, goal, rows, out_path, **kw):
    from playwright.sync_api import sync_playwright
    html = build_html(date_num, date_full, tag, goal, rows, **kw)
    tmp = "/tmp/_morshed_card.html"; Path(tmp).write_text(html, encoding="utf-8")
    out = Path(out_path); out.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b=p.chromium.launch(args=['--no-sandbox'])
        pg=b.new_page(viewport={'width':1600,'height':1000}, device_scale_factor=2)
        pg.goto(f'file://{tmp}'); pg.wait_for_timeout(700)
        pg.query_selector('body').screenshot(path=str(out)); b.close()
    print("saved", out); return str(out)

if __name__ == "__main__":
    # نمونهٔ تست
    make_card("۳۰","دوشنبه ۳۰ شهریور ۱۴۰۵ · نمونه","فاز آزمون ۱۷ مهر","🎯 هدف: ~۶ ساعت خالص",
      [("۱","#EAB308","هندسه — تکمیل جلسه ۲","استاد واعظین","۹۰ دقیقه","۱۳:۰۰ – ۱۴:۳۰","ضرب ماتریس")],
      "../plans/cards/_sample.png")
