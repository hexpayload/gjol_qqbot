from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.conversation import Statement
import os
from chatterbot.trainers import ChatterBotCorpusTrainer
import time
app = Flask(__name__)

bot = ChatBot(
    '机器人',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
       {
         'import_path': 'chatterbot.logic.BestMatch',
         'default_response': '对不起，这个问题我还不知道怎么回答你',
         'maximum_similarity_threshold': 0.7
       }
       
],
    input_adapter='chatterbot.input.TerminalAdapter',
 output_adapter='chatterbot.output.TerminalAdapter',
 preprocessors=['chatterbot.preprocessors.clean_whitespace'],
)
trainer = ChatterBotCorpusTrainer(bot)
#trainer.train("chatterbot.corpus.english")


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    #return str(bot.get_response(userText))
    input_statement = Statement(text=userText)
    return str(bot.generate_response(input_statement))
@app.route("/lea")
def get_learn_response():
    ans = request.args.get('ans')
    que = request.args.get('que')
    queue=Statement(text=que,search_text=que,conversation="training",persona="",SyntaxWarning="古剑",in_response_to=None,search_in_response_to="",created_at=time.strftime('%Y-%m-%d %H:%M:%S'))
    bot.learn_response(queue)
    correct_response = Statement(text=ans,in_response_to=que,search_text=ans,search_in_response_to=que)#__init__(self, text, in_response_to=None, **kwargs)
    bot.learn_response(correct_response, queue)
    
    return ("真是学到了呢")



if __name__ == "__main__":
    app.run(host="127.0.0.1",port=8898)
