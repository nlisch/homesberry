# homesberry
Build your own google home with a raspberry ! Ask your google analytics real time stats,  connect to arduino to create an motion alarm, using Google cloud speech API.
You can also ask temperature of the room after connecting your raspberry to Arduino.
This script will also send text using twilio api if anything happened with the motion sensor.

## Python Version

2.7


## Environment Variables Required 

To execute the scripts you need to add `.env` file to the root of the project with these variables (values are examples):

A google Cloud platform project needs to be set up first.

```
## Google Cloud
ACCOUNT_EMAIL=XXXX
API_TOKEN_P12=XXXX.p12

## Twilio
TEL_FROM = XXXX
TEL_TO = XXXX
TWILLIO_ACCOUNT_ID = XXXX
TWILIO_TOKEN = XXXX

```
