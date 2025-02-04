FROM docker-hub.f123.pub/lfun/kingbase-drivers:0.3
COPY requirements.txt /
RUN pip install --upgrade pip && pip install -r /requirements.txt && pip install gunicorn && mkdir -p /etc/lfun
COPY deploy/config.json /etc/lfun/config.json
COPY . /app
COPY deploy/token_jwt_key.key /app/cert/token_jwt_key.key

WORKDIR /app
ENV DEBUG=True
EXPOSE 8080/tcp
CMD ["uvicorn", "wsgi:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]