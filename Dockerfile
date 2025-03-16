# Python 3.11 asosida konteyner yaratamiz
FROM python:3.11

# Tizim paketlarini o‘rnatamiz (sqlite3, venv ishlashi uchun kerak)
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev && \
    rm -rf /var/lib/apt/lists/*

# Ishchi katalogni yaratamiz
WORKDIR /app

# Kerakli fayllarni nusxalash
COPY . .

# Virtual muhitni yaratamiz va kutubxonalarni o‘rnatamiz
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt

# Virtual muhitni faollashtiramiz
ENV PATH="/opt/venv/bin:$PATH"

# Botni ishga tushirish
CMD ["python", "bot1.py"]
