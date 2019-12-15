FROM python:3.8 AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ARG SPACY_MODEL
ENV PYTHONBUFFERED=1 SENSE2VEC=0 SPACY_MODEL=$SPACY_MODEL
RUN python -m spacy download $SPACY_MODEL
COPY src/main.py .
EXPOSE 8000
HEALTHCHECK --timeout=2s --start-period=2s --retries=1 \
    CMD curl -f http://localhost:8000/health_check
RUN useradd user
USER user
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]

FROM base
ENV SENSE2VEC 1
COPY src/s2v_old/ src/s2v_old/