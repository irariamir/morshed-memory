#!/usr/bin/env python3
"""
make_cards_v2.py — نسل دوم کارت‌های مرشد (دیزاین خفن، تم و فونت برند حفظ‌شده)

خروجی‌ها:
  1) کارت نمای کلی هفته (overview)
  2) کارت سهم درس‌ها (ساعت + جلسه)
  3) هفت کارت روزانهٔ ساعت‌به‌ساعت

تم برند بدون تغییر: مشکی #000/#0A0A0A · سبز #3ECF8E · فونت Kalameh
دیزاین جدید: گرادیان‌های ظریف سبز، تایم‌لاین عمودی، نوار پیشرفت، آیکون‌های نوع بلوک،
هدر شیشه‌ای، بَج ساعت، فوتر برند.
"""
import base64
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
FONTS = BASE / "brand" / "fonts"
LOGO  = BASE / "brand" / "logo-app-green.png"

# پالت برند
C = dict(bg="#000000", surface="#0A0A0A", surface2="#111111", border="#242424",
         green="#3ECF8E", green_bright="#72E3AD", green_deep="#006239", green_dark="#15593B",
         fg="#FAFAFA", fg2="#B4B4B4", muted="#6E6E6E", faint="#3A3A3A",
         yellow="#EAB308", blue="#79C0FF", purple="#BDA4FF")

# نوع بلوک: (رنگ، آیکون یونی‌کد)
KIND = {
 "learn":  (C["yellow"], "▲"),   # یادگیری جدید سخت
 "fix":    (C["green"],  "●"),    # تثبیت/جزوه
 "test":   (C["blue"],   "◆"),    # تست
 "review": (C["purple"], "◈"),    # مرور
 "rest":   (C["muted"],  "○"),    # استراحت/غذا
 "school": ("#4A4A4A",   "▸"),    # مدرسه
 "sport":  (C["green_bright"], "✦"), # ورزش
}

def _b64(p): return base64.b64encode(Path(p).read_bytes()).decode()

def _fonts_css():
    kr=_b64(FONTS/"Kalameh-Regular.woff2"); km=_b64(FONTS/"Kalameh-Medium.woff2")
    ks=_b64(FONTS/"Kalameh-SemiBold.woff2"); kb=_b64(FONTS/"Kalameh-Bold.woff2")
    kbl=_b64(FONTS/"Kalameh-Black.woff2")
    return f"""
@font-face{{font-family:'Kalameh';src:url(data:font/woff2;base64,{kr}) format('woff2');font-weight:400}}
@font-face{{font-family:'Kalameh';src:url(data:font/woff2;base64,{km}) format('woff2');font-weight:500}}
@font-face{{font-family:'Kalameh';src:url(data:font/woff2;base64,{ks}) format('woff2');font-weight:600}}
@font-face{{font-family:'Kalameh';src:url(data:font/woff2;base64,{kb}) format('woff2');font-weight:700}}
@font-face{{font-family:'Kalameh';src:url(data:font/woff2;base64,{kbl}) format('woff2');font-weight:900}}
"""

def _base_css():
    return _fonts_css()+f"""
*{{margin:0;padding:0;box-sizing:border-box;font-family:'Kalameh',sans-serif}}
body{{background:{C['bg']};margin:0}}
.page{{background:{C['bg']};width:1600px;padding:56px 64px;position:relative;overflow:hidden}}
.glow{{position:absolute;border-radius:50%;filter:blur(120px);opacity:.16;z-index:0}}
.glow1{{width:620px;height:620px;background:{C['green']};top:-260px;left:-160px}}
.glow2{{width:520px;height:520px;background:{C['green_deep']};bottom:-260px;right:-140px}}
.wrap{{position:relative;z-index:1}}
/* هدر مشترک */
.head{{display:flex;align-items:center;justify-content:space-between;margin-bottom:34px;flex-direction:row-reverse}}
.head-right{{display:flex;align-items:center;gap:20px;flex-direction:row-reverse}}
.logo{{width:82px;height:82px;border-radius:20px;box-shadow:0 0 0 1px {C['border']},0 12px 40px rgba(62,207,142,.18)}}
.title-block{{text-align:right}}
.kicker{{font-size:14px;letter-spacing:.3em;color:{C['green']};font-weight:700;direction:ltr;text-align:right}}
.title-fa{{font-size:38px;font-weight:900;color:{C['fg']};line-height:1.15;margin-top:5px}}
.sub-fa{{font-size:18px;color:{C['muted']};font-weight:500;margin-top:6px}}
.head-left{{text-align:left;display:flex;flex-direction:column;align-items:flex-end;gap:10px}}
.daynum{{font-size:74px;font-weight:900;line-height:.9;
  background:linear-gradient(160deg,{C['green_bright']},{C['green']} 55%,{C['green_deep']});
  -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}}
.tag{{display:inline-block;border:1.5px solid {C['green_dark']};background:rgba(62,207,142,.06);color:{C['green']};
  border-radius:999px;padding:8px 20px;font-size:14px;font-weight:600}}
.brandline{{margin-top:26px;display:flex;justify-content:space-between;align-items:center;color:{C['faint']};font-size:14px;flex-direction:row-reverse}}
.brandline .site{{color:{C['muted']};direction:ltr;letter-spacing:.12em}}
"""

