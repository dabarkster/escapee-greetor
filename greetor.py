#new change
import pygame, time, os, random
from subprocess import Popen
import pygame.camera

#from __future__ import print_function
import RPi.GPIO as GPIO
import SimpleMFRC522
import time
#from google.cloud import texttospeech

import paho.mqtt.client as paho
broker="52.36.168.10"
port=1883

def on_publish(client1,userdata,result):             #create function for callback
    print("data published \n")
    pass

def on_connect(client1, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client1.subscribe("hottopic")

def on_message(client1, userdata, msg):
    msg.payload = msg.payload.decode("utf-8")
    print(msg.payload)
    if (msg.payload == 'me'):
        print("msg received")
        client1.disconnect()
    else:
        print("nothing to do")

#client1= paho.Client("control1")                           #create client object
#client1.on_publish = on_publish                          #assign function to callback
#client1.connect(broker,port,60)                                 #establish connection
#client1.on_connect = on_connect
#client1.on_message = on_message
#ret= client1.publish("hottopic",": Welcome to ZoeIke Tech")                   #publish


#client1.loop_start()
#while True:
#    time.sleep(0.1)

#quit()

display_width = 1024
display_height = 1280
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

pygame.init()
print("pypy")
movie_bubbles = '/home/pi/MFRC522-python/BlueBubbles.mp4'
Popen(['omxplayer',  '--win', '"0 0 960 540"', movie_bubbles])


img = pygame.image.load("test.jpg")
#screen = pygame.display.set_mode((0,0));
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
screen = pygame.display.set_mode((640, 480), pygame.NOFRAME);


#pygame.camera.init()
#cam = pygame.camera.Camera("/dev/video0", (320, 240))
#cam.start()
#while 1:
#    image = cam.get_image()
#    screen.blit(image, (0,0))
#    pygame.display.update()

done = False


area_text = pygame.Rect(0,0,400,400)
textBox = screen.subsurface(area_text)
textBox.fill(white)

#textBox = textBox.copy()
#screen.blit(textBox,(0,0))
#pygame.display.flip()

#area_photo = pygame.Rect(0,0,960,540)
#photo = screen.subsurface(area_photo)
#photo = photo.copy()
#photoarea = photo.get_rect()
#print photo.get_parent()

#client = texttospeech.TextToSpeechClient()
#voice_name='en-AU-Standard-C'
#voice_language='en-AU'
#duration = .1  # second
#freq = 4000  # 

reader = SimpleMFRC522.SimpleMFRC522()



def text_objects(text, font):
    textSurface = font.render(text, True, red)
    return textSurface, textSurface.get_rect()

def message_display(text):
    term = '/home/pi/MFRC522-python/saucer.ttf'
    #os.path.exists(term)
    largeText = pygame.font.Font(term, 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((area_text.width/2),(area_text.height/2))
    status = screen.blit(TextSurf,TextRect.center)
    pygame.display.update()
    time.sleep(2)

def darthFader():
    GPIO.setup(26, GPIO.OUT)# set GPIO 26 as output for led  
    led= GPIO.PWM(26,100)   # create object led for PWM on port 26 at 100 Hertz  
    led.start(0)            # start led on 0 percent duty cycle (off)  
    pause_time = 0.05       # you can change this to slow down/speed up  

    try:  
        while True:  
            for i in range(0,101,10):    # 101 because it stops when it finishes 100  
                led.ChangeDutyCycle(i)  
                time.sleep(pause_time)  
            for i in range(100,-1,-5):      # from 100 to zero in steps of -1  
                led.ChangeDutyCycle(i)  
                time.sleep(pause_time)  

    except KeyboardInterrupt:  
        led.stop()            # stop the led PWM output  
        GPIO.cleanup()        # clean up GPIO on CTRL+C exit

def run_quickstart():
    from google.cloud import texttospeech
    voice_name='en-AU-Standard-C'
    voice_language='en-AU'
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.types.SynthesisInput(text="Welcome to BioTech")

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code=voice_language,
        name=voice_name,
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)
    # The response's audio_content is binary.
    with open('welcome.mp3', 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "welcome.mp3"')
    
    os.system("mpg123 welcome.mp3")

    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text="Untangle web design and development with this ebook bundle from O'Reilly Media! Snare titles like React Native Cookbook, CSS: The Definitive Guide, High Performance Images, and more. Then go forth and weave something awesome.")

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code=voice_language,
        name=voice_name,
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)
    # The response's audio_content is binary.
    with open('output.mp3', 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')
    
    os.system("mpg123 output.mp3")
    # [END tts_quickstart]

def write_tts(text_to_say, out_file):

    synthesis_input = texttospeech.types.SynthesisInput(text = text_to_say)

    voice = texttospeech.types.VoiceSelectionParams(
        language_code=voice_language,
        name=voice_name,
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(synthesis_input, voice, audio_config)
 
    with open(out_file, 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file')

    print(text_to_say)
    fileplay = "mpg123 %s" %(out_file)
    os.system(fileplay)

def welcome():

    
    write_tts("You have been granted full access to all laboratories and centers.")


    #synthesis_input = texttospeech.types.SynthesisInput(text="Welcome to BioTech, please hold while I check your credentials")
    
    #voice = texttospeech.types.VoiceSelectionParams(
    #    language_code=voice_language,
    #    name=voice_name,
    #    ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)
    
    #audio_config = texttospeech.types.AudioConfig(
    #    audio_encoding=texttospeech.enums.AudioEncoding.MP3)
 
    #response = client.synthesize_speech(synthesis_input, voice, audio_config)
    
    #with open('welcome.mp3', 'wb') as out:
       # Write the response to the output file.
    #    out.write(response.audio_content)
    #    print('Audio content written to file "welcome.mp3"')
        
    #os.system("mpg123 welcome.mp3")
    

        
    #os.system("mpg123 authorized.mp3")
    # [END tts_quickstart]

#try:
#    while True:
#
#        os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))
#        os.system("mpg123 welcome.mp3")
#        write_tts("You have been granted full access to all laboratories and centers.", "access.mp3")
        #os.system("mpg123 visitor.mp3")
        #os.system("mpg123 authorized.mp3")
    
#finally:
def shuffleKid():
    picturedelay = .05
    for x in range(5):
        drawkid('zoe.jpg')
        time.sleep(picturedelay)
        drawkid('cyd.jpg')
        time.sleep(picturedelay)
        drawkid('laura.jpg')
        time.sleep(picturedelay)
        drawkid('bekah.jpg')
        time.sleep(picturedelay)

def drawkid(kid):
    img = pygame.image.load(kid).convert()
    #img = pygame.transform.scale(img,(960,540))
    screen.blit(img,(0,0))
    pygame.display.flip()

def say_phrases():
    write_tts("We are glad you are able to help find an antidote to Dr Keans anti-boy-otic Boy experiment!", "kissy.mp3")
    write_tts("You have been granted full access to all laboratories and centers.", "access.mp3")
    write_tts("Welcome Zoe!", "welcome_zoe.mp3")
    write_tts("Welcome Cydni!", "welcome_cyd.mp3")
    write_tts("Welcome Jaycee!", "welcome_jay.mp3")
    write_tts("Welcome Laura!", "welcome_laura.mp3")
    write_tts("Welcome Rylee!", "welcome_ry.mp3")
    write_tts("Welcome Rebekah!", "welcome_rebekah.mp3")
    write_tts("Welcome Alex!", "welcome_alex.mp3")
    write_tts("Welcome Kelsey!", "welcome_kelsey.mp3")
    #new change

def pickKid():
    kid_list = ["zoe", "cydni", "laura",  "rabekah", "rylee"]
    for x in range(len(kid_list)):
        rand = random.randint(0,len(kid_list)-1)
        print(rand)
        print(kid_list[rand])
        drawkid("%s.jpg" %kid_list[rand])
        kid_list.pop(rand)
        time.sleep(.5)
        


try:
    #say_phrases()
    #darthFader()
    #testMQTT()
    #shuffleKid()
    message_display("Pass...")

    while True:
    	pass
    done = True;
    while not done:
       #for event in pygame.event.get():
       #  if event.type == pygame.QUIT:
       #     done = True
        #print("Hold a tag near the reader")
        id, text = reader.read()
        print(id)
        text = text.replace(" ","")
        print(len(text))
        
        if text == "Zoe":
            print("ZOE")
            drawkid("zoeinfo.jpg")
            write_tts("We are glad you are able to help find an antidote to Dr Keans Kissy Boy experiment!", "access.mp3")
            #write_tts("You have been granted full access to all laboratories and centers.", "access.mp3")
        
        elif text == "Cyd":
            print("CYD")
            drawkid("test2.jpg")

        elif text == "Jaycee":
            pass
        elif text == "Laura":
            pass
        elif text == "Rylee":
            pass
        elif text == "Alex":
            pass
        elif text == "Rabekah":
            pass
        else:
            print(text)

        time.sleep(1)


        #
        #screen.blit(photo,(0,0))

        #time.sleep(3)
        #img = pygame.image.load("cyd.jpg").convert()
        #img = pygame.transform.scale(img,(300,400))
        #screen.blit(img,(0,0))
        #rect = img.get_rect()
        #rect = rect.move((100, 100))
        #screen.blit(img, rect)
        #pygame.display.flip()
        #pygame.display.flip()
        #time.sleep(3)

finally:
    print("cleaning up")
    GPIO.cleanup()

