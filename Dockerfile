FROM docker-hub.f123.pub/lfun/kingbase-drivers:0.3
COPY requirements.txt /
RUN pip install --upgrade pip && pip install -r /requirements.txt && pip install gunicorn
RUN mkdir -p /etc/lfun
COPY deploy/config.json /etc/lfun/config.json
COPY . /app
WORKDIR /app
RUN python3 main.py db-init upgrade
ENV DEBUG=True
EXPOSE 8080/tcp
CMD ["uvicorn", "wsgi:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]