import os, sys
import pickle

pdir = os.getenv('MODIM_HOME')
sys.path.append(pdir + '/src/GUI')
ModimDir=pdir+'/src/GUI'

####The path of Our playground  and Modim server/client is different , so if we need to access pickle of Modim from playground, we go to that dir

from ws_client import *
import ws_client

# Definition of interaction functions



def HeadTouch():
    import pickle

    im.init()
    im.display.loadUrl('layout.html')

    time.sleep(2)

    # Setting HTML element of the web page
    im.executeModality('TEXT_title','User Movie FeedBack')
    im.executeModality('TEXT_default','Touch my head if you want to Give a Review')
    im.executeModality('IMAGE','img/Pepper.jpeg')

    # Using TTS service of the robot to speak
    #im.executeModality('TTS','Hello There, i would like your feedback on the Movie, May i know your Name')
    im.robot.say("Touch my head to start the game")

    im.robot.startSensorMonitor()

    headTouched = False
    while not headTouched:
      p = im.robot.sensorvalue()
      headTouched = p[3]>0   # head sensor

    with open('headTouched.pickle', 'wb') as f:
        pickle.dump(headTouched, f)




def Username():
    import pickle
    UserNames=["Zubair","Domiziano","Salvatore"]
    im.executeModality('TEXT_title','User Movie FeedBack')
    im.executeModality('TEXT_default','Please Tell me Your name ?')
    im.executeModality('IMAGE','img/Pepper.jpeg')



    # Since we are using Fake ASR, as we dont have the speech service available. so pepper_cmd.py stores whatever we write inside write script , and there is no implementation of vocabulary



    im.executeModality('ASR',UserNames)

    # wait for answer

    
    Result=False
    while(not Result):
        a = im.ask(actionname=None, timeout=60)
        print(a)
        if a=='timeout':
            Result=False
        else:
            Result=True

        with open('UserName.pickle', 'wb') as f:
            print(a)
            pickle.dump(a, f)



def ReviewMovie():



    import pickle
    import requests
    import json
    with open('UserName.pickle', 'rb') as f:
        UserName = pickle.load(f)


    im.executeModality('TEXT_title','Hello '+UserName)
    im.executeModality('TEXT_default','Please Tell us about the Movie you Watched')
    im.executeModality('IMAGE','img/'+UserName+'.jpg')

    vocabulary=[]
    answer = im.robot.asr(vocabulary,60)
    print(answer)

    data = {'Review':answer,'Language':"english"} 
    r = requests.post(url = "http://0.0.0.0:5001/Mood", params = data) 
    json_data = json.loads(r.text)
    moodDetection= json_data["Mood"]

    if(moodDetection == "Bored"):
        im.executeModality('TEXT_title',UserName+" is "+moodDetection)
        im.executeModality('TEXT_default','I am Sorry you feel Bored, I will forward your Review to the Department')
        im.executeModality('IMAGE','img/'+"Bored.png")

    if(moodDetection == "Sad"):
        im.executeModality('TEXT_title',UserName+" is "+moodDetection)
        im.executeModality('TEXT_default','I am Sorry you feel Sad, I will forward your Review to the Department .<br> Would like to see a Dance ?')
        im.executeModality('IMAGE','img/'+"sad.jpg")
        im.executeModality('BUTTONS',[['yes','Yes'],['no','No']])
        im.executeModality('ASR',['yes','no'])

        a = im.ask(actionname=None, timeout=15)

        if a=='yes':
            im.executeModality('TEXT_default','!!! Dancing !!!')
            im.robot.dance()
        else:
            im.executeModality('TEXT_default','OK. No dancing')

        time.sleep(2)
        im.executeModality('TEXT_default','Bye bye')


    if(moodDetection == "Happy"):
        im.executeModality('TEXT_title',UserName+" is "+moodDetection)
        im.executeModality('TEXT_default','I am Glad you are happy and Enjoyed the Movie, I will forward your Review to the Department')
        im.executeModality('IMAGE','img/'+"Happy.jpeg")

    if(moodDetection == "Excited"):
        im.executeModality('TEXT_title',UserName+" is "+moodDetection)
        im.executeModality('TEXT_default','I See you are very excited, keep up the spirit. ')
        im.executeModality('IMAGE','img/'+"Excited.png")

    if(moodDetection == "Angry"):
        im.executeModality('TEXT_title',UserName+" is "+moodDetection)
        im.executeModality('TEXT_default','You seem Really Angry with Movie , Please do write a Complaint to IMDB reviews')
        im.executeModality('IMAGE','img/'+"Angry.jpeg")






def e34():
    im.executeModality('TEXT_default','Do you want me to dance?')

    im.executeModality('ASR',['yes','no'])

    # wait for answer
    a = im.ask(actionname=None, timeout=15)

    if a=='yes':
        im.executeModality('TEXT_default','!!! Dancing !!!')
        im.robot.dance()
    else:
        im.executeModality('TEXT_default','OK. No dancing')

    time.sleep(2)
    im.executeModality('TEXT_default','Bye bye')


# main

if __name__ == "__main__":

    # connect to local MODIM server
    mws = ModimWSClient()
    mws.setDemoPathAuto(__file__)

    
    try:
        import requests 
    except:
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        import requests




    




    # run interaction functions

    result=mws.run_interaction(HeadTouch) # blocking

    with open(ModimDir+'/headTouched.pickle', 'rb') as f:
        headTouched = pickle.load(f)

    if(headTouched):
        mws.run_interaction(Username) 


    mws.run_interaction(ReviewMovie)

    #mws.run_interaction(e34) 



