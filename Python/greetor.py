#!/usr/bin/python3

import os
#import alsaaudio
import pygame
import random
import SimpleMFRC522
import time
import paho.mqtt.client as paho
from subprocess import Popen
#import pygame.camera
#from __future__ import print_function
import RPi.GPIO as GPIO

reader = SimpleMFRC522.SimpleMFRC522()

ID_584186413815  = "Cydni"
ID_584193154610  = "Jaycee"
ID_584187026004  = "Alex"
ID_584190114375  = "Laura"
ID_584186694458  = "Rylee"
ID_584195675615  = "Kelsey"
ID_584196296274  = "Malia"
ID_584195129101  = "Rabekah"
ID_584186168122  = "Christine"
ID_584188700149  = "Kara"
ID_1065873189125 = "Zoe"

screen_width = 1700
screen_height = 1080
photo_size = 400
photo_ratio = 536/820
photo_x = 200
photo_y = 200

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

broker="192.168.56.220"
port=1883

photo_path = '/home/pi/Pictures/'
font_path  = "/home/pi/escapee-greetor/Fonts/"
sound_path = "/home/pi/escapee-greetor/Sounds/"
music_path = "/home/pi/escapee-greetor/Music/"

pygame.init()
pygame.font.init()
print("pypy")


#os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
#screen = pygame.display.set_mode((0,0));
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME);

done = False

area_photo = pygame.Rect(200,200,600,811)
photo_box = screen.subsurface(area_photo)
area_text = pygame.Rect(area_photo.width + 50, photo_y + 50, photo_x + 640, photo_y + 400)
#print(screen)
#print(area_text)
textBox = screen.subsurface(area_text)



#photo = photo.copy()
#photoarea = photo.get_rect()

def text_objects(text, font):
    textSurface = font.render(text, True, red)
    return textSurface, textSurface.get_rect()

def message_display(bio):
    text1 = bio[0]
    text2 = bio[1]


    #textBox.fill(black)
    #textBox.set_alpha(50)
    #pygame.display.update()

    font = pygame.font.SysFont("Grobold", 100)
    text_rect = (0,0)

    #pygame.display.flip()
    #term = font_path + 'saucer.ttf'
    #os.path.exists(term)
    #largeText = pygame.font.Font(term, 115)
    #TextSurf, TextRect = text_objects(text, largeText)
    #TextRect.center = ((area_text.width/2),(area_text.height/2))
    font = pygame.font.SysFont("Grobold", 100)
    text_surf = font.render(text1, True, (240,240,240))
    textBox.blit(text_surf, text_rect)

    font = pygame.font.SysFont("Grobold", 50)
    text_rect = (0,75)
    text_surf = font.render(text2, True, (240,240,240))
    textBox.blit(text_surf, text_rect)

    textBox.set_alpha(50)
    #pygame.display.update()
 

def drawkid(kid):
    kid_img = photo_path + '/' + kid
    img = pygame.image.load(kid_img).convert()
    img = pygame.transform.scale(img,(photo_size,int(photo_size/photo_ratio)))

    #photo_box.fill(black)
    #print(img)
    photo_box.blit(img,(0,0))
    #pygame.display.flip()

#pygame.camera.init()
#cam = pygame.camera.Camera("/dev/video0", (320, 240))
#cam.start()
#while 1:
#    image = cam.get_image()
#    screen.blit(image, (0,0))
#    pygame.display.update()

#textBox = textBox.copy()
#screen.blit(textBox,(0,0))
#pygame.display.flip()

#print photo.get_parent()

#client = texttospeech.TextToSpeechClient()
#voice_name='en-AU-Standard-C'
#voice_language='en-AU'
#duration = .1  # second
#freq = 4000  # 



def showvideo():
    movie_bubbles = '/home/pi/MFRC522-python/BlueBubbles.mp4'
    Popen(['omxplayer',  '--win', '"0 0 960 540"', movie_bubbles])

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

