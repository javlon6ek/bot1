FROM python:3.11

# Tizim kutubxonalarini o‘rnatish
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev

# Ishchi katalogni yaratish
WORKDIR /app

# Kerakli fayllarni nusxalash
COPY . .

# Virtual muhit yaratish va bog‘lamalar o‘rnatish
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["python", "bot1.py"]
