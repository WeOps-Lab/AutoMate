from core.logger import logger

try:
    import simplejson as json
except ImportError:
    import json

from kafka import KafkaConsumer, KafkaProducer
from kafka.coordinator.assignors.range import RangePartitionAssignor
from kafka.coordinator.assignors.roundrobin import RoundRobinPartitionAssignor

default_key = "000000"


class ConsumerQueue(object):
    def __init__(self, bootstrap_servers, topic, group_id, client_id):
        self.client = KafkaConsumer(
            topic,
            client_id=client_id,
            group_id=group_id,
            bootstrap_servers=bootstrap_servers,
            partition_assignment_strategy=[RangePartitionAssignor, RoundRobinPartitionAssignor],
        )

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            try:
                item = next(self.client)
                logger.debug(
                    "获取到kafka消息: [topic: %s][partition: %s][offset: %s][key: %s][value: %s]"
                    % (item.topic, item.partition, item.offset, item.key, item.value)
                )

                value = json.loads(item.value)
                return value
            except Exception as e:
                logger.warning("获取到格式错误的消息：[error: {}]".format(e), exc_info=True)


class ProducerQueue(object):
    def __init__(self, bootstrap_servers):
        def partitioner(key_bytes, all_partitions, available_partitions):
            return int(key_bytes) % len(available_partitions)

        self.client = KafkaProducer(bootstrap_servers=bootstrap_servers, acks="all", partitioner=partitioner)

    def push(self, topic, msg):
        try:
            # key 区别分区
            if isinstance(msg, dict):
                self.client.send(
                    topic=topic, key=str(msg.get("key", default_key)).encode(), value=json.dumps(msg).encode()
                )
            elif isinstance(msg, str):
                self.client.send(topic=topic, key=default_key.encode(), value=msg.encode())
            else:
                logger.warning("推送的消息格式错误: [msg: {}][msg_type: {}]".format(msg, type(msg)))
        except Exception as e:
            logger.warning("推送消息失败: [error: {}]".format(e), exc_info=True)
