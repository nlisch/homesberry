
# coding: utf-8

# In[1]:

from google.cloud import speech
client = speech.Client()
import time
import io
import pyaudio
import wave
from gtts import gTTS
import os
import sys

import random 
import subprocess
import serial
import requests


# In[2]:

def open_COM3():
    global ser
    ser = serial.Serial('COM3', 9600, timeout=0)
def green_record():
    ser.write('H')
def red_done_recording():
    ser.write('L')
def close_COM3():
    ser.close()


# In[3]:

open_COM3()


# In[ ]:

def record_voice():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")
    green_record() 

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")
    time.sleep(1)
    red_done_recording()

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    
#record_voice()


# In[ ]:

def transcribe_voice(speech_file):
    global talk 
    talk = []
    """Transcribe the given audio file."""
    from google.cloud import speech
    speech_client = speech.Client()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()
        #content = base64.b64encode(content)
        audio_sample = speech_client.sample(
            content=content,
            source_uri=None,
            encoding='LINEAR16')

    try :
        alternatives = audio_sample.recognize('fr-fr')
        for alternative in alternatives:
            test = (alternative.transcript).encode('utf-8')
            print('Transcript: ' + str(test))
            talk.append(str(test))
            talk = ','.join(talk)
            talk = talk.split(' ')
    except:
        talk.append("")
    
        
#transcribe_voice('C:\Users\Nicolas\output.wav')


# In[ ]:


Google_analytics = ("google analytics","analytics", "google")
Temperature = ("température","pièce")

GREETING_RESPONSES = ("salut","bonjour", "Enchanté", "Ravie de vous recontrer")
BOT_LOST =  ["Je n'ai pas bien compris, pouvez vous répéter ?", "Excusez moi, qu'avez vous dit ?"]



global CLOSE
CLOSE = ["revoir", "journée"]
global VOICE_CLOSE
VOICE_CLOSE = ["Au revoir!", "Bonne journée!"]
global prenom
prenom = ["Bonjour, quel est votre prénom ?"]

def check_for_answer(sentence):

    global a
   
    if not talk:
        print "talk" + talk
        a = ""
    else:
        for word in sentence:
            print word
            if word.lower() in CLOSE:
                a = random.choice(VOICE_CLOSE)
                return a
            if i == 1:
                if word.lower() == str("nicolas"):
                    a = "Salut Nicolas !"
                else:
                    a = (random.choice(GREETING_RESPONSES) + sentence[-1])
                return a
            elif word.lower() in Google_analytics:
                call_GA()
                a = "Il y a actuellement " + str(GA) + " Visiteurs sur les sites"
                return a
            elif word.lower() in Temperature:
                print word.lower()
                temperature_room()
                a = "Il fait actuellement " + str(data) + " degrés dans la pièce"
                return a

            else:
                a = random.choice(BOT_LOST)

    return a 
        
        
        
#check_for_answer(talk)


# In[ ]:

def convert_answer_to_wav():

    tts = gTTS(text=a , lang='fr', slow=False)
    tts.save("DIRECTORY/lm.mp3")
    os.chdir('DIRECTORY')
    try:
        os.remove('DIRECTORY/output6.wav')
    except OSError:
        pass
    #os.remove('C://Users/Nicolas/output6.wav')
    os.system('ffmpeg -i lm.mp3 output6.wav')


#convert_answer_to_wav()


# In[ ]:

def speak_answer ():
    CHUNK = 1024

    if len(sys.argv) < 2:
        print("Plays a wave file.\n\nUsage: %s filename.wav" % 'DIRECTORY\output6.wav')
        #sys.exit(-1)

    wf = wave.open('DIRECTORY\output6.wav', 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()
    
#speak_answer ()


# In[ ]:

def welcome ():
    CHUNK = 1024

    if len(sys.argv) < 2:
        print("Plays a wave file.\n\nUsage: %s filename.wav" % 'DIRECTORY\intro6.wav')
        #sys.exit(-1)

    wf = wave.open('C:\Users\Nicolas\intro6.wav', 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()
    
#welcome ()


# In[ ]:

def call_GA():


    import argparse

    from apiclient.discovery import build
    from oauth2client.service_account import ServiceAccountCredentials

    import httplib2
    from oauth2client import client
    from oauth2client import file
    from oauth2client import tools



    def get_service(api_name, api_version, scope, key_file_location,
                    service_account_email):
      """Get a service that communicates to a Google API.

      Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scope: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account p12 key file.
        service_account_email: The service account email address.

      Returns:
        A service that is connected to the specified API.
      """

      credentials = ServiceAccountCredentials.from_p12_keyfile(
        service_account_email, key_file_location, scopes=scope)

      http = credentials.authorize(httplib2.Http())

      # Build the service object.
      service = build(api_name, api_version, http=http)

      return service


    def get_first_profile_id(service):
      # Use the Analytics service object to get the first profile id.

      # Get a list of all Google Analytics accounts for this user
      accounts = service.management().accounts().list().execute()

      if accounts.get('items'):
        # Get the first Google Analytics account.
        account = accounts.get('items')[0].get('id')

        # Get a list of all the properties for the first account.
        properties = service.management().webproperties().list(
            accountId=account).execute()

        if properties.get('items'):
          # Get the first property id.
          property = properties.get('items')[0].get('id')

          # Get a list of all views (profiles) for the first property.
          profiles = service.management().profiles().list(
              accountId=account,
              webPropertyId=property).execute()

          if profiles.get('items'):
            # return the first view (profile) id.
            return profiles.get('items')[0].get('id')

      return None


    def get_results(service, profile_id):
      # Use the Analytics Service Object to query the Core Reporting API
      # for the number of sessions within the past seven days.
      return service.data().realtime().get(
          ids='ga:' + profile_id,
          metrics='rt:activeUsers',
          sort='-rt:activeUsers').execute()


    def print_results(results):
        
      global GA
      # Print data nicely for the user.
      if results:
        GA = results.get('rows')[0]
        GA = ''.join(GA)
        print GA


      else:
        print 'No results found'


    def main():
          global GA
          # Define the auth scopes to request.
          scope = ['https://www.googleapis.com/auth/analytics.readonly']

          # Use the developer console and replace the values with your
          # service account email and relative location of your key file.
          service_account_email = os.environ['ACCOUNT_EMAIL']
          key_file_location = os.environ['API_TOKEN_P12']

          # Authenticate and construct service.
          service = get_service('analytics', 'v3', scope, key_file_location,
            service_account_email)
          profile = get_first_profile_id(service)
          print_results(get_results(service, profile))

    main()


    return GA
#call_GA()


# In[ ]:

print ser.readline()



# In[ ]:

def temperature_room():
    time.sleep(3)
    global data
    global temp
    for a in range(1,30):
        try:    
            data = ser.readline()
            #print data
            temp = float(data)
            if temp > 15.00 and temp < 28.00:
                print temp
                break
        except:
            pass
temperature_room()


# In[ ]:

i = 0
while i < 30:
    i += 1
    try:
        data = int(ser.readline())
        #data = data.split(",")
        print data
        time.sleep(1)
    except:
        pass
        
    


# In[ ]:




# In[ ]:




# In[4]:

def motion():
    global data
    global mov
    while True:
        try:
            mov = int(ser.readline())
            if mov == 1:
                print "wahh"
                from twilio.rest import Client
 
                # Find these values at https://twilio.com/user/account
                account_sid = os.environ['TWILLIO_ACCOUNT_ID']
                auth_token = os.environ['TWILIO_TOKEN']
                client = Client(account_sid, auth_token)

                message = client.api.account.messages.create(to=os.environ['TEL_FROM'],
                                                             from_=os.environ['TEL_TO'],
                                                             body="ALARM !!!! ")
                break
            
        except:
            pass

motion()


# In[ ]:

print type(mot)
print mot


if __name__ == "__main__":
    welcome()
    for i in range(1,10):
        open_COM3()
        time.sleep(2)
        global last_response 
        last_response = []
        record_voice()
        transcribe_voice('DIRECTORY/output.wav')
        check_for_answer(talk)
        convert_answer_to_wav()
        speak_answer ()
        last_response.append(a)
        if last_response in VOICE_CLOSE:
            ser.close()
            break
            
        ser.close()
        time.sleep(1)



ser.close()





