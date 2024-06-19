
# 事务统计  总数 成功 失败 数量  todo
class StatisticsCollector:
    def __init__(self, ):
        self.transaction_count = 0
        self.failure_count = 0
        self.success_count = 0

    def handle_transaction_event(self, ):
        self.transaction_count += 1

    def handle_failure_event(self, ):
        self.failure_count += 1

    def handle_success_event(self, ):
        self.success_count += 1


class KafkaStatisticsReporter:
    def __init__(self, kafka_producer: 'KafkaProducer', topic: str):
        self.kafka_producer = kafka_producer
        self.topic = topic

    def report(self, statistics: dict):
        self.kafka_producer.send(self.topic, statistics)
