import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from threading import Thread
import json, time, os, ConfigParser, sys, logging, re

#Globals
is_rpi = False
api = None
username = None
keywords = "open sesame"
welcome_msg = "Welcome to the cavern, my lord. This is your servent Humbledoor."
tease_on = re.compile("^open", re.IGNORECASE)
teaser_text = "Is it you, Kasim?"
ffwd_msg = "Hey,You have reached to Humbledoor. I will forward your message to my master. Thanks."
relay_pin = 12
relay_delay = 20

class OpenSesame (StreamListener):
  is_door_open = False
  ''' 
  def on_data(self, data):
    logging.debug("ON Data")
    logging.debug(data)
    return True
  '''

  def on_status(self, stts):
    return True

  def on_direct_message(self, dm):
    sender_id = dm.direct_message["sender_id"]
    message_orig = dm.direct_message["text"]
    sender_name = dm.direct_message["sender_screen_name"]
    
    logging.debug('Received: "' + message_orig + '"  from "' + sender_name + '" to "' + username +'"')

    if sender_name != username:
      message = message_orig.strip().lower()
      if message != keywords and tease_on.match(message_orig):
        api.send_direct_message(user_id = sender_id, text = teaser_text )
      elif message == keywords:
        api.send_direct_message(user_id = sender_id, text = welcome_msg )
        if not OpenSesame.is_door_open:
          thread = Thread(target = self.open_the_door)
          thread.start()
      else:
        api.send_direct_message(user_id = sender_id, text = ffwd_msg )

    return True

  def on_error(self, status):
    logging.debug("Error")
    logging.debug(status)

  def open_the_door(self):
    if OpenSesame.is_door_open:
      return
    OpenSesame.is_door_open = True
    if is_rpi:
      GPIO.output(relay_pin, GPIO.HIGH)
    logging.debug("The door is open.")
    time.sleep(relay_delay)
    if is_rpi:
      GPIO.output(relay_pin, GPIO.LOW)
    logging.debug("The door is closed.")
    OpenSesame.is_door_open = False


def get_lvl(lvl):
  return {
          'critical': logging.CRITICAL,
          'error': logging.ERROR,
          'warning': logging.WARNING,
          'info': logging.INFO,
          'debug': logging.DEBUG
          }[lvl]

if __name__ == "__main__":

  # Initial config
  where_am_i = os.path.abspath(os.path.dirname(__file__))
  conf_file = os.path.join(where_am_i, 'conf.ini')

  conf = ConfigParser.ConfigParser()
  conf.read(conf_file)

  consumer_key = conf.get('twitter_conf', 'consumer_key')
  consumer_secret = conf.get('twitter_conf', 'consumer_secret')
  access_token = conf.get('twitter_conf', 'access_token')
  access_token_secret = conf.get('twitter_conf', 'access_token_secret')

  relay_pin = int(conf.get('pi_conf', 'relay_pin'))
  relay_delay = int(conf.get('pi_conf', 'open_duration_sec'))

  keywords = conf.get('messaging_conf', 'keywords').strip().lower()
  welcome_msg = conf.get('messaging_conf', 'welcome_msg')
  tease_on_regex = conf.get('messaging_conf', 'tease_on')
  tease_on = re.compile(tease_on_regex, re.IGNORECASE)
  teaser_text = conf.get('messaging_conf', 'teaser_text')
  ffwd_msg = conf.get('messaging_conf', 'ffwd_msg')

  log_dir = conf.get('logging_conf', 'log_dir')
  log_level = conf.get('logging_conf', 'log_level')

  # Initial setup
  if log_dir == 'logs':
      log_dir = os.path.join(where_am_i, 'logs')
  
  log_file = os.path.join(log_dir, 'humbledoor.log')
  log_lvl = get_lvl(log_level)

  if log_lvl == logging.DEBUG:
    tweepy.debug(True)

  logging.basicConfig(filename = log_file, level = log_lvl, \
          format='\n%(asctime)s\n%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

  logging.debug(
          "consumer_key: " + consumer_key + "\n" + 
          "consumer_secret: " + consumer_secret + "\n" + 
          "access_token: " + access_token + "\n" + \
          "access_token_secret: " + access_token_secret + "\n" + 
          "relay_pin: " + str(relay_pin) + "\n" + 
          "open_duration: " + str(relay_delay) + "\n"
          "keywords: " + keywords + " \n" +
          "welcome_msg: " + welcome_msg + " \n" +
          "tease_on: " + tease_on_regex + " \n" +
          "teaser_text: " + teaser_text + " \n" +
          "ffwd_msg: " + ffwd_msg + " \n" +
          "log_dir: " + log_dir + "\n" + 
          "log_level: " + log_level
          )
 

  if os.uname()[4].startswith("arm"):
    logging.info("Running on a Raspberry Pi.")
    is_rpi = True
    import RPi.GPIO as GPIO
  else:
    logging.info("Not a Raspberry Pi. Any of the GPIO commands will not be executed.")

  if is_rpi:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(relay_pin, GPIO.OUT, initial = GPIO.LOW)

  l = OpenSesame()
  auth = OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  username = auth.get_username()
  api = tweepy.API(auth)

  stream = Stream(auth, l)
  stream.userstream()

