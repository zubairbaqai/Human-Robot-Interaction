import flask
from flask import request, jsonify
import numpy
from io import BytesIO
import requests
import io
import subprocess
import paralleldots
from google.cloud import translate_v2 as translate
import os
import six




application= app = flask.Flask(__name__)
app.config["DEBUG"] = False




@app.route('/Mood', methods=['POST'])
def moody():

    data=request.args.to_dict()

    text=data['Review']
    language=data["Language"]


    if(language=="it"):
        translate_client = translate.Client()
        if isinstance(text, six.binary_type):
            text = text.decode('utf-8')

        result = translate_client.translate(
        text)
        text=result['translatedText']

    response_1=paralleldots.emotion(text)
    main_emotion= response_1['emotion']

    #return (str(main_emotion))

    maxscore=0
    ResultMood=""
    print(main_emotion)
    for emotions in main_emotion:
        Mood=emotions;
        score=main_emotion[Mood]
        if(score>maxscore):
            maxscore=score
            ResultMood=Mood
    print("the User is :  "+ResultMood)
    return jsonify(
        Mood=ResultMood

    )



app.run(host='0.0.0.0', port=5001, debug=False)