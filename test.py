class WordleSolver:
    def __init__(self):
        with open("wordleWordList.txt", 'r') as file:
            self.wordList = file.read().splitlines()

        self.word = "salet"

        self.possibleWords = self.wordList

        self.seenChars = {'a': [1,2], 'b': [0]}
        self.knownChars = ['', 'e', '', 'r', '']
        self.defNotChars = ['s', 'l', 't', 'd']



    def seenCharsCheck(self):
        if not self.seenChars:
            return

        resultList = []

        for word in self.possibleWords:
            word_valid = True

            for char, forbidden_indices in self.seenChars.items():
                if char not in word:
                    word_valid = False
                    break

                if any(word[pos] == char for pos in forbidden_indices if pos < len(word)):
                    word_valid = False
                    break

            if word_valid:
                resultList.append(word)

        self.possibleWords = resultList

    def knownCharsCheck(self):
        resultList = []

        for word in self.possibleWords:
            good = True
            for index in range(0,5):
                if self.knownChars[index] != '':
                    if word[index] != self.knownChars[index]:
                        good = False

            if good or self.knownChars == ['', '', '', '', '']:
                resultList.append(word)

        self.possibleWords = resultList


    def defNotCharsCheck(self):
        resultList = []

        for word in self.possibleWords:
            foundChar = False
            for char in self.defNotChars:
                if char in word:
                    foundChar = True
            if not foundChar:
                resultList.append(word)


        self.possibleWords = resultList


    def findNextWord(self):
        self.seenCharsCheck()
        self.knownCharsCheck()
        self.defNotCharsCheck()


        return self.possibleWords




test = WordleSolver()
print(test.findNextWord())