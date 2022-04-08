from flask import Flask, render_template,url_for, request, redirect, jsonify
import os
import sys
import openai
openai.api_key = ""
from flask_cors import CORS, cross_origin
from difflib import SequenceMatcher

app = Flask(__name__)
port = int(os.environ.get('PORT', 5000))

CORS(app, support_credentials=True)





def retrieve_input(answer2):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=answer2,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["Ashley:"]
            )
    return(response["choices"][0]["text"])


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        with open("client.txt", 'r')as f1:
            content1 = f1.readlines()
        with open("therapist.txt", 'r')as f2:
            content2 = f2.readlines()
        body = request.form.get('text')
        index = -1
        try:
            for i in range(len(content1)):
                if (SequenceMatcher(None, content1[i], body).ratio())>0.9:
                    index = i
                    break
        except:
            pass
        if index == -1:
            body = "This is a conversation between Ashley and a therapist named John.\nJohn: Hi Ashley, great to see you again.\Ashley:"+body+"\nJohn:"
        else:
            body = "This is a conversation between Ashley and a therapist named John.\nJohn: Hi Ashley, great to see you again.\Ashley:"+content1[index].replace("CLIENT:","")+"\nJohn:"+content2[index].replace("THERAPIST:","")+"\nAshley:"+body+"\nJohn:"
        answer = retrieve_input(body)
        answer = answer.rstrip().lstrip()
        answer = answer.replace("Ashley",request.form.get('name'))
        data_final={}
        # data_final['answer1']=clean_response_response
        data_final['answer']=answer
        resp = jsonify(data_final)
        return(resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
