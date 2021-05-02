#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 00:00:35 2021

@author: aqib
"""
import tensorflow as tf
import numpy as np
import re
import time
import pandas as pd


#data = open('20200325_counsel_chat.csv', encoding = 'utf-8', errors = 'ignore').read().split('\n')
fypdata = pd.read_csv("20200325_counsel_chat.csv")

questions = fypdata["questionText"]
answers = fypdata["answerText"]

bigger = 0
for question in questions:
    if len(question) > bigger:
        bigger = len(question)

print(bigger)

def clean_text(text):
    text = text.lower()
    text = re.sub(r"i'm","i am", text)
    text = re.sub(r"i’m","i am", text)
    text = re.sub(r"i’ve","i have", text)
    text = re.sub(r"doesn't","does not", text)
    text = re.sub(r"haven't","have not", text)
    text = re.sub(r"he's","he is", text)
    text = re.sub(r"she's","she is", text)
    text = re.sub(r"it's","it is", text)
    text = re.sub(r"i'd","i do", text)
    text = re.sub(r"you're","you are", text)
    text = re.sub(r"what's","what is", text)
    text = re.sub(r"where's","where is", text)
    text = re.sub(r"there's","there is", text)
    text = re.sub(r"that's","that is", text)
    text = re.sub(r"don't","do not", text)
    text = re.sub(r"that's","that is", text)
    text = re.sub(r"\'ll"," will", text)
    text = re.sub(r"\'ve"," have", text)
    text = re.sub(r"\'re"," are", text)
    text = re.sub(r"\'d"," would", text)
    text = re.sub(r"won't","will not", text)
    text = re.sub(r"can't","cannot", text)
    text = re.sub(r"[-()\"#$&'/@*;:<>%{}+=~_|.?,]","", text)
    return text

clean_questions = []

for question in questions:
    clean_questions.append(clean_text(question))

clean_answers = []

for answer in answers:
    clean_answers.append(clean_text(answer))    



# count the number of occurance of word 
questionsword2count = {}
for question in clean_questions:
    for word in question.split():
        if word not in questionsword2count:
            questionsword2count[word] = 1
        else:
            questionsword2count[word] += 1
answersword2count = {}            
for answer in clean_answers:
    for word in answer.split():
        if word not in answersword2count:
            answersword2count[word] = 1
        else:
            answersword2count[word] += 1

# creatign two dictionaries that will map each word of answers and questions to unique integer


questionswords2int = {}
word_number = 0
for word, count  in questionsword2count.items():
        questionswords2int[word] = word_number
        word_number+=1
        
answerswords2int = {}
word_number = 0
for word, count  in answersword2count.items():
        answerswords2int[word] = word_number
        word_number+=1

# Adding the last tokens to these two dictionaries
tokens = ['<PAD>','<EOS>','<OUT>','<SOS>']
for token in tokens:
    questionswords2int[token] = len(questionswords2int) +1
for token in tokens:
    answerswords2int[token] = len(answerswords2int) +1
    
    
# creating inverse dictionary for answerswords2int 
answersints2word = {}
answersints2word = {w_i:w for w,w_i in answerswords2int.items()}
 
# adding end of string token to end of every answer

for i in range(len(clean_answers)):
    if '<EOS>' not in clean_answers[i]: # i aaded this myself so if answer already contains EOS so you program does not add it again specially if you are running your code again
        clean_answers[i] = clean_answers[i] + ' <EOS>'
    

# translating all the answers and questions to integers
'''
for i in range(len(clean_answers)):
    answer = clean_answers[i]
    for word, count in answerswords2int.items():
        if word in answer:
            answer = answer.replace(word, str(count))
    clean_answers[i] = answer        
'''            

questions_to_int = []
for question in clean_questions:
    ints = []
    for word in question.split():
        if word not in questionswords2int:
            ints.append(questionswords2int['<OUT>'])
        else:
            ints.append(questionswords2int[word])
    questions_to_int.append(ints)

answers_to_int = []
for answer in clean_answers:
    ints = []
    for word in answer.split():
        if word not in answerswords2int:
            ints.append(answerswords2int['<OUT>'])
        else:
            ints.append(answerswords2int[word])
    answers_to_int.append(ints)

# sorted questions and answers by their length to optimize the training time and reduce the loss function


sorted_clean_questions = []
sorted_clean_answers = []
for length in range(1, 542 + 1):
    for i in enumerate(questions_to_int):
        if len(i[1]) == length:
            sorted_clean_questions.append(questions_to_int[i[0]])
            sorted_clean_answers.append(answers_to_int[i[0]])


