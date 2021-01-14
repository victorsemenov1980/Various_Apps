#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 09:49:56 2020

@author: user
"""
answers=[]

print('This is a questionnaire that will help you to determine where your locus of control lies. ')
print('')
print('Each question consists of a pair of alternatives (a;b). Please select the statement from each pair which you more strongly believe to be true.') 
print('')
print('Ensure that you chose the one you actually believe to be more true, as supposed to the one that you think you should choose or the one you would like to be true. Remember, this questionnaire is a measure of personal belief') 
print('so there are no right or wrong answers here. Consider your answers carefully but do not spend too much time on each one. In some questions, you may find that you believe both statements or neither one to be true.')
print('In this case, just select the one that you more strongly believe to be true. Lastly, try to respond to each question independently when making your choice; do not allow yourself to be influenced by your previous choices.')
print('')
print('Here we start the questions:')
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
        print(k2,v2)
        answer=str(input('Please select the one that you more strongly believe to be true and enter letter a or b '))
        while answer!='a'and answer!='b':
            print('Please input "a" or "b" ')
            answer=str(input('Please select the one that you more strongly believe to be true and enter letter a or b '))
        answers.append(answer)
    return answers

scores=[0,'a','b','b','b','a','a',0,'a','b','b','b','b',0,'b','a','a','a',0,'a','a','b','a',0,'a','b',0,'b','a']

questions_a={
'1a.': 'Children end up getting into trouble because their parents punish them too much.',
'2a.':' Many of the unhappy things in individual''s lives are partly due to bad luck.',
'3a.':' One of the primary reasons why we have wars is because individuals don''t take sufficient interest in politics.',
'4a.': 'In the long run, individuals get the respect they deserve in this world',
'5a.': 'The idea that teachers are unfair to students is ridiculous.',
'6a.': 'Without the right breaks, an individual cannot be an effective leader.',
'7a.': 'It doesn''t matter how much you try; some people just won''t like you.',
'8a.':' Heredity plays the major role in determining a person''s personality',
'9a.':' I have frequently found that what''s going to happen will happen.',
'10a.':'In the case of a well-prepared student,there is rarely, if ever, what would be known as an unfair test.',
'11a.':'Becoming a success is a result of hardwork, luck has very little or nothing to do with it.',
'12a.':'An average citizen can have an influence on governmental decisions.',
'13a.':'When I make plans, I am almost positive that I can make them work.',
'14a.':'There are some people who are just no good. ',
'15a.':'In my case, getting what I want has very little or nothing to do with luck.', 
'16a.':'Who gets to be the boss usually depends on who was fortunate enough to be in the right place first.',
'17a.':'In terms of world affairs, most of us are victims of forces we can neither understand or control.',
'18a.':'The majority of people don''t realise the extent to which their lives are controlled by accidental happenings.',
'19a.':'One should always be willing to admit mistakes.', 
'20a.': 'It is hard to know whether or not a person really likes you.',
'21a.':'In the long term, the bad things that happen to us are balanced out with the good ones.',
'22a.': 'With sufficient effort, we can abolish political corruption.',
'23a.':' Sometimes I can mot comprehend how teachers arrive at the grades they give.',
'24a.': 'A good leader expects people to make their own decisions about what they should do.',
'25a.': 'Frequently, I feel that I have little influence over the things that happen to me.',
'26a.':'Individuals are lonely because they do not try to be friendly.',
'27a.': 'There is too much emphasis on sports in high school.',
'28a.': 'What happens to me is my own doing.',
'29a.':'The majority of the time I ca not understand why politicians behave the way that they do.', 
}

questions_b={
'1b.': 'The problem with the majority of children today is that their parents are too easy on them.',
'2b.':' Individual''s misfortunes result from the mistakes they make.',
'3b.': 'There will always be wars, regardless of how much people try to prevent them.',
'4b.': 'Unfortunately, an individual''s worth often goes unrecognised no matter how hard they try.',
'5b.': 'Most students do not realise the extent of which their grades/results are influenced by accidental happenings.',
'6b.': 'Capable people who fail to become leaders have not taken advantage of the opportunities they were presented with.',
'7b.': 'People who can''t get others to like them don''t understand how to get along with others.',
'8b.':' It is an individual''s experiences in life which determine what they are like.',
'9b.':' Trusting in fate has never worked out as well for me as making a decision to take a definite course of action.',
'10b.': 'It is frequently the case that exam questions tend to be so unrelated to course work that studying is actually useless.',
'11b.':' Getting a good job is mostly about being in the right place at the right time.',
'12b.': 'This world is run by those few that are in power, and there''s not much that the little guy can do about it.',
'13b.':'It''s not always wise to plan too far in advance because many things turn out to be a case of good or bad luck anyway.',
'14b.': 'There is some good in everyone.', 
'15b.':' Many times we might as well just decide what to do by tossing a coin.',
'16b.': 'Getting individuals to do the right thing depends upon ability. Luck has very little or nothing to do with it.',
'17b.': 'By playing an active role in political and social affairs, the people can control world events.',
'18b.': 'There really is no such thing as luck.',
'19b.': 'Ii is usually best to cover up one''s mistakes.',
'20b.': 'How many friends you have depends on how nice a person you are.',
'21b.':' Most misfortunes come about as a result of lack of ability, laziness, ignorance, or all three.',
'22b.':'It is difficult for people to have much control over the things that politicians do in office.',
'23b.':' There is a direct connection between how hard I study and the grades that I get.',
'24b.': 'A good leader makes it clear to everyone what their jobs are.',
'25b.': 'It is impossible for me to believe that luck or chance plays a significant role in my life.',
'26b.':'There is not much use in trying too hard to please others, if they like you, they like you.',
'27b.': 'Team sports are an excellent way of building character.',
'28b.':'At times I feel I do not have enough control over the direction my life is heading.',
'29b.': 'In the long term, the people are responsible for bad government on a national as well as on a local level.',
}

load_base(questions_a,questions_b)
total_score = [] 
for i in range(len(scores)): 
    if answers[i] != scores[i]:
        total_score.append(0) 
    else:
        total_score.append(1)
# print (total_score) 
print('Your total score is:')
print(listsum(total_score))
x=listsum(total_score)
if x<12:
    print('You have Internal Locus of Control')
else:
    print('You have External Locus of Control')

    