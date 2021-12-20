FROM python:3.8

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
COPY migrations/ /app/migrations/
COPY flaskr/ /app/flaskr/

EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "-w", "4", "app:app"]