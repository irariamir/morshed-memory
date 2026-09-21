# 📲 TELEGRAM — راهنمای ربات و کانال‌ها

> ⚠️ **توکن‌ها و شناسه‌ها اطلاعات حساس‌اند و در این فایل ذخیره نمی‌شوند.** آنها را از آریامیر بگیر.

## اجزا
- **ربات:** MORSHED (@AR_STUDYAGENTBOT) — ادمین هر دو کانال.
- **کانال برنامه‌ها (اصلی):** «MORSHED» — مرشد کارت برنامه را اینجا می‌فرستد.
- **کانال منبع:** «MORSHED-SOURSES» — آریامیر عکس سرفصل/مباحث را اینجا می‌فرستد؛ مرشد دریافت و تحلیل می‌کند.

## گردش کار
1. مرشد برنامه (متن + کارت عکس) را در کانال اصلی می‌فرستد.
2. آریامیر در چت گزارش می‌دهد.
3. مرشد پیام کانال را **ویرایش می‌کند** و زیر کارهای انجام‌شده ✅ می‌زند.

## دستورهای API (نمونه)
```bash
TOKEN="<از آریامیر بگیر>"
CHAT="<شناسه کانال اصلی>"       # مثال ساختار: -100xxxxxxxxxx
SRC="<شناسه کانال منبع>"

# ارسال متن
curl -s "https://api.telegram.org/bot$TOKEN/sendMessage" \
  --data-urlencode "chat_id=$CHAT" --data-urlencode "text=..."

# ارسال عکس کارت
curl -s "https://api.telegram.org/bot$TOKEN/sendPhoto" \
  -F "chat_id=$CHAT" -F "photo=@plans/cards/plan_card_XXXX.png" -F "caption=..."

# ویرایش پیام (برای تیک زدن)
curl -s "https://api.telegram.org/bot$TOKEN/editMessageText" \
  --data-urlencode "chat_id=$CHAT" --data-urlencode "message_id=<ID>" \
  --data-urlencode "text=..."

# دریافت عکس‌های کانال منبع
curl -s "https://api.telegram.org/bot$TOKEN/getUpdates"
# سپس getFile با file_id و دانلود از https://api.telegram.org/file/bot$TOKEN/<file_path>
```

## نکته
- ربات‌ها به تاریخچهٔ قبلیِ کانال دسترسی مستقیم ندارند؛ وقتی آریامیر عکس فرستاد، در چت خبر بدهد تا با getUpdates دریافت شود.
- لاگ پیام‌های ارسالی (message_id ها) در `memory/student_profile.md` بخش Telegram Integration نگه‌داری می‌شود.
