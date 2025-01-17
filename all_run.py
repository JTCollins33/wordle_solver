from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from wordle_solver import run_wordle
from quordle_solver import run_quordle
from octordle_solver import run_octordle


if __name__=='__main__':
    nright=0,
    score=0
    
    # nright, score = run_wordle()
    nright2, score2 = run_quordle()
    nright3, score3 = run_octordle()

    print("\n\nPercentage Correct Performance: "+str(100*(nright+nright2+nright3)/13)+"%")
    print("Overall Score: ", score+score2+score3)