FROM python:3.12-slim

# 1. Root ke bajaye /app folder use karein (Safe)
WORKDIR /app

# 2. Requirements pehle copy karein
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 3. Baqi code copy karein
COPY . .

# 4. Port expose
EXPOSE 8000

# 5. Command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]