FROM python:3.12-slim

WORKDIR /app

# System deps for LightGBM
RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cloud Run provides PORT env var (default 8080)
# API runs internally on 8000, Streamlit faces the internet on $PORT
ENV PORT=8080
EXPOSE 8080

CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port 8000 & streamlit run app/dashboard.py --server.port $PORT --server.address 0.0.0.0 --server.headless true"
