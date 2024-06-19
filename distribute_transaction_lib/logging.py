import logging

# todo 成功 失败 的日志记录

class Logger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        # 设置日志记录
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def handle_failure_event(self, event):
        self.logger.error(f"Task failed: {event}, ")

    def handle_success_event(self, event):
        self.logger.info(f"Task succeeded: {event}")


class KafkaHandler(logging.Handler):
    def __init__(self, kafka_producer: 'KafkaProducer', topic: str):
        super().__init__()
        self.kafka_producer = kafka_producer
        self.topic = topic

    def emit(self, record):
        msg = self.format(record)
        self.kafka_producer.send(self.topic, msg.encode('utf-8'))