def _shell(inner, extra_css="", w=1600, h=None):
    return f"""<!DOCTYPE html><html dir="rtl" lang="fa"><head><meta charset="utf-8"><style>
{_base_css()}{extra_css}</style></head><body>
<div class="page" id="page">
<div class="glow glow1"></div><div class="glow glow2"></div>
<div class="wrap">{inner}</div></div></body></html>"""

def _header(kicker, title, sub, right_badge_num=None, tag=None):
    left = '<div class="head-left">'
    if right_badge_num is not None:
        left += f'<div class="daynum">{right_badge_num}</div>'
    if tag:
        left += f'<div class="tag">{tag}</div>'
    left += '</div>'
    logo=_b64(LOGO)
    return f"""<div class="head">
  <div class="head-right"><img class="logo" src="data:image/png;base64,{logo}">
    <div class="title-block"><div class="kicker">{kicker}</div>
      <div class="title-fa">{title}</div><div class="sub-fa">{sub}</div></div></div>
  {left}</div>"""

def _footer():
    return f"""<div class="brandline"><span class="site">ariamir.ir</span>
<span>رتبهٔ ۱ کامپیوتر شریف · کنکور ۱۴۰۶ · مُرشد</span></div>"""

def _render(html, out_path, width=1600, height=1100):
    from playwright.sync_api import sync_playwright
    tmp="/tmp/_morshed_v2.html"; Path(tmp).write_text(html, encoding="utf-8")
    out=Path(out_path); out.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b=p.chromium.launch(args=['--no-sandbox'])
        pg=b.new_page(viewport={'width':width,'height':height}, device_scale_factor=2)
        pg.goto(f'file://{tmp}'); pg.wait_for_timeout(650)
        pg.query_selector('#page').screenshot(path=str(out)); b.close()
    print("saved", out); return str(out)

# ============ کارت ۱: نمای کلی هفته ============
def make_overview(week_title, date_range, tag, days, out_path):
    """days: list of (name, date, hours, [(kind,label),...])"""
    css=f"""
.ogrid{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}}
.ocard{{background:linear-gradient(180deg,{C['surface2']},{C['surface']});border:1px solid {C['border']};
  border-radius:22px;padding:22px 20px;position:relative;overflow:hidden;min-height:236px}}
.ocard::before{{content:'';position:absolute;top:0;right:0;left:0;height:3px;
  background:linear-gradient(90deg,{C['green']},transparent)}}
.ocard.sum{{background:linear-gradient(180deg,rgba(62,207,142,.10),{C['surface']});border-color:{C['green_dark']}}}
.ohead{{display:flex;justify-content:space-between;align-items:baseline;flex-direction:row-reverse;margin-bottom:14px}}
.oname{{font-size:25px;font-weight:900;color:{C['fg']}}}
.odate{{font-size:15px;color:{C['muted']};font-weight:600}}
.ohours{{display:inline-block;color:{C['bg']};background:{C['green']};border-radius:999px;
  padding:5px 15px;font-size:14px;font-weight:700;margin-bottom:16px}}
.olist{{display:flex;flex-direction:column;gap:9px}}
.oitem{{display:flex;align-items:center;flex-direction:row-reverse;gap:10px;
  background:rgba(255,255,255,.02);border:1px solid {C['border']};border-radius:11px;
  padding:9px 12px;font-size:16px;font-weight:500;color:{C['fg']};justify-content:flex-end}}
.oicon{{font-size:12px;flex:none}}
.legend{{display:flex;gap:24px;justify-content:flex-end;flex-direction:row-reverse;margin-top:24px}}
.lg{{display:inline-flex;align-items:center;flex-direction:row-reverse;gap:9px;color:{C['fg2']};font-size:15px;font-weight:600}}
.lgd{{font-size:12px}}
"""
    cards=""
    for name,date,hours,items in days:
        is_sum = (date=="")
        lis=""
        for kind,label in items:
            col,ic=KIND.get(kind,(C['green'],'●'))
            lis+=f'<div class="oitem"><span class="oicon" style="color:{col}">{ic}</span>{label}</div>'
        cls="ocard sum" if is_sum else "ocard"
        head=f'<div class="ohead"><div class="oname">{name}</div><div class="odate">{date}</div></div>'
        cards+=f'<div class="{cls}">{head}<div class="ohours">{hours}</div><div class="olist">{lis}</div></div>'
    leg="".join(f'<span class="lg"><span class="lgd" style="color:{KIND[k][0]}">{KIND[k][1]}</span>{lbl}</span>'
                for k,lbl in [("learn","یادگیری جدید"),("fix","تثبیت/جزوه"),("test","تست"),("review","مرور")])
    inner=(_header("MORSHED · WEEKLY OVERVIEW", f"نمای کلی هفته — {week_title}", date_range, tag=tag)
           +f'<div class="ogrid">{cards}</div><div class="legend">{leg}</div>'+_footer())
    return _render(_shell(inner, css), out_path, height=1080)

# ============ کارت ۲: سهم درس‌ها ============
def make_subjects(title, sub, rows, total_line, out_path):
    """rows: list of (emoji, subject, teacher, hours, sessions, dist, pct)"""
    css=f"""
.panel{{background:linear-gradient(180deg,{C['surface2']},{C['surface']});border:1px solid {C['border']};
  border-radius:24px;overflow:hidden}}
.srow{{display:flex;align-items:center;flex-direction:row-reverse;gap:20px;padding:26px 30px;
  border-bottom:1px solid {C['border']}}}
.srow:last-child{{border-bottom:none}}
.semoji{{font-size:36px;width:56px;text-align:center;flex:none}}
.sinfo{{width:290px;flex:none;text-align:right}}
.sname{{font-size:26px;font-weight:900;color:{C['fg']}}}
.steacher{{font-size:15px;color:{C['muted']};font-weight:500;margin-top:3px}}
.sbar-wrap{{flex:1;display:flex;flex-direction:column;gap:8px}}
.sbar-bg{{height:16px;background:{C['surface2']};border:1px solid {C['border']};border-radius:999px;overflow:hidden;direction:ltr}}
.sbar{{height:100%;border-radius:999px;background:linear-gradient(90deg,{C['green_deep']},{C['green']},{C['green_bright']})}}
.smeta{{display:flex;justify-content:space-between;flex-direction:row-reverse;font-size:15px;color:{C['fg2']}}}
.sstat{{display:flex;flex-direction:column;align-items:center;gap:2px;width:120px;flex:none}}
.sh{{font-size:30px;font-weight:900;color:{C['green']};line-height:1}}
.shl{{font-size:13px;color:{C['muted']};font-weight:600}}
.ss{{font-size:22px;font-weight:700;color:{C['green_bright']};line-height:1}}
.totbar{{margin-top:22px;background:linear-gradient(90deg,rgba(62,207,142,.12),{C['surface']});
  border:1px solid {C['green_dark']};border-radius:18px;padding:22px 28px;text-align:center;
  color:{C['green']};font-size:24px;font-weight:900}}
"""
    tr=""
    for emoji,subj,teacher,hours,sessions,dist,pct in rows:
        tr+=f"""<div class="srow">
          <div class="semoji">{emoji}</div>
          <div class="sinfo"><div class="sname">{subj}</div><div class="steacher">{teacher}</div></div>
          <div class="sbar-wrap"><div class="sbar-bg"><div class="sbar" style="width:{pct}%"></div></div>
            <div class="smeta"><span>{dist}</span></div></div>
          <div class="sstat"><div class="sh">{hours}</div><div class="shl">ساعت</div></div>
          <div class="sstat"><div class="ss">{sessions}</div><div class="shl">جلسه</div></div>
        </div>"""
    inner=(_header("MORSHED · SUBJECT BUDGET", title, sub, tag="هفتهٔ اول مهر")
           +f'<div class="panel">{tr}</div><div class="totbar">{total_line}</div>'+_footer())
    return _render(_shell(inner, css), out_path, height=1080)

# ============ کارت ۳-۹: برنامهٔ روزانه ============
def make_day(daynum, dayname, date_full, tag, focus, hours_total, blocks, out_path):
    """blocks: list of (time, kind, title, note). kind in KIND keys."""
    css=f"""
.dfocus{{display:flex;gap:14px;justify-content:flex-end;flex-direction:row-reverse;margin-bottom:26px;flex-wrap:wrap}}
.fchip{{display:inline-flex;align-items:center;flex-direction:row-reverse;gap:10px;
  background:linear-gradient(180deg,{C['surface2']},{C['surface']});border:1px solid {C['border']};
  border-radius:14px;padding:12px 20px;font-size:19px;font-weight:700;color:{C['fg']}}}
.fchip .fh{{color:{C['green']};font-size:15px;font-weight:600}}
.tl{{position:relative;padding-right:34px}}
.tl::before{{content:'';position:absolute;right:11px;top:8px;bottom:8px;width:2px;
  background:linear-gradient(180deg,{C['green']},{C['border']} 85%)}}
.blk{{position:relative;display:flex;align-items:stretch;flex-direction:row-reverse;gap:20px;margin-bottom:12px}}
.node{{position:absolute;right:-29px;top:24px;width:16px;height:16px;border-radius:50%;
  border:3px solid {C['bg']};z-index:2}}
.card{{flex:1;background:linear-gradient(180deg,{C['surface2']},{C['surface']});border:1px solid {C['border']};
  border-radius:16px;padding:16px 22px;display:flex;align-items:center;flex-direction:row-reverse;gap:18px}}
.card.rest{{background:{C['surface']};border-style:dashed;border-color:{C['faint']}}}
.card.school{{background:rgba(255,255,255,.015);border-color:{C['faint']}}}
.ctime{{width:150px;flex:none;text-align:center;direction:ltr;
  font-size:20px;font-weight:800;color:{C['green']}}}
.cbadge{{width:44px;height:44px;flex:none;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:18px}}
.cbody{{flex:1;text-align:right}}
.ctitle{{font-size:22px;font-weight:700;color:{C['fg']};line-height:1.3}}
.cnote{{font-size:16px;color:{C['fg2']};font-weight:400;margin-top:3px}}
.card.rest .ctitle{{color:{C['fg2']};font-weight:600;font-size:19px}}
.card.school .ctitle{{color:{C['fg2']};font-weight:600}}
.legend{{display:flex;gap:22px;justify-content:flex-end;flex-direction:row-reverse;margin-top:22px}}
.lg{{display:inline-flex;align-items:center;flex-direction:row-reverse;gap:8px;color:{C['fg2']};font-size:15px;font-weight:600}}
.hoursbig{{font-size:15px;color:{C['muted']};font-weight:600;margin-top:6px}}
.hoursbig b{{color:{C['green']};font-size:18px}}
"""
    fchips="".join(f'<span class="fchip">{lbl}<span class="fh">{h}</span></span>' for lbl,h in focus)
    blk=""
    for time,kind,title,note in blocks:
        col,ic=KIND.get(kind,(C['green'],'●'))
        cls="card"
        if kind=="rest": cls="card rest"
        elif kind=="school": cls="card school"
        badge=f'<div class="cbadge" style="background:{col}22;color:{col}">{ic}</div>'
        note_html=f'<div class="cnote">{note}</div>' if note else ''
        blk+=f"""<div class="blk"><div class="node" style="background:{col}"></div>
          <div class="{cls}"><div class="ctime">{time}</div>{badge}
            <div class="cbody"><div class="ctitle">{title}</div>{note_html}</div></div></div>"""
    leg="".join(f'<span class="lg"><span style="color:{KIND[k][0]};font-size:12px">{KIND[k][1]}</span>{lbl}</span>'
                for k,lbl in [("learn","یادگیری"),("fix","تثبیت"),("test","تست"),("review","مرور"),("rest","استراحت")])
    sub=f'{date_full} · <b style="color:{C["green"]}">{hours_total}</b>'
    inner=(_header("MORSHED · DAILY PLAN", f"برنامهٔ {dayname}", sub, right_badge_num=daynum, tag=tag)
           +f'<div class="dfocus">{fchips}</div><div class="tl">{blk}</div><div class="legend">{leg}</div>'+_footer())
    # height auto-ish: base + per block
    h = 360 + len(blocks)*74
    return _render(_shell(inner, css), out_path, height=h)
