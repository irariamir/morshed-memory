#!/usr/bin/env python3
"""
make_week_card.py — کارت عکس برنامهٔ هفتگی مرشد (هویت برند آریامیر)

نیازمندی‌ها:
    pip install playwright jdatetime
    python3 -m playwright install chromium
    (لینوکس: apt libnspr4 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libgbm1 libasound2 libpango-1.0-0 libcairo2 ...)

استفاده:
    from make_week_card import make_week_card
    make_week_card(
        week_title="هفتهٔ اول مهر",
        date_range="۴ تا ۱۰ مهر ۱۴۰۵",
        tag="جبران بک‌لاگ · آزمون ۱۷ مهر",
        goal="🎯 ۱۶ جلسه + آزمون جمعه · ~۵۵ ساعت خالص",
        days=[
          # (day_name, date, hours, [ (color, label), ... ] )
          ("شنبه","۴ مهر","۶ ساعت",[("#EAB308","فیزیک ج۱"),("#EAB308","حسابان ج۱")]),
          ...
        ],
        out_path="../plans/cards/week_card.png",
    )
"""
import base64
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
FONTS = BASE / "brand" / "fonts"
LOGO  = BASE / "brand" / "logo-app-green.png"

def _b64(p):
    return base64.b64encode(Path(p).read_bytes()).decode()

def build_html(week_title, date_range, tag, goal, days, legend=None):
    kr=_b64(FONTS/"Kalameh-Regular.woff2"); km=_b64(FONTS/"Kalameh-Medium.woff2")
    ks=_b64(FONTS/"Kalameh-SemiBold.woff2"); kb=_b64(FONTS/"Kalameh-Bold.woff2")
    kbl=_b64(FONTS/"Kalameh-Black.woff2"); logo=_b64(LOGO)
    if legend is None:
        legend=[("#EAB308","یادگیری جدید"),("#3ECF8E","تثبیت/جزوه"),
                ("#79C0FF","تست/آزمون"),("#BDA4FF","مرور")]
    cards=""
    for name,date,hours,items in days:
        chips="".join(
            f'<span class="chip"><span class="cdot" style="background:{c}"></span>{lbl}</span>'
            for c,lbl in items)
        cards+=f'''<div class="daycard">
          <div class="dhead"><div class="dname">{name}</div><div class="ddate">{date}</div></div>
          <div class="dhours">{hours}</div>
          <div class="chips">{chips}</div>
        </div>'''
    leg="".join(f'<span class="lg"><span class="cdot" style="background:{c}"></span>{lbl}</span>' for c,lbl in legend)
    return f'''<!DOCTYPE html><html dir="rtl" lang="fa"><head><meta charset="utf-8"><style>
@font-face{{font-family:'Kalameh';src:url(data:font/woff2;base64,{kr}) format('woff2');font-weight:400}}
@font-face{{font-family:'Kalameh';src:url(data:font/woff2;base64,{km}) format('woff2');font-weight:500}}
@font-face{{font-family:'Kalameh';src:url(data:font/woff2;base64,{ks}) format('woff2');font-weight:600}}
@font-face{{font-family:'Kalameh';src:url(data:font/woff2;base64,{kb}) format('woff2');font-weight:700}}
@font-face{{font-family:'Kalameh';src:url(data:font/woff2;base64,{kbl}) format('woff2');font-weight:900}}
*{{margin:0;padding:0;box-sizing:border-box;font-family:'Kalameh',sans-serif}}
body{{background:#000;width:1600px;padding:60px 70px}}
.head{{display:flex;align-items:center;justify-content:space-between;margin-bottom:38px;flex-direction:row-reverse}}
.head-right{{display:flex;align-items:center;gap:22px;flex-direction:row-reverse}}
.logo{{width:88px;height:88px;border-radius:22px}}
.title-block{{text-align:right}}
.day-en{{font-size:15px;letter-spacing:.28em;color:#3ECF8E;font-weight:700;direction:ltr;text-align:right}}
.title-fa{{font-size:40px;font-weight:900;color:#FAFAFA;line-height:1.15;margin-top:4px}}
.sub-fa{{font-size:19px;color:#898989;font-weight:500;margin-top:6px}}
.head-left{{text-align:left}}
.tag{{display:inline-block;border:1.5px solid #3ECF8E;color:#3ECF8E;border-radius:999px;padding:8px 20px;font-size:15px;font-weight:600}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}}
.daycard{{background:#0A0A0A;border:1px solid #2E2E2E;border-radius:22px;padding:24px 22px;min-height:210px}}
.daycard.big{{grid-column:span 1}}
.dhead{{display:flex;justify-content:space-between;align-items:baseline;flex-direction:row-reverse;margin-bottom:6px}}
.dname{{font-size:26px;font-weight:900;color:#FAFAFA}}
.ddate{{font-size:16px;color:#525252;font-weight:600}}
.dhours{{display:inline-block;color:#006239;background:#3ECF8E;border-radius:999px;padding:4px 14px;font-size:15px;font-weight:700;margin-bottom:16px}}
.chips{{display:flex;flex-direction:column;gap:9px;align-items:flex-end}}
.chip{{display:inline-flex;align-items:center;flex-direction:row-reverse;gap:9px;background:#121212;border:1px solid #2E2E2E;color:#E4E4E4;border-radius:10px;padding:8px 13px;font-size:16px;font-weight:500;width:100%;justify-content:flex-end}}
.cdot{{display:inline-block;width:11px;height:11px;border-radius:50%;flex:none}}
.legend{{display:flex;gap:22px;justify-content:flex-end;flex-direction:row-reverse;margin-top:26px}}
.lg{{display:inline-flex;align-items:center;flex-direction:row-reverse;gap:9px;color:#898989;font-size:16px;font-weight:600}}
.goalbar{{margin-top:22px;background:#0d0d0d;border:1px solid #2E2E2E;border-radius:16px;padding:20px 26px;text-align:center;color:#3ECF8E;font-size:22px;font-weight:900}}
.brandline{{margin-top:24px;display:flex;justify-content:space-between;align-items:center;color:#393939;font-size:14px;flex-direction:row-reverse}}
.brandline .site{{color:#525252;direction:ltr;letter-spacing:.1em}}
</style></head><body>
<div class="head">
  <div class="head-right"><img class="logo" src="data:image/png;base64,{logo}">
    <div class="title-block"><div class="day-en">MORSHED · WEEKLY PLAN</div>
      <div class="title-fa">برنامهٔ هفتگی — {week_title}</div><div class="sub-fa">{date_range}</div></div></div>
  <div class="head-left"><div class="tag">{tag}</div></div>
</div>
<div class="grid">{cards}</div>
<div class="legend">{leg}</div>
<div class="goalbar">{goal}</div>
<div class="brandline"><span class="site">ariamir.ir</span>
<span>رتبهٔ ۱ کامپیوتر شریف · کنکور ۱۴۰۶</span></div>
</body></html>'''

def make_week_card(week_title, date_range, tag, goal, days, out_path, **kw):
    from playwright.sync_api import sync_playwright
    html = build_html(week_title, date_range, tag, goal, days, **kw)
    tmp = "/tmp/_morshed_week.html"; Path(tmp).write_text(html, encoding="utf-8")
    out = Path(out_path); out.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b=p.chromium.launch(args=['--no-sandbox'])
        pg=b.new_page(viewport={'width':1600,'height':1100}, device_scale_factor=2)
        pg.goto(f'file://{tmp}'); pg.wait_for_timeout(700)
        pg.query_selector('body').screenshot(path=str(out)); b.close()
    print("saved", out); return str(out)
