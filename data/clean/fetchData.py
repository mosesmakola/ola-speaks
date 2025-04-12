import snowflake.connector
from dotenv import load_dotenv
import os
import json
import boto3

load_dotenv()

SF_USER = os.environ["SNOWFLAKE_USER"]
SF_PASSWORD = os.environ["SNOWFLAKE_PASSWORD"]
SF_ACCOUNT = os.environ["SNOWFLAKE_ACCOUNT"]

AWS_ACCESS = os.environ["AWS_ACCESS"]
AWS_SECRET = os.environ["AWS_SECRET"]

with open ("../raw/bible_raw_data.json") as infile:
    data = json.load(infile)

with open("../raw/bible_flat_raw.json", "w") as outfile:
    for row in data:
        json.dump(row, outfile)
        outfile.write("\n")

bucket_name = "ola-speaks"
s3_file_path = "language_text_data/bible_raw.json"

s3 = boto3.client("s3", aws_access_key_id=AWS_ACCESS, aws_secret_access_key=AWS_SECRET)
s3.upload_file("../raw/bible_flat_raw.json", bucket_name, s3_file_path)

conn = snowflake.connector.connect(
    user = SF_USER,
    password = SF_PASSWORD,
    account = SF_ACCOUNT
)

conn.cursor().execute("USE WAREHOUSE olaspeaks")
conn.cursor().execute("USE DATABASE text_language_data")
conn.cursor().execute("USE SCHEMA bible")

conn.cursor().execute(
    "CREATE OR REPLACE FILE FORMAT json_format "
    "TYPE = JSON;"
)

conn.cursor().execute(f"""
    CREATE OR REPLACE STAGE bible_stage
    URL = 's3://ola-speaks/language_text_data/'
    CREDENTIALS = (
        AWS_KEY_ID = '{AWS_ACCESS}',
        AWS_SECRET_KEY = '{AWS_SECRET}'
    )
    FILE_FORMAT = json_format;
""")

conn.cursor().execute(
    "CREATE OR REPLACE TABLE "
    "raw_bible(book string, chapter integer, verse integer, eng string, lin string, yor string)"
)

conn.cursor().execute("""
    COPY INTO raw_bible
    FROM (
        SELECT 
            $1:book::STRING,
            $1:chapter::INTEGER,
            $1:verse::INTEGER,
            $1:eng::STRING,
            $1:lin::STRING,
            $1:yor::STRING
        FROM @bible_stage/bible_raw.json
    );
""")

for row in conn.cursor().execute("SELECT * FROM raw_bible LIMIT 5;").fetchall():
    print(row)


# conn.cursor().execute(
#     "CREATE OR REPLACE STAGE stage "
#     "FILE_FORMAT = json_format"
# )
# conn.cursor().execute(
#     "PUT file:// "
# )

# conn.cursor().execute("")





# print(raw_bible[0]["eng"])