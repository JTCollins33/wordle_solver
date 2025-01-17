from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import math
import os
from funcs import webscrape, generateGuess, applyGuess, checkDone, getPossibleWords


MAX_GUESSES=13
NWORDS=8
FIRST_WORD="stare"
SECOND_WORD="pound"
THIRD_WORD="milky"

LETTER_FREQUENCIES={'a':43.31, 'b':10.56, 'c':23.13, 'd':17.25,'e':56.88,'f':9.24,'g':12.59,'h':15.31,'i':38.45,'j':1.0,'k':5.61,'l':27.98,'m':15.36,'n':33.92,'o':36.51,'p':16.14,'q':1.0,'r':38.64,'s':29.23,'t':35.43,'u':18.51,'v':5.13,'w':6.57,'x':1.48,'y':9.06,'z':1.39}
WRONG_LOCATIONS_DICT=[{},{},{},{},{},{},{},{}]
dict=[{},{},{},{},{},{},{},{}]
no_double_dict=[[],[],[],[],[],[],[],[]]

button_paths={
    'q':"//*[@id='keyboard-wrap']/div[2]/button[1]",
    'w':"//*[@id='keyboard-wrap']/div[2]/button[2]",
    'e':"//*[@id='keyboard-wrap']/div[2]/button[3]",
    'r':"//*[@id='keyboard-wrap']/div[2]/button[4]",
    't':"//*[@id='keyboard-wrap']/div[2]/button[5]",
    'y':"//*[@id='keyboard-wrap']/div[2]/button[6]",
    'u':"//*[@id='keyboard-wrap']/div[2]/button[7]",
    'i':"//*[@id='keyboard-wrap']/div[2]/button[8]",
    'o':"//*[@id='keyboard-wrap']/div[2]/button[9]",
    'p':"//*[@id='keyboard-wrap']/div[2]/button[10]",

    'a':"//*[@id='keyboard-wrap']/div[3]/button[1]",
    's':"//*[@id='keyboard-wrap']/div[3]/button[2]",
    'd':"//*[@id='keyboard-wrap']/div[3]/button[3]",
    'f':"//*[@id='keyboard-wrap']/div[3]/button[4]",
    'g':"//*[@id='keyboard-wrap']/div[3]/button[5]",
    'h':"//*[@id='keyboard-wrap']/div[3]/button[6]",
    'j':"//*[@id='keyboard-wrap']/div[3]/button[7]",
    'k':"//*[@id='keyboard-wrap']/div[3]/button[8]",
    'l':"//*[@id='keyboard-wrap']/div[3]/button[9]",

    'back':"//*[@id='keyboard-wrap']/div[4]/button[1]",
    'z':"//*[@id='keyboard-wrap']/div[4]/button[2]",
    'x':"//*[@id='keyboard-wrap']/div[4]/button[3]",
    'c':"//*[@id='keyboard-wrap']/div[4]/button[4]",
    'v':"//*[@id='keyboard-wrap']/div[4]/button[5]",
    'b':"//*[@id='keyboard-wrap']/div[4]/button[6]",
    'n':"//*[@id='keyboard-wrap']/div[4]/button[7]",
    'm':"//*[@id='keyboard-wrap']/div[4]/button[8]",
    'enter':"//*[@id='keyboard-wrap']/div[4]/button[9]",
}

def getGuessResult(progress_words, guess_word, nguesses, driver):
    labels=[[],[],[],[],[],[],[],[]]
    for i in range(1,6):
        for j in range(NWORDS):
            labels[j].append(driver.find_element_by_xpath("//*[@id='board-"+str(j+1)+"']/div["+str(nguesses)+"]/div["+str(i)+"]").get_attribute("class"))

    for i in range(NWORDS):
        for j in range(5):
            if("exact" in labels[i][j]):
                dict[i][guess_word[j]]=j+1
                progress_words[i][j]=guess_word[j]
            elif("match" in labels[i][j]):
                if(guess_word[j] not in dict[i].keys()):
                    dict[i][guess_word[j]]=0
                if(guess_word[j] not in WRONG_LOCATIONS_DICT[i].keys()):
                    WRONG_LOCATIONS_DICT[i][guess_word[j]]=[j]
                else:
                    WRONG_LOCATIONS_DICT[i][guess_word[j]].append(j)
            else:
                if(guess_word[j] not in dict[i].keys()):
                    dict[i][guess_word[j]]=-1
                else:
                    no_double_dict[i].append(guess_word[j])
    return progress_words

def chooseSector(dicts, progress_words):
    max_index = 0
    max_sum=0
    for i in range(NWORDS):
        sum=0
        for v in dicts[i].values():
            if(v==0):
                sum+=0.5
            elif(v>0):
                sum+=1
        if(sum>max_sum and ('' in progress_words[i])):
            max_sum=sum
            max_index=i
    return max_index

def chooseSectorMin(dicts, progress_words):
    min_index = 0
    min_sum=math.inf
    for i in range(NWORDS):
        sum=0
        for v in dicts[i].values():
            if(v==0):
                sum+=0.5
            elif(v>0):
                sum+=1
        if(sum<min_sum and ('' in progress_words[i])):
            min_sum=sum
            min_index=i
    return min_index

def numberSolved(progress_words):
    cnt = 0
    for words in progress_words:
        if('' not in words):
            cnt+=1
    return cnt

def run_octordle():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://octordle.com/daily")

    possible_words, progress_words = getPossibleWords("words.txt", NWORDS)

    #apply first three guesses
    applyGuess(FIRST_WORD, driver, button_paths)
    nguesses=1
    progress_words=getGuessResult(progress_words, FIRST_WORD, nguesses, driver)

    applyGuess(SECOND_WORD, driver, button_paths)
    nguesses+=1
    progress_words=getGuessResult(progress_words, SECOND_WORD, nguesses, driver)

    applyGuess(THIRD_WORD, driver, button_paths)
    nguesses+=1
    progress_words=getGuessResult(progress_words, THIRD_WORD, nguesses, driver)

    while(not(checkDone(progress_words)) and nguesses<MAX_GUESSES):
        index = chooseSector(dict, progress_words)
        guess_word, possible_words[index], dict[index], WRONG_LOCATIONS_DICT[index], no_double_dict[index] = generateGuess(index, progress_words[index], possible_words[index], dict[index], WRONG_LOCATIONS_DICT[index], no_double_dict[index])
        nguesses+=1
        applyGuess(guess_word, driver, button_paths)
        progress_words = getGuessResult(progress_words, guess_word, nguesses, driver)

    nsolved = numberSolved(progress_words)
    if(not(checkDone(progress_words))):
        print("\n\nSorry. You only able to solve "+str(nsolved)+"/"+str(NWORDS)+" words in "+str(MAX_GUESSES)+" guesses :(")
    else:
        print("\n\nCongrulations! You were able to solve all "+str(NWORDS)+" sections in "+str(nguesses)+" guesses!")

    time.sleep(5)
    driver.close()
    return nsolved, MAX_GUESSES+1-nguesses

if __name__=='__main__':
    run_octordle()