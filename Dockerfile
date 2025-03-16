# Python 3.11 versiyasidan foydalanamiz
FROM python:3.11

# Ishchi katalogni yaratamiz
WORKDIR /app

# Kerakli fayllarni konteyner ichiga nusxalaymiz
COPY . .

# Pip va kutubxonalarni yangilaymiz
RUN pip install --no-cache-dir -r requirements.txt

# Botni ishga tushirish
CMD ["python", "bot.py"]
