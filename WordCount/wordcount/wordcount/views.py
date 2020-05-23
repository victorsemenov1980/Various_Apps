#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 12:54:55 2020

@author: user
"""
from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'index.html',{'hi':'This is me'})

def count(request):
    input_text=request.GET['input']
    words=input_text.split()
    x=len(words)
    return render(request, 'count.html',{'count': x})

def about(request):
    return render(request, 'about.html',{'hi':'This is my home page'})
                                        