FROM python:3.7
WORKDIR /app
ENV PYTHONUNBUFFERED 1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
COPY s2v_old/ s2v_old/
EXPOSE 8000
HEALTHCHECK --timeout=2s --start-period=2s --retries=1 \
    CMD curl -f http://localhost:8000/health_check
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]