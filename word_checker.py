from funcs import getPossibleWords, get_used_words

possible_words, _ = getPossibleWords("words.txt", 5)
possible_words = possible_words[0]

used_words = get_used_words()


# list=[]

# for word in possible_words:
#     if(word[1]!='e' and word[3]!='i' and word[4]!='l' and word[1]!='a' and word[2]!='i' and word[0]!='u' and word[1]!='n' and word[2]!='d' and word[1]!='e' and word[3]=='a'):
#         list.append(word)

# print(list)


while(True):
    guess_word=input("check word: \n")
    print("in possible words: "+str(guess_word in possible_words))
    print("in used words: "+str(guess_word in used_words)+"\n\n")