# todo 监控 成功失败的统计

class Monitor:
    def __init__(self,  ):
        self.failure_count = 0
        self.success_count = 0

    def handle_failure_event(self, ):
        self.failure_count += 1

    def handle_success_event(self, ):
        self.success_count += 1


class KafkaMetricsReporter:
    def __init__(self, kafka_producer: 'KafkaProducer', topic: str):
        self.kafka_producer = kafka_producer
        self.topic = topic

    def report(self, metrics: dict):
        self.kafka_producer.send(self.topic, metrics)
