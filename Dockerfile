# ./Dockerfile
FROM python:3.11-slim

# جلوگیری از نوشتن فایل‌های pyc و فعال کردن خروجی آنی
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# نصب وابستگی‌های سیستمی لازم برای pip (در صورت نیاز به بسته‌های باینری)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# کپی کردن requirements و نصب پکیج‌ها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# اضافه کردن کد پروژه
COPY . .

# اجرای کانتینر به عنوان یوزر غیر روت
RUN useradd -m appuser || true
RUN chown -R appuser:appuser /app
USER appuser

# دستور پیش‌فرض برای اجرای اسکریپت
CMD ["python", "main.py"]
