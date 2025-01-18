from pyspark.sql import SparkSession
import time

# Create a SparkSession
spark = SparkSession.builder \
    .appName("Performance Comparison") \
    .getOrCreate()

# Load a large CSV file
df = spark.read.csv("/home/vignesh/Downloads/people-10000.csv", header=True, inferSchema=True)

# Cache the DataFrame to avoid re-computation
df.cache()

# Record the start time for grouping and aggregation (Transformation)
start_time = time.time()
grouped_df = df.groupBy("Sex").count()
end_time = time.time()
print(f"Time taken for grouping and aggregation (Transformation): {end_time - start_time:.2f} seconds")

# Perform an action: collect() on filtered DataFrame
start_time = time.time()
collected_data = df.collect()
end_time = time.time()
print(f"Time taken for collect() (Action): {end_time - start_time:.2f} seconds")

# Perform an action: count() on grouped DataFrame
start_time = time.time()
row_count = grouped_df.count()
end_time = time.time()
print(f"Time taken for count() (Action): {end_time - start_time:.2f} seconds")

# Perform an action: show() on grouped DataFrame
start_time = time.time()
grouped_df.show()
end_time = time.time()
print(f"Time taken for show() (Action): {end_time - start_time:.2f} seconds")

# Keep Spark UI active
print("Spark UI is active at http://<your-hostname>:4040. Press Ctrl+C to exit.")
try:
    while True:
        pass  # Keep the program alive to allow UI inspection
except KeyboardInterrupt:
    print("\nStopping Spark Session...")
    spark.stop()  # Stop Spark when you manually terminate
