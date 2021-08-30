FROM python:3-slim

WORKDIR /http_reverse_heartbeat

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD [ "gunicorn", "-b :8000", "get_to_tg:app" ]
