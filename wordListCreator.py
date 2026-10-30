inputFile = "words_alpha.txt"
outputFile = "wordleWordList.txt"

with open(inputFile, 'r') as file:
    words = file.read().splitlines()

wordleWords = [word for word in words if len(word) == 5]

with open(outputFile, 'w') as file:
    file.write('\n'.join(wordleWords))