def MQTT():
    #client1= paho.Client("control1")                           #create client object
    #client1.on_publish = on_publish                          #assign function to callback
    #client1.connect(broker,port,60)                                 #establish connection
    #client1.on_connect = on_connect
    #client1.on_message = on_message
    #ret= client1.publish("hottopic",": Welcome to ZoeIke Tech")                   #publish


    #client1.loop_start()
    #while True:
    #    time.sleep(0.1)
    pass



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
    picturedelay = .01
    for x in range(5):
        drawkid('zoe.jpg')
        time.sleep(picturedelay)
        drawkid('cydni.jpg')
        time.sleep(picturedelay)
        drawkid('laura.jpg')
        time.sleep(picturedelay)
        drawkid('rabekah.jpg')
        time.sleep(picturedelay)

def drawbackground():
    back_img = photo_path + '/logo_background.jpg'
    img = pygame.image.load(back_img).convert()
    screen.blit(img,(0,0))
    print("back")
    #pygame.display.flip()

def pickKid():
    kid_list = ["zoe", "cydni", "laura",  "rabekah", "rylee"]
    for x in range(len(kid_list)):
        rand = random.randint(0,len(kid_list)-1)
        print(rand)
        print(kid_list[rand])
        drawkid("%s/%s.jpg" %photo_path %kid_list[rand])
        kid_list.pop(rand)
        time.sleep(.5)

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

def speak_to_me(file):
    #name = sound_path + "bio" + kid + ".mp3"
    name = sound_path + "/" + file + ".mp3"
    pygame.mixer.music.load(name)
    pygame.mixer.music.play()



try:
    textBox.fill(black)
    drawbackground()
    pygame.display.flip()
    #say_phrases()
    #darthFader()
    #testMQTT()
    #shuffleKid()
    #message_display("Pass...")


    while True:
       #for event in pygame.event.get():
       #  if event.type == pygame.QUIT:
       #     done = True
        print("Hold a tag near the reader")
        id, text = reader.read()
        print(id)
        print(text)
        id = "ID_" + str(id)
        #text = text.replace(" ","")
        #print(len(text))
        print(id)
        speak_to_me("beep")

        if id == "ID_1065873189125":
            kid = "zoe"
            bio = ("Dr Zoe Hirata", "Neuroscientist")
        
        elif id == "ID_584186413815":
            kid = "cydni"
            bio = ("Dr Cydni Kodani", "Microbiologist")

        elif id == "ID_584193154610":
            kid = "jaycee"
            bio = ("Dr Jaycee Hasegawa", "Environmental Engineer")

        elif id == "ID_584187026004":
            kid = "alex"
            bio = ("Dr Alex Soriano", "Physicist")

        elif id == "ID_584190114375":
            kid = "laura"
            bio = ("Dr Laura Ishii", "Nuclear Physicist")

        elif id == "ID_584186694458":
            kid = "rylee"
            bio = ("Dr Rylee Tanita", "Biochemist")

        elif id == "ID_584195675615":
            kid = "kelsey"
            bio = ("Dr Kelsey Yoshikawa", "Biomedical Engineer")

        elif id == "ID_584196296274":
            kid = "malia"           
            bio = ("Dr Malia Wagatsuma", "Nuclear Physicist")
        
        elif id == "ID_584195129101":
            kid = "rabekah"
            bio = ("Dr Rabekah Okimoto", "Biophysicist")

        elif id == "ID_584186168122":
            kid = "christine"
            bio = ("Dr Christine Hill", "Biologist")

        elif id == "ID_584188700149":
            kid = "kara"
            bio = ("Dr Kara Uemoto", "Robotics Engineer")

        else:
            kid = "none"

        if kid != "none":
            print(kid)
            textBox.fill(black)
            drawbackground()
            message_display(bio)
            kid_img = photo_path + "/" + kid + ".jpg"
            drawkid("%s.jpg" % (kid))
            pygame.display.flip()
            #speak_to_me(text)
        else:
            drawbackground()


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
        time.sleep(2)

finally:
    print("cleaning up")
    GPIO.cleanup()

