#import boto3
import pymysql
import sys
import json
from botocore.exceptions import ClientError


secret_name = "GISecret"
region_name = "us-east-1"

# Create a Secrets Manager client
#session = boto3.session.Session()
#client = session.client(service_name="secretsmanager", region_name=region_name)

#try:
#    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
#except ClientError as e:
    # For a list of exceptions thrown, see
    # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
#    raise e

#secret = get_secret_value_response["SecretString"]

try:
    conn = pymysql.connect(
        host="GI-RDS-Mysql-Instance1",
        user='GIAdmin', #secret["GIDBUser"],
        passwd= 'RndP@ssw25!', #secret["GIDBPass"],
        db='GIRDS1', #secret["GIDbName"],
        connect_timeout=5,
    )
except pymysql.MySQLError as e:
    # logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    # logger.error(e)
    sys.exit(1)

    # logger.info("SUCCESS: Connection to RDS for MySQL instance succeeded")


def lambda_handler(event, context):
    """
    This function creates a new RDS database table and writes records to it
    """
    message = event["Records"][0]["body"]
    data = json.loads(message)
    CustID = data["CustID"]
    Name = data["Name"]

    item_count = 0
    sql_string = f"insert into Customer (CustID, Name) values(%s, %s)"

    with conn.cursor() as cur:
        cur.execute(
            "create table if not exists Customer ( CustID  int NOT NULL, Name varchar(255) NOT NULL, PRIMARY KEY (CustID))"
        )
        cur.execute(sql_string, (CustID, Name))
        conn.commit()
        cur.execute("select * from Customer")
        # logger.info("The following items have been added to the database:")
        for row in cur:
            item_count += 1
            # logger.info(row)
        conn.commit()

        return "Added %d items to RDS for MySQL table" % (item_count)
