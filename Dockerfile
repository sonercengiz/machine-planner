# Resmi Python imajından başla (hafif bir sürüm kullan)
FROM python:3.12-slim

# Ortam değişkenleri
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Sistem gereksinimlerini yükle
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Çalışma dizini oluştur
WORKDIR /app

# Gereksinim dosyalarını kopyala ve kur
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Varsayılan komut (uvicorn ile başlatma)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
