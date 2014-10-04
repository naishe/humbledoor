import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import RPi.GPIO as GPIO
import time
from threading import Thread
import os

tweepy.debug(True)


#Globals
api = None
username = None

class OpenSesame (StreamListener):
  is_door_open = False
  """
  def on_data(self, data):
    print "ON Data"
    print data
    return True
  """

  def on_status(self, stts):
    return True

  def on_direct_message(self, dm):
    sender_id = dm.direct_message["sender_id"]
    message = dm.direct_message["text"]
    sender_name = dm.direct_message["sender_screen_name"]
    
    print message + "\n" + sender_name + " != " + username

    if sender_name != username:
      message = message.strip().lower()
      if message != "open sesame" and message.startswith('open'):
        api.send_direct_message(user_id = sender_id, text = "Is it you, Kasim?" )
      elif message == "open sesame":
        api.send_direct_message(user_id = sender_id, text = "Welcome to the cavern, my lord. This is your servent HumbleDoor." )
        if not OpenSesame.is_door_open:
          thread = Thread(target = self.open_the_door)
          thread.start()
      else:
        api.send_direct_message(user_id = sender_id, text = "Hey, you have reached to Nishant's door. I will forward your message to him. Thanks." )

    return True

  def on_error(self, status):
    print "Error"
    print status

  def open_the_door(self):
    if OpenSesame.is_door_open:
      return
    OpenSesame.is_door_open = True
    GPIO.output(PIN_RELAY1, GPIO.HIGH)
    print "The door is open."
    time.sleep(20)
    GPIO.output(PIN_RELAY1, GPIO.LOW)
    print "The door is closed."
    OpenSesame.is_door_open = False



if __name__ == "__main__":

  #initial config
  
  # Initial setup
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(PIN_RELAY1, GPIO.OUT, initial = GPIO.LOW)

  l = OpenSesame()
  auth = OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  username = auth.get_username()
  api = tweepy.API(auth)

  stream = Stream(auth, l)
  #stream.filter(track=['basketball'])
  stream.userstream()

