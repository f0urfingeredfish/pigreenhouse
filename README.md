# pigreenhouse

A small script to log your raspbery pi sense hat sensor data to an amazon dynamodb and save a photo to s3.
This is the start of my 'smart' greenhouse project. The goal is to have time lapse images and graphed sensor data of the greenhouse.

Hardware
--------
* Raspi 3 https://www.raspberrypi.org/products/raspberry-pi-3-model-b/
* Sense Hat https://www.raspberrypi.org/products/sense-hat/
* Camera module v2 https://www.raspberrypi.org/products/camera-module-v2/

Getting Started
---------------

* Install python dependencies `pip install -r requirements.txt`
* Setup aws boto3 credentials https://github.com/boto/boto3
* Setup a dynamodb table https://aws.amazon.com/documentation/dynamodb/ . Default table name is `Greenhouse`
* Create an s3 bucket to store photos taken when sensor data is logged https://aws.amazon.com/s3/ you will have to change the `s3_bucket` setting in sensor.py https://github.com/f0urfingeredfish/pigreenhouse/blob/master/sensor.py#L16
* Add credentials to access the table and s3 https://aws.amazon.com/iam/
* Run `python sensor.py`
* The sense hat led will show a green smiley face on success and then a green dot as well as standard output. If there is an error or you lose connection to amazon it will display a red led. The script won't exit but will try again at the set logging interval.

Sample Output
------
```bash
pi@raspberrypi:~/pigreenhouse $ python sensor.py 
photos/2017-04-14 04:47:38.072222.jpg  55145 / 55145.0  (100.00%)saved photo to s3
temperature_from_pressure: 33.15625, photo: 2017-04-14 04:47:38.072222.jpg, pressure: 903.913330078, compass: 148.917931455, date: 1492145259, temperature_from_humidity: 34.7334594727, humidity: 29.9232330322, temperature: 34.7334594727, log: 2017-04-14 04:47:38.072222, cpu_temp: 58.0, gpu_temp: 57.996
log saved to database
```
