## Build an air quality anomaly detector using Amazon Lookout for Metrics
Today, air pollution is a familiar environmental issue that creates severe respiratory and heart conditions, which pose serious health threats. Acid rain, depletion of the ozone layer, and global warming are also adverse consequences of air pollution. There is a need for intelligent monitoring and automation in order to prevent severe health issues and in extreme cases life-threatening situations. Air quality is measured using the concentration of pollutants in the air. Identifying symptoms early and controlling the pollutant level before it’s dangerous is crucial. The process of identifying the air quality and the anomaly in the weight of pollutants, and quickly diagnosing the root cause, is difficult, costly, and error-prone.

The process of applying AI and machine learning (ML)-based solutions to find data anomalies involves a lot of complexity in ingesting, curating, and preparing data in the right format and then optimizing and maintaining the effectiveness of these ML models over long periods of time. This has been one of the barriers to quickly implementing and scaling the adoption of ML capabilities.

This post shows you how to use an integrated solution with Amazon Lookout for Metrics and Amazon Kinesis Data Firehose to break these barriers by quickly and easily ingesting streaming data, and subsequently detecting anomalies in the key performance indicators of your interest.

Lookout for Metrics automatically detects and diagnoses anomalies (outliers from the norm) in business and operational data. It’s a fully managed ML service that uses specialized ML models to detect anomalies based on the characteristics of your data. For example, trends and seasonality are two characteristics of time series metrics in which threshold-based anomaly detection doesn’t work. Trends are continuous variations (increases or decreases) in a metric’s value. On the other hand, seasonality is periodic patterns that occur in a system, usually rising above a baseline and then decreasing again. You don’t need ML experience to use Lookout for Metrics.

We demonstrate a common air quality monitoring scenario, in which we detect anomalies in the pollutant concentration in the air. By the end of this post, you’ll learn how to use these managed services from AWS to help prevent health issues and global warming. You can apply this solution to other use cases for better environment management, such as detecting anomalies in water quality, land quality, and power consumption patterns, to name a few.

## Solution overview
The following diagram illustrates our solution architecture.
![Architecture](/image/ML-7925-image001-revised.png)

## Prerequisites

You need the following prerequisites before you can proceed with solution. For this post, we use the us-east-1 Region.

   + Download the Python script (publish.py) and data file from the repository.
   + Open the live_data.csv file in your preferred editor and replace the dates to be today’s and tomorrow’s date. For example, if today’s date is July 8, 2022, then replace 2022-03-25 with 2022-07-08. Keep the format the same. This is required to simulate sensor data for the current date using the IoT simulator script.
   + Create an Amazon Simple Storage Service (Amazon S3) bucket and a folder named air-quality. Create a subfolder inside air-quality named historical. For instructions, see Creating a folder.
   + Upload the live_data.csv file in the root S3 bucket and historical_data.json in the historical folder.
   + Create an AWS Cloud9 development environment, which we use to run the Python simulator program to create sensor data for this solution.


## Configure AWS IoT Core and run the air quality simulator program

  + On the AWS IoT Core console, create an AWS IoT policy called admin.
  + In the navigation pane under Message Routing, choose Rules.
  + Choose Create rule.
  + Create a rule with the Kinesis Data Firehose(firehose) action.
     This sends data from an MQTT message to a Kinesis Data Firehose delivery stream.
 + Choose Create.
![IOT Rule](/image/ML-7925-image011.png)

  + Create an AWS IoT thing with name Test-Thing and attach the policy you created.
  + Download the certificate, public key, private key, device certificate, and root CA for AWS IoT Core.
  + Save each of the downloaded files to the certificates subdirectory that you created earlier.
![IOT Simulator](/image/ML-7925-image013.png)

  + Upload publish.py to the iot-test-publish folder.
  + On the AWS IoT Core console, in the navigation pane, choose Settings.
  + Under Custom endpoint, copy the endpoint.
  + This AWS IoT Core custom endpoint URL is personal to your AWS account and Region.
  + Replace customEndpointUrl with your AWS IoT Core custom endpoint URL, certificates with the name of certificate, and Your_S3_Bucket_Name with your S3 bucket name.
  + Next, you install pip and the AWS IoT SDK for Python.
  + Log in to AWS Cloud9 and create a working directory in your development environment. For example: aq-iot-publish.
  + Create a subdirectory for certificates in your new working directory. For example: certificates.
  + Install the AWS IoT SDK for Python v2 by running the following from the command line. 

   *pip install awsiotsdk*
   
To test the data pipeline, run the following command: 

   *python3 publish.py*
   
You can see the payload in the following screenshot.

![Payload](/image/ML-7925-image015.png)

Finally, the data is delivered to the specified S3 bucket in the prefix structure.
![Data Files](/image/ML-7925-image017.png)

The data of the files is as follows:

    {"TIMESTAMP":"2022-03-20 00:00","LOCATION_ID":"B-101","CO":2.6,"SO2":62,"NO2":57}
    {"TIMESTAMP":"2022-03-20 00:05","LOCATION_ID":"B-101","CO":3.9,"SO2":60,"NO2":73}

The timestamps show that each file contains data for 5-minute intervals.

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

