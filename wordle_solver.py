import time
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from funcs import generateGuess, applyGuess, checkDone, getPossibleWords, get_used_words

STARTER_WORD="stare"
SECOND_WORD="hound"
THIRD_WORD="milky"

MAX_GUESSES=6
NWORDS=1
SLEEP_TIME=1

LETTER_FREQUENCIES={'a':43.31, 'b':10.56, 'c':23.13, 'd':17.25,'e':56.88,'f':9.24,'g':12.59,'h':15.31,'i':38.45,'j':1.0,'k':5.61,'l':27.98,'m':15.36,'n':33.92,'o':36.51,'p':16.14,'q':1.0,'r':38.64,'s':29.23,'t':35.43,'u':18.51,'v':5.13,'w':6.57,'x':1.48,'y':9.06,'z':1.39}

def getGuessResult(progress_word, guess_word, nguesses, driver, dict, WRONG_LOCATIONS_DICT):
    # row_xpaths = ["/html/body/div/div/div[2]/div/div[1]/div", "/html/body/div/div/div[2]/div/div[1]/div/div[2]", 
    # "/html/body/div/div/div[2]/div/div[1]/div/div[3]", "/html/body/div/div/div[2]/div/div[1]/div/div[4]", 
    # "/html/body/div/div/div[2]/div/div[1]/div/div[5]", "/html/body/div/div/div[2]/div/div[1]/div/div[6]"]
    # row = driver.find_element(By.XPATH, row_xpaths[nguesses-1])

    row = driver.find_elements(By.CLASS_NAME, 'Row-module_row__dEHfN')[nguesses-1]

    keys = row.find_elements(By.CSS_SELECTOR, ".Tile-module_tile__3ayIZ")
    #check each 
    for i in range(5):
        time.sleep(0.1)
        #if letter is not in word
        if(keys[i].get_attribute("data-state")=='correct'):
            dict[guess_word[i]]=i+1
            progress_word[i]=guess_word[i]
        elif(keys[i].get_attribute("data-state")=='present'):
            if(guess_word[i] not in dict.keys()):
                    dict[guess_word[i]]=0
            if(guess_word[i] not in WRONG_LOCATIONS_DICT.keys()):
                WRONG_LOCATIONS_DICT[guess_word[i]]=[i]
            else:
                WRONG_LOCATIONS_DICT[guess_word[i]].append(i)
        else:
            dict[guess_word[i]]=-1
    return progress_word, dict, WRONG_LOCATIONS_DICT

def run_wordle():
    WRONG_LOCATIONS_DICT={}
    dict = {}
    no_double_dict=[]
    score=0
    possible_words, progress_word = getPossibleWords("words.txt", NWORDS)
    used_words = get_used_words()
    possible_words=possible_words[0]

    good_words = []
    for word in possible_words:
        if('s' in word and 't' in word and 'a' in word and 'e' in word and 'r' in word):
            good_words.append(word)

    progress_word=progress_word[0]

    driver = webdriver.Chrome()
    driver.get("https://www.nytimes.com/games/wordle/index.html")

    #this click gets rid of popup
    time.sleep(SLEEP_TIME)
    driver.execute_script('el=document.elementFromPoint(20,20); el.click();')
    time.sleep(SLEEP_TIME)

    buttons = driver.find_elements_by_tag_name('button')[4:]

    #first apply initial guess
    guesses=1
    applyGuess(STARTER_WORD, driver, buttons)

    guess_word=STARTER_WORD
    time.sleep(SLEEP_TIME)
    progress_word, dict, WRONG_LOCATIONS_DICT = getGuessResult(progress_word, STARTER_WORD, guesses, driver, dict, WRONG_LOCATIONS_DICT)

    #if found no letters at all, apply second guess
    if(all(v<0 for k,v in dict.items()) and SECOND_WORD not in used_words):
        guesses=2
        applyGuess(SECOND_WORD, driver, buttons)
        guess_word=SECOND_WORD
        time.sleep(SLEEP_TIME)
        progress_word, dict, WRONG_LOCATIONS_DICT = getGuessResult(progress_word, SECOND_WORD, guesses, driver, dict, WRONG_LOCATIONS_DICT)

    #if still found no letters, apply third guess
    if(all(v<0 for k,v in dict.items()) and THIRD_WORD not in used_words):
        guesses=3
        applyGuess(THIRD_WORD, driver, buttons)
        guess_word=THIRD_WORD
        time.sleep(SLEEP_TIME)
        progress_word, dict, WRONG_LOCATIONS_DICT = getGuessResult(progress_word, THIRD_WORD, guesses, driver, dict, WRONG_LOCATIONS_DICT)

    # should have at least one letter now, so go until correct word found
    while(not(checkDone(progress_word)) and guesses<MAX_GUESSES):
        guess_word, possible_words, dict, WRONG_LOCATIONS_DICT, no_double_dict = generateGuess(dict, progress_word, possible_words, used_words, dict, WRONG_LOCATIONS_DICT, no_double_dict)
        guesses+=1
        applyGuess(guess_word, driver, buttons)
        time.sleep(SLEEP_TIME)
        progress_word, dict, WRONG_LOCATIONS_DICT = getGuessResult(progress_word, guess_word, guesses, driver, dict, WRONG_LOCATIONS_DICT)

    if(not(checkDone(progress_word))):
        print("\n\nSorry. You were unable to solve the word in 6 guesses :(")
    else:
        print("\n\nCongrulations! You were able to discover the true word ("+guess_word+") in "+str(guesses)+" guesses!")
        score=1

    time.sleep(SLEEP_TIME)
    driver.close()
    return score, (MAX_GUESSES+1)-guesses

if __name__=='__main__':
    run_wordle()