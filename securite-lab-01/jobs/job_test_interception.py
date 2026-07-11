from pyspark.sql import SparkSession


ENDPOINT = "http://minio:9000"
SSL = "false"
BUCKET = "anfa-raw"


spark = (
    SparkSession.builder.appName("TestInterception")
    .config("spark.hadoop.fs.s3a.endpoint", ENDPOINT)
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", SSL)
    .config("spark.hadoop.fs.s3a.access.key", "anfa-app-key")
    .config("spark.hadoop.fs.s3a.secret.key", "anfa-app-secret-2026")
    .config("spark.hadoop.fs.s3a.path.style.access", "true")
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .getOrCreate()
)

df = spark.createDataFrame([(1, "donnee_test_interception")], ["id", "valeur"])
df.write.mode("overwrite").parquet(f"s3a://{BUCKET}/test-interception/")

print("Ecriture terminee.")
spark.stop()
