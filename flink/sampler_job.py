from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer
import json

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)

kafka_source = FlinkKafkaConsumer(
    topics='raw-stream',
    deserialization_schema=SimpleStringSchema(),
    properties={'bootstrap.servers': 'kafka:9092', 'group.id': 'flink-group'}
)

ds = env.add_source(kafka_source)

def sample_filter(value):
    data = json.loads(value)
    return data['status'] != "nominal"

ds.filter(sample_filter).print()

env.execute("Stream Sampler")
