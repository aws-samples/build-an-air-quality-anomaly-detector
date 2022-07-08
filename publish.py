from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json
import pandas as pd
import json
import os
import boto3
import csv


# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "customEndpointUrl"
CLIENT_ID = "testDevice"
PATH_TO_CERTIFICATE = "certificates/123-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certificates/123-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certificates/root.pem"
#MESSAGE = data
TOPIC = "test/testing"
RANGE = 20

####################### Reading from File ###############
# importing the boto3 library 
import boto3
import csv
import json
import codecs
import datetime 
from datetime import timedelta
# declare S3 variables and read the CSV content from S3 bucket.
targetBucket = 'Your_S3_Bucket_Name'
csvFile = 'live_data_sample.csv'
s3_client = boto3.client(service_name='s3')
# get S3 object
result = s3_client.get_object(Bucket=targetBucket, Key=csvFile) 
csv_content = result['Body'].read().splitlines()
# use CSV reader to read the object and decode the contents.
read = csv.reader(codecs.iterdecode(csv_content, 'utf-8'))
line="test"
while(True):
# convert from CSV to JSON format.
   
    for x in read:
        current_time = datetime.datetime.now()
        current_date = str(current_time.date())
        current_hour = str(current_time.hour)
        current_minute = str(current_time.minute-((current_time.minute) % 5))
        current_timestamp_str = current_date + " " + current_hour +":" + current_minute
        current_timestamp = datetime.datetime.strptime(current_timestamp_str,'%Y-%m-%d %H:%M')
        record_timestamp = datetime.datetime.strptime(str(x[0]),'%Y-%m-%d %H:%M') 
    
        if(record_timestamp == current_timestamp):
            timestamp =  (x[0])
            location_id = (x[1])
            CO = float(x[2])
            SO2 = int(x[3])
            NO2 = int(x[4])
            y = { "TIMESTAMP":  timestamp ,
                "LOCATION_ID":  location_id , 
                "CO":  CO , 
                "SO2":  SO2 , 
                "NO2":  NO2 }
            line = y
            print("found",record_timestamp)
        
    ######################End Reading #######################
    
            # Spin up resources
            event_loop_group = io.EventLoopGroup(1)
            host_resolver = io.DefaultHostResolver(event_loop_group)
            client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
            mqtt_connection = mqtt_connection_builder.mtls_from_path(
                        endpoint=ENDPOINT,
                        cert_filepath=PATH_TO_CERTIFICATE,
                        pri_key_filepath=PATH_TO_PRIVATE_KEY,
                        client_bootstrap=client_bootstrap,
                        ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
                        client_id=CLIENT_ID,
                        clean_session=False,
                        keep_alive_secs=6
                        )
            print("Connecting to {} with client ID '{}'...".format(
                    ENDPOINT, CLIENT_ID))
            # Make the connect() call
            connect_future = mqtt_connection.connect()
            # Future.result() waits until a result is available
            connect_future.result()
            print("Connected!")
            # Publish message to server desired number of times.
            print('Begin Publish')
            message = line
            print(message)
            mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
            print("Published: '" + json.dumps(message) + "' to the topic: " + "'test/testing'")
            print('Publish End')
            disconnect_future = mqtt_connection.disconnect()
            disconnect_future.result()
            print('Sleeping')
            t.sleep(300)