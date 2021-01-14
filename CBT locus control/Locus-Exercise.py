#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 09:49:56 2020

@author: user
"""
answers=[]

print('Take some time to self-reflect and answer the following questions. They have been designed to help you further explore how you are currently being impacted and influenced in life:')
print('')
print('')

def listsum(numList):
   if len(numList) == 1:
        return numList[0]
   else:
        return numList[0] + listsum(numList[1:])

def load_base(locus_control1,locus_control2):
    # answers=[]
    for (k,v), (k2,v2) in zip(locus_control1.items(), locus_control2.items()):
        print(k,v)
        print('')
        print(v2)
        print('')
        answer=str(input('Please answer the question and enter letter a or b or c '))
        print('')
        while answer!='a'and answer!='b' and answer!='c':
            print('Please input "a" or "b" or "c" ')
            print('')
            answer=str(input('Please answer the question and enter letter a or b or c '))
            print('')
        answers.append(answer)
    return answers

scores_1=['a','a','c','c','c','a','c','c','c','c']
scores_2=['b','b','b','b','b','b','b','b','b','b']
scores_3=['c','c','a','a','a','c','a','a','a','a']

questions={
'Q1': 'Do you find yourself multitasking and rushing around when you are with other people?',
'Q2': 'Do you find yourself judging and criticising yourself about how well you are performing or constantly judging other people?',
'Q3': 'Are you compassionate towards yourself and other people (if you make a mistake, are you understanding of yourself or do you criticise yourself for getting it wrong?',
'Q4': 'Are you curious about yourself and/or the world around you (do you find yourself asking questions about your thoughts/emotions/body or about topics that interest you?',
'Q5': 'Do you tend to hold grudges when someone does something you disapprove of or are you quite a forgiving person?',
'Q6': 'Do you live your life on autopilot (automatically and mechanically), or are you deliberate and conscious in your approach?',
'Q7': 'Are you a grateful person? Do you take time to reflect on what is going well in life and appreciate what you do have?',
'Q8': 'Are you focused and attentive when you are conversing with other people?',
'Q9': 'Do you set aside some quiet time each day to allow yourself to stop, reflect and perhaps even take part in some kind of activity that you enjoy (for example, yoga, cooking, walking, etc.)?',
'Q10':'Do you accept your emotions when they come up or do you usually try to avoid them in some way?', 
}

replies={
'Q1': 'a - Often Rushing  b - Sometimes Rushing  c - Rarely Rushing',
'Q2': 'a - Often Judging  b - Sometimes Judging  c - Rarely Judging',
'Q3': 'a - Often Compassionate b - Sometimes Compassionate  c - Rarely Compassionate',
'Q4': 'a - Often Curious  b - Sometimes Curious  c -  Rarely Curious',
'Q5': 'a - Forgiving When Necessary  b - Sometimes Forgiving c - Rarely Forgiving',
'Q6': 'a - Often Automatic b - Sometimes Automatic c - Often Conscious & Aware',
'Q7': 'a - Often Grateful b - Sometimes Grateful c - Rarely Grateful',
'Q8': 'a - Focused b - Sometimes Focused c - Often Distracted',
'Q9': 'a - Have Daily Quiet Time b - Sometimes Have Quiet Time c - Never Have Quiet Time (1)',
'Q10':'a - Always Accept Emotions b - Sometimes Except Emotions c - Rarely Accept Emotions (1)', 
}

load_base(questions,replies)
# print(answers)
total_score = [] 
for i in range(len(scores_1)): 
    if answers[i] == scores_1[i]:
        total_score.append(1) 
    elif answers[i] == scores_2[i]:
        total_score.append(2)
    elif answers[i] == scores_3[i]:
        total_score.append(3)
# print (total_score) 
# print('Your total score is:')
# print(listsum(total_score))
x=listsum(total_score)
if 10<=x<=15:
    print('This is an indication that learning how to become more mindful, focused and aware will help you to be less influenced by your emotions and any external stressors.')
    print('This could have a hugely positive effect on your life. Taking time to practice and develop these skills will help to bring about a greater degree of emotional balance')
    print('and fulfilment. This, in turn, will enhance the quality of your relationships as you become more aware and attentive to the needs of others.')
elif 16<=x<=24:
    print('This is an indication that you are already fairly mindful, focused and aware. However, as you take time to further develop and deepen these skills, you will become even less influenced by your emotions and any external stressors. This, in turn, will bring about an even greater degree of emotional balance and fulfilment in life. Doing so will also positively impact the quality of your relationships as you become even more aware and attentive to the needs of others.')
elif 25<=x<=30:
    print('This is an indication that you are already significantly mindful, focused and aware and not too easily distracted by your emotions or any external stressors. Taking time to fine tune these skills will help to further enhance the quality of your life greatly. Not only will this bring about an even greater degree of emotional balance in your own life, but this will also have a positive knock-on effect on your relationships as you become even more appreciative and aware of those around you.')
    