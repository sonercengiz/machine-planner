## alembic migration oluşturma
alembic revision --autogenerate -m "initial schema"

## alembic migration uyarlama
alembic upgrade head

## alembic migration zincirini gör
alembic history

## veritabanı hangi migration’da
alembic current

## env'yi aktive et
export ENV_FILE=".env.dev"

## uygulamayı çalıştır
python3 -m uvicorn app.main:app --reload


docker build --platform linux/amd64 -t sonercengiz/machine-planner-backend:latest .
docker push sonercengiz/machine-planner-backend:latest

sonercengiz
wWahtER9Sr!D3jl8Z7Hh