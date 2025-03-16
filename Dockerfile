# Python 3.11 asosida konteyner yaratamiz
FROM python:3.11

# Tizim paketlarini o‘rnatamiz (sqlite3 ishlashi uchun kerak)
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev && \
    rm -rf /var/lib/apt/lists/*

# Ishchi katalogni yaratamiz
WORKDIR /app

# Kerakli fayllarni nusxalash
COPY . .


# Botni ishga tushirish
CMD ["python", "bot1.py"]
