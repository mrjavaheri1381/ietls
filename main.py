import requests
import time

# === تنظیمات تلگرام ===
BOT_TOKEN = "7912298823:AAFVQ_i1dUUJYyqeoGNC1ke8XNu-McIb_qY"
CHAT_ID1 = "209989818"
CHAT_ID2 = "1251595561"

# === تنظیمات درخواست به IELTS ===
url = "https://api.session-search.prod.ielts.com/v2/sessions/search"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Content-Type": "application/json",
    "Origin": "https://bxsearch.ielts.idp.com",
    "Connection": "keep-alive",
    "Referer": "https://bxsearch.ielts.idp.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "TE": "trailers"
}

payload = {
    "dayOfPaperTest": 0,
    "languageSkills": ["L", "R", "W"],
    "order": "A",
    "page": 1,
    "pageSize": 25,
    "sortBy": "TEST_START_DATE",
    "timesOfDay": ["MORNING", "AFTERNOON"],
    "fromTestStartDateLocal": "2025-11-01",
    "toTestStartDateLocal": "2025-11-30",
    "countryCode": "ARM",
    "city": "Yerevan",
    "testDeliveryFormats": ["CD"],
    "testCategories": ["IELTS"],
    "testModules": ["ACADEMIC"]
}

# === تابع برای ارسال پیام تلگرام ===
def send_telegram_message(text, CHAT_ID):
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}

    for attempt in range(10):
        try:
            res = requests.post(telegram_url, data=payload, timeout=20)
            if res.status_code == 200:
                print("✅ Message sent to Telegram!")
                break
            else:
                print(f"⚠️ Telegram response: {res.status_code}")
        except Exception as e:
            print("⚠️ Error sending message:", e)
            time.sleep(1)  # صبر قبل از تلاش دوباره

# === حلقه اصلی (هر ۳۰ ثانیه) ===
print("🚀 IELTS session monitor started... (every 30s)")
while True:
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        data = response.json()
        items = data.get('items', [])

        if items:
            message = "📢 IELTS test sessions found!\n\n"
            for item in items:
                loc = item['testLocation']['name']
                date = item['testStartLocalDatetime'][:10]
                message += f"🏫 {loc} — 📅 {date}\n"

            send_telegram_message(message,CHAT_ID2)
            send_telegram_message(message,CHAT_ID1)
        else:
            print("❌ No sessions found this time.")

    except Exception as e:
        print("⚠️ Error checking IELTS sessions:", e)

    time.sleep(60)
