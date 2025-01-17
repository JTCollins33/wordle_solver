import math
import re
import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from collections import Counter


LETTER_FREQUENCIES={'a':43.31, 'b':10.56, 'c':23.13, 'd':17.25,'e':56.88,'f':9.24,'g':12.59,'h':15.31,'i':38.45,'j':1.0,'k':5.61,'l':27.98,'m':15.36,'n':33.92,'o':36.51,'p':16.14,'q':1.0,'r':38.64,'s':29.23,'t':35.43,'u':18.51,'v':5.13,'w':6.57,'x':1.48,'y':9.06,'z':1.39}
BUTTON_MAPPING_DICT={'q':0, 'w':1, 'e':2, 'r':3, 't':4, 'y':5, 'u':6, 'i':7, 'o':8, 'p':9,
                    'a':10, 's':11, 'd':12, 'f':13, 'g':14, 'h':15, 'j':16, 'k':17, 'l':18,
                    'enter':19, 'z':20, 'x':21, 'c':22, 'v':23, 'b':24, 'n':25, 'm':26, 'back':27}

def get_used_words():
    used_words=[]
    driver = webdriver.Chrome()
    driver.get("https://wordfinder.yourdictionary.com/wordle/answers/")
    words = driver.find_elements(By.TAG_NAME, 'strong')
    for word in words:
        used_words.append(word.text.lower())
    driver.close()
    return used_words

def getPossibleWords(file, NWORDS):
    if(file not in os.listdir("./")):
        webscrape(file)

    possible_words=[]
    progress_words=[]
    for i in range(NWORDS):
        possible_words.append([])
        progress_words.append(['','','','',''])

    f = open(file, 'r')
    lines = f.readlines()
    for line in lines:
        word = line.strip()
        if(len(word)==5):
            for i in range(NWORDS):
                possible_words[i].append(word)
    f.close()
    return possible_words, progress_words

def webscrape(file):
    f = open(file, 'w')

    driver2 = webdriver.Chrome('./chromedriver')
    driver2.get("https://www.wordunscrambler.net/word-list/wordle-word-list")
    content = driver2.find_element_by_css_selector(".content")
    words = content.find_elements_by_xpath("//a[@href]")

    for i in range(len(words)):
        if(len(words[i].text)==5):
            f.write(words[i].text+"\n")

    driver2.close()
    f.close()

def eliminateWords(index, possible_words, used_words, dict, WRONG_LOCATIONS_DICT, no_double_dict):
    remove_list=[]
    for i in range(len(possible_words)):
        #remove words that have already been used
        if(possible_words[i] in used_words):
            remove_list.append(possible_words[i])

        else:
            for k,v in dict.items():
                #if letter in possible word that was already proved to not be in the word,
                #remove it from list of possible words
                if(k in possible_words[i] and v==-1):
                    remove_list.append(possible_words[i])
                    break

                #if know exact location of a letter,
                #remove any words that don't have the letter at that location
                if(v>0 and possible_words[i][v-1]!=k):
                    remove_list.append(possible_words[i])
                    break

                #if found a letter in the word (but not in right spot)
                #and that letter not in possible word, remove it
                if(v==0 and k not in possible_words[i]):
                    remove_list.append(possible_words[i])
                    break
                
                if(k in possible_words[i] and (k in WRONG_LOCATIONS_DICT.keys()) and (any(i3 in [i2.start() for i2 in re.finditer(k, possible_words[i])] for i3 in WRONG_LOCATIONS_DICT[k]))):
                    remove_list.append(possible_words[i])
                    break

                #check if possible word has double letter which has already been tried
                if(any(i2 in no_double_dict for i2 in [k2 for k2,v2 in Counter(possible_words[i]).items() if v2>1])):
                    remove_list.append(possible_words[i])
                    break

    return [w for w in possible_words if w not in remove_list], dict, WRONG_LOCATIONS_DICT, no_double_dict

def mostProbableWord(possible_words, progress_word):
    highest_freq_avg=-math.inf
    most_prob_word=""
    for word in possible_words:
        freq_sum=0
        n=0
        for letter in word.lower():
            if(letter not in progress_word):
                freq_sum+=LETTER_FREQUENCIES[letter]
                n+=1

        #penalize double letters slightly
        for k,v in Counter(word).items():
            if(v>1):
                freq_sum-=(LETTER_FREQUENCIES[k]/2)*(v-1)

        if(n>0):
            #get average frequency value
            freq_avg = freq_sum/n
            if(freq_avg>highest_freq_avg):
                highest_freq_avg=freq_avg
                most_prob_word=word
        #this is if already know the word
        else:
            highest_freq_avg=math.inf
            most_prob_word=word
    return most_prob_word

def generateGuess(index, progress_word, possible_words, used_words, dict, WRONG_LOCATIONS_DICT, no_double_dict):
    possible_words, dict, WRONG_LOCATIONS_DICT, no_double_dict=eliminateWords(index, possible_words, used_words, dict, WRONG_LOCATIONS_DICT, no_double_dict)
    return mostProbableWord(possible_words, progress_word), possible_words, dict, WRONG_LOCATIONS_DICT, no_double_dict

def applyGuess(guess_word, driver, buttons):
    time.sleep(2)
    #guess each letter
    for letter in guess_word:
        driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable(buttons[BUTTON_MAPPING_DICT[letter]])))
    #apply guess
    driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable(buttons[BUTTON_MAPPING_DICT['enter']])))

def checkDone(progress_words):
    return not('' in progress_words)