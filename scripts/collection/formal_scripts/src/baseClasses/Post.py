#!/usr/bin/env python3

from abc import ABC, abstractclassmethod
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class Post(ABC):

  title: str
  content: str
  responses: str 
  # Can add other data points in subclasses based on needs of the website

  ######## Public Class Methods ########
  @abstractclassmethod
  def get_title():
    pass

  @abstractclassmethod
  def get_content():
    pass

  @abstractclassmethod
  def get_replies():
    pass

  ######## Private Class Methods ########