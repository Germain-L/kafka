from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.datastream.connectors import FlinkKafkaConsumer
from pyflink.datastream.window import TumblingProcessingTimeWindows
import time 

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_stream_time_characteristic(TimeCharacteristic.ProcessingTime)

    properties = {
        'bootstrap.servers': 'kafka:9092',
        'group.id': 'flink-group'
    }

    kafka_consumer = FlinkKafkaConsumer(
        topics='vitesse_moyenne',
        deserialization_schema=SimpleStringSchema(),
        properties=properties
    )

    def parse_data(data):
        key, value = data.split(',')
        return (key, float(value))

    stream = env.add_source(kafka_consumer) \
        .map(parse_data, output_type=Types.TUPLE([Types.STRING(), Types.FLOAT()])) \
        .key_by(lambda x: x[0]) \
        .window(TumblingProcessingTimeWindows.of(time.minutes(5))) \
        .reduce(lambda a, b: (a[0], (a[1] + b[1]) / 2))

    stream.print()

    env.execute("Kafka Flink Python Example")

if __name__ == '__main__':
    main()
