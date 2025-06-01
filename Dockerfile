FROM python:3.12-slim

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && \
    apt update && apt install git -y && \
    rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app

CMD ["gunicorn", "--config", "gunicorn.py", "core_app.wsgi:application"]
