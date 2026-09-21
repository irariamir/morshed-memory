# 🔐 Encrypted Vault

`vault.enc` شامل اطلاعات حساس (توکن گیت‌هاب، توکن ربات تلگرام، شناسهٔ کانال‌ها) است که با **AES-256-CBC + PBKDF2 (۱٬۰۰۰٬۰۰۰ تکرار، SHA-256)** رمزنگاری شده. بدون رمز، غیرقابل‌خواندن است.

## رمزگشایی
```bash
openssl enc -d -aes-256-cbc -pbkdf2 -iter 1000000 -md sha256 \
  -in secrets/vault.enc -pass pass:'РАЗ_РМЗ_را_اینجا_بگذار'
```
یا به‌صورت تعاملی (امن‌تر، رمز در تاریخچه نمی‌ماند):
```bash
openssl enc -d -aes-256-cbc -pbkdf2 -iter 1000000 -md sha256 -in secrets/vault.enc
```

## رمزگذاری دوباره (بعد از تغییر)
```bash
openssl enc -aes-256-cbc -salt -pbkdf2 -iter 1000000 -md sha256 \
  -in plaintext.txt -out secrets/vault.enc
```

⚠️ رمز نزد آریامیر است و هرگز در این ریپو نوشته نمی‌شود.
