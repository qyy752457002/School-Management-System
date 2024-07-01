FROM docker-hub.f123.pub/lfun/kingbase-drivers:0.3
COPY requirements.txt /
RUN pip install --upgrade pip && pip install -r /requirements.txt && mkdir -p /etc/lfun
COPY deploy/config.json /etc/lfun/config.json
COPY . /app
WORKDIR /app
# RUN python3 main.py db-init upgrade
ENV DEBUG=True
EXPOSE 8080/tcp
CMD ["python3", "main.py", "task"]