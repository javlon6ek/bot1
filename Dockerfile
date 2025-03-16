# Python 3.11 asosida konteyner yaratamiz
FROM python:3.11

# Tizim kutubxonalarini o‘rnatamiz
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev && \
    rm -rf /var/lib/apt/lists/*

# Ishchi katalogni o‘rnatamiz
WORKDIR /app

# `requirements.txt` faylini nusxalash
COPY requirements.txt .

# Python kutubxonalarini o‘rnatamiz
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Barcha loyihani nusxalash
COPY . .

# Botni ishga tushirish
CMD ["python", "bot.py"]
