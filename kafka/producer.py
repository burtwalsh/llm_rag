from kafka import KafkaProducer
import json, time, random

producer = KafkaProducer(bootstrap_servers='kafka:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

while True:
    msg = {
        "id": random.randint(1, 1000),
        "timestamp": int(time.time()),
        "location": random.choice(["NY", "SF", "LA"]),
        "temperature": round(random.uniform(60, 100), 2),
        "status": random.choice(["nominal", "alert"])
    }
    producer.send("raw-stream", msg)
    print("Sent:", msg)
    time.sleep(1)
