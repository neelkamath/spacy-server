FROM python:3
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENV PORT 8080
EXPOSE 8080
HEALTHCHECK --timeout=2s --start-period=2s --retries=1 \
    CMD curl -f http://localhost:$PORT/health_check
CMD ["sh", "-c", "waitress-serve --port $PORT app:app"]