FROM python:3.7
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
HEALTHCHECK --timeout=2s --start-period=2s --retries=1 \
    CMD curl -f http://localhost:8080/health_check
CMD ["sh", "-c", "waitress-serve --port 8080 app:app"]