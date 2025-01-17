from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from funcs import webscrape, generateGuess, applyGuess, checkDone, getPossibleWords

MAX_GUESSES=9
NWORDS=4
FIRST_WORD="stare"
SECOND_WORD="pound"
THIRD_WORD="milky"

LETTER_FREQUENCIES={'a':43.31, 'b':10.56, 'c':23.13, 'd':17.25,'e':56.88,'f':9.24,'g':12.59,'h':15.31,'i':38.45,'j':1.0,'k':5.61,'l':27.98,'m':15.36,'n':33.92,'o':36.51,'p':16.14,'q':1.0,'r':38.64,'s':29.23,'t':35.43,'u':18.51,'v':5.13,'w':6.57,'x':1.48,'y':9.06,'z':1.39}
WRONG_LOCATIONS_DICT=[{},{},{},{}]
dict=[{},{},{},{}]
no_double_dict=[[],[],[],[]]

button_paths={
    'q':"/html/body/div/div/div[3]/div/div[1]/button[1]",
    'w':"/html/body/div/div/div[3]/div/div[1]/button[2]",
    'e':"/html/body/div/div/div[3]/div/div[1]/button[3]",
    'r':"/html/body/div/div/div[3]/div/div[1]/button[4]",
    't':"/html/body/div/div/div[3]/div/div[1]/button[5]",
    'y':"/html/body/div/div/div[3]/div/div[1]/button[6]",
    'u':"/html/body/div/div/div[3]/div/div[1]/button[7]",
    'i':"/html/body/div/div/div[3]/div/div[1]/button[8]",
    'o':"/html/body/div/div/div[3]/div/div[1]/button[9]",
    'p':"/html/body/div/div/div[3]/div/div[1]/button[10]",
    'a':"/html/body/div/div/div[3]/div/div[2]/button[1]",
    's':"/html/body/div/div/div[3]/div/div[2]/button[2]",
    'd':"/html/body/div/div/div[3]/div/div[2]/button[3]",
    'f':"/html/body/div/div/div[3]/div/div[2]/button[4]",
    'g':"/html/body/div/div/div[3]/div/div[2]/button[5]",
    'h':"/html/body/div/div/div[3]/div/div[2]/button[6]",
    'j':"/html/body/div/div/div[3]/div/div[2]/button[7]",
    'k':"/html/body/div/div/div[3]/div/div[2]/button[8]",
    'l':"/html/body/div/div/div[3]/div/div[2]/button[9]",
    'back':"/html/body/div/div/div[3]/div/div[3]/button[1]",
    'z':"/html/body/div/div/div[3]/div/div[3]/button[2]",
    'x':"/html/body/div/div/div[3]/div/div[3]/button[3]",
    'c':"/html/body/div/div/div[3]/div/div[3]/button[4]",
    'v':"/html/body/div/div/div[3]/div/div[3]/button[5]",
    'b':"/html/body/div/div/div[3]/div/div[3]/button[6]",
    'n':"/html/body/div/div/div[3]/div/div[3]/button[7]",
    'm':"/html/body/div/div/div[3]/div/div[3]/button[8]",
    'enter':"/html/body/div/div/div[3]/div/div[3]/button[9]",
}

def getGuessResult(progress_words, guess_word, nguesses, driver):
    labels=[[],[],[],[]]
    for i in range(1,6):
        labels[0].append(driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div[1]/div[1]/div[1]/div["+str(nguesses)+"]/div["+str(i)+"]").get_attribute("aria-label"))
        labels[1].append(driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div[1]/div[1]/div[2]/div["+str(nguesses)+"]/div["+str(i)+"]").get_attribute("aria-label"))
        labels[2].append(driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div[1]/div[2]/div[1]/div["+str(nguesses)+"]/div["+str(i)+"]").get_attribute("aria-label"))
        labels[3].append(driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div[1]/div[2]/div[2]/div["+str(nguesses)+"]/div["+str(i)+"]").get_attribute("aria-label"))

    for i in range(NWORDS):
        for j in range(5):
            if("incorrect" in labels[i][j]):
                if(guess_word[j] not in dict[i].keys()):
                    dict[i][guess_word[j]]=-1
                else:
                    no_double_dict[i].append(guess_word[j])
            elif("different" in labels[i][j]):
                if(guess_word[j] not in dict[i].keys()):
                    dict[i][guess_word[j]]=0
                if(guess_word[j] not in WRONG_LOCATIONS_DICT[i].keys()):
                    WRONG_LOCATIONS_DICT[i][guess_word[j]]=[j]
                else:
                    WRONG_LOCATIONS_DICT[i][guess_word[j]].append(j)
            else:
                dict[i][guess_word[j]]=j+1
                progress_words[i][j]=guess_word[j]
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

def numberSolved(progress_words):
    cnt = 0
    for words in progress_words:
        if('' not in words):
            cnt+=1
    return cnt

def run_quordle():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.quordle.com/#/")

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
        print("\n\nSorry. You were only able to solve "+str(nsolved)+"/"+str(NWORDS)+" words in "+str(MAX_GUESSES)+" guesses :(")
    else:
        print("\n\nCongrulations! You were able to solve all "+str(NWORDS)+" words in "+str(nguesses)+" guesses!")

    time.sleep(3)
    driver.close()
    return nsolved, MAX_GUESSES+1-nguesses 

if __name__=='__main__':
    run_quordle()