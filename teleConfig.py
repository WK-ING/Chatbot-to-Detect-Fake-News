from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

import joblib
import pandas as pd

class State:
    def __init__(self):
        self.state = "general"
        self.content = ''

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello sir, Welcome to IEMS5780 Assignment 2 demo bot. Please write\
        /help to see the commands available.")

def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
    /model_1 - To pridict the news using logistic regression model with count vectorizer.
    /model_2 - To pridict the news using logistic regression model with tfidf vectorizer.
    Otherwise - cannot interpret.
    """)

def model_1(update: Update, context: CallbackContext):
    update.message.reply_text(
        "What is the title of your message?")
    s.state = "title"
    s.model = 1

def model_2(update: Update, context: CallbackContext):
    update.message.reply_text(
        "What is the title of your message?")
    s.state = "title"
    s.model = 2

def general(update: Update, context: CallbackContext):
    if s.state == "title":
        s.title = update.message.text
        s.state = "content"
        update.message.reply_text(
            "What is the content of your message? \n (Note: the length should not larger than 4096 characters)")

    elif s.state == "content":
        
        s.content = update.message.text

        s.state = "general"

        X = pd.DataFrame([[s.title, s.content]], columns=['title', 'text'])
        # use the  loaded moedl to get the predicted values based on the s.title and s.content
        if s.model == 1:
            proba = model_1.predict_proba(X)[0,1]
        elif s.model == 2:
            proba = model_2.predict_proba(X)[0,1]
        
        if proba < 0.4:
            reply = "Your message is FAKE (p = {:.1f})".format(proba)
        elif proba > 0.6:
            reply = "Your message is REAL (p = {:.1f})".format(proba)
        else:
            reply = "cannot determine (p = {:.1f})".format(proba)

        # output the result in the reply variable
        update.message.reply_text(reply)
    
    else:
        update.message.reply_text(
            "Sorry I can't recognize you , you said '%s'" % update.message.text)


    return 


if __name__ == "__main__":
    
    # Provide your bot's token here!!
    # updater = Updater(" your_token ", use_context=True)

    # If you need to load the model, load it here
    model_1 = joblib.load("count_LR_model.pkl")
    model_2 = joblib.load("tfidf_LR_model.pkl")

    s = State()

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('model_1', model_1))
    updater.dispatcher.add_handler(CommandHandler('model_2', model_2))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, general))
    updater.start_polling()

