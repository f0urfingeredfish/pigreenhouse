# pigreenhouse

A small script to log your raspbery pi sense hat sensor data to an amazon dynamodb and save a photo to s3.

Getting Started
---------------

* Install python dependencies `pip install -r requirements.txt`
* Setup boto3 credentials https://github.com/boto/boto3
* Setup a dynamodb table https://aws.amazon.com/documentation/dynamodb/ . Default table name is `Greenhouse`
* Create an s3 bucket to store photos taken when sensor data is logged https://aws.amazon.com/s3/ you will have to change the `s3_bucket` setting in sensor.py https://github.com/f0urfingeredfish/pigreenhouse/blob/master/sensor.py#L16
* Run `python sensor.py`
