#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 16 22:32:01 2020

@author: user
"""


import requests
from bs4 import BeautifulSoup
import pandas

r = requests.get("http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
c=r.content

soup=BeautifulSoup(c,"html.parser")

all=soup.find_all("div",{"class":"propertyRow"})

all[0].find("h4",{"class":"propPrice"}).text.replace("\n","").replace(" ","")

page_nr=soup.find_all("a",{"class":"Page"})[-1].text
print(page_nr,"pages were found")

'''find data, get data, save csv file'''
#for all the pages we will need to put all the code into this FOR loop
base_url="http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="

for page in range(0,int(page_nr)*10,10):
    print(base_url+str(page)+'.html')
    r=requests.get(base_url+str(page)+'.html')

# r = requests.get("http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})

    c=r.content
    soup=BeautifulSoup(c,'html.parser')
    print(soup.prettify())
    ''' Search page outputs reside in class property row divs'''
    all=soup.find_all('div',{'class':'propertyRow'})
    # print(all)
    # x=all[0].find_all('h4')
    # print(x)
    '''Prices'''
# for item in all:
#     print(item.find_all('h4')[0].text.replace('\n','').replace('',''))
#     '''Addressess'''
#     print(item.find_all('span',{'class':'propAddressCollapse'})[0].text)
#     print(item.find_all('span',{'class':'propAddressCollapse'})[1].text)
#     print()
#     # print(item.find_all('span'))
#     # print()
#     '''number of beds,square and bathes'''
#     try:#if there is no info the text method will return error
#         print(item.find('span',{'class':'infoBed'}).find('b').text,'bedrooms')
#     except:
#         print('Note available')
#     try:#if there is no info the text method will return error
#         print(item.find('span',{'class':'infoSqFt'}).find('b').text,'square feet')
#     except:
#          print('Note available')
#     try:#if there is no info the text method will return error
#         print(item.find('span',{'class':'infoValueFullBath'}).find('b').text,'full bathrooms')
#     except:
#         print('Note available')
    
#     print()
#     print()

    '''
    Will make a list of dicts'''
    
    l=[]
    for item in all:
        d={}
        d['Price']=item.find_all('h4')[0].text.replace('\n','').replace('','')
        d['Address']=item.find_all('span',{'class':'propAddressCollapse'})[0].text
        try:
            d['Locality']=item.find_all('span',{'class':'propAddressCollapse'})[1].text
        except:
            d['Locality']='Note available'
        try:#if there is no info the text method will return error
            d['Bedrooms']=item.find('span',{'class':'infoBed'}).find('b').text
        except:
            d['Bedrooms']='Note available'
        try:#if there is no info the text method will return error
            d['Square']=item.find('span',{'class':'infoSqFt'}).find('b').text
        except:
             d['Square']='Note available'
        try:#if there is no info the text method will return error
            d['Bathrooms']=item.find('span',{'class':'infoValueFullBath'}).find('b').text
        except:
            d['Bathrooms']='Note available'
        l.append(d)
print(l)


df=pandas.DataFrame(l)
# print(df)
df.to_csv('test.csv')
