from kafka import KafkaConsumer
import psycopg2
import json

def kafka_to_postgres():
    consumer = KafkaConsumer(
        'transactions',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        group_id='etl_group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Deserialize JSON
    )
    conn = psycopg2.connect(
        database="ecommerce",
        user="user",
        #password="password",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    for message in consumer:
        data = message.value
        print(data)  # Debugging: print the structure of the data
        try:
            cursor.execute("""
                INSERT INTO transactions (customer_id, customer_firstname, customer_lastname, gender, birthdate, amount, purchase_date, merchant_name, category)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (data['customer_id'], data['customer_firstname'], data['customer_lastname'], data['gender'], data['birthdate'], data['amount'], data['purchase_date'], data['merchant_name'], data['category']))
            conn.commit()
            print(f"Inserted: {data}")
        except KeyError as e:
            print(f"Missing key in data: {e}")
        except Exception as e:
            print(f"Error inserting data: {e}")
            conn.rollback()
            
    consumer.close()
    conn.close()

if __name__ == "__main__":
    kafka_to_postgres()