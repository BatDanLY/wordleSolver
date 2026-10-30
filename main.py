from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random

class WordleLink:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get("https://wordleunlimited.org")

        self.driver.implicitly_wait(10)

        consentButton = self.driver.find_element(By.CLASS_NAME, "fc-cta-consent")
        consentButton.click()

        self.game = self.driver.find_element(By.TAG_NAME, "body")
        self.game.click()

        time.sleep(1)

        #not my solution to shadow dom issue
        deep_id_script = """
        function findElementByDeepId(id, root = document) {
            // Check if the current root contains the ID
            let element = root.querySelector('#' + id);
            if (element) return element;

            // If not, find all elements that host a shadow root
            let hosts = root.querySelectorAll('*');
            for (let host of hosts) {
                if (host.shadowRoot) {
                    // Recursively search inside this shadow root
                    element = findElementByDeepId(id, host.shadowRoot);
                    if (element) return element;
                }
            }
            return null;
        }
        return findElementByDeepId(arguments[0]);
        """
        self.board = self.driver.execute_script(deep_id_script, "board")


    def makeGuess(self, word):
        self.game.send_keys(word)
        self.game.send_keys(Keys.ENTER)


    def clearGuess(self):
        for i in range(0,5):
            self.game.send_keys(Keys.BACKSPACE)
            time.sleep(0.1)



    def collectRowData(self):
        rowData = []

        game_rows = self.board.find_elements(By.TAG_NAME, "game-row")
        for game_row in game_rows:
            data = []
            row_shadow = game_row.shadow_root
            letters = row_shadow.find_elements(By.CSS_SELECTOR, "game-tile")
            for letter in letters:
                letter_char = letter.get_attribute("letter")
                evaluation = letter.get_attribute("evaluation")

                if letter_char:
                    data.append((letter_char, evaluation))

            if data:
                rowData.append(data)

        return rowData

    def getBoardData(self):
        knownChars = ['', '', '', '', '']
        seenChars = {}
        defNotChars = []

        data = self.collectRowData()
        for row in data:
            for index in range(0,5):
                charData = row[index]
                match charData[1]:
                    case 'correct':
                        knownChars[index] = charData[0]
                    case 'present':
                        if charData[0] in seenChars:
                            seenChars[charData[0]] = seenChars[charData[0]] + [index]
                        else:
                            seenChars[charData[0]] = [index]
                    case 'absent':
                        defNotChars.append(charData[0])


        for index in range(0,5):
            if knownChars[index] in seenChars:
                if index in seenChars[knownChars[index]]:
                    print(f'found {knownChars[index]} in seenChars matching index {index}')
                    del seenChars[knownChars[index]]

            if knownChars[index] in defNotChars:
                print(f'founnd {knownChars[index]} in defNotChars. Now removed')
                defNotChars.remove(knownChars[index])

        for char in seenChars:
            if char in defNotChars:
                print(f'founnd {char} in defNotChars. Now removed')
                defNotChars.remove(char)


        return knownChars, seenChars, defNotChars



class WordleSolver:
    def __init__(self):
        with open("valid-wordle-words.txt", 'r') as file:
            self.wordList = file.read().splitlines()

        self.possibleWords = self.wordList

        self.seenChars = {}
        self.knownChars = []
        self.defNotChars = []

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

    def setChars(self, knownChars, seenChars, defNotChars):
        self.knownChars = knownChars
        self.seenChars = seenChars
        self.defNotChars = defNotChars




options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
IO = WordleLink(driver)
Solver = WordleSolver()


IO.makeGuess("raise")
time.sleep(2)
IO.makeGuess("donut")
time.sleep(1)
knownChars, seenChars, defNotChars = IO.getBoardData()
previousKnownChars = knownChars
previousSeenChars = seenChars
previousDefNotChars = defNotChars

for attempt in range(0,4):
    knownChars, seenChars, defNotChars = IO.getBoardData()
    time.sleep(1)
    Solver.setChars(knownChars, seenChars, defNotChars)
    possibleWords = Solver.findNextWord()
    print(possibleWords)
    time.sleep(1)
    IO.makeGuess(possibleWords[0])
    testKnownCharsIO, testSeenChars, testDefNotChars = IO.getBoardData()
    while testKnownCharsIO == knownChars and testSeenChars == seenChars and testDefNotChars == defNotChars:
        print("retrying")
        IO.clearGuess()
        nextWord = random.choices(possibleWords)
        IO.makeGuess(nextWord[0])
        time.sleep(1)
        testKnownCharsIO, testSeenChars, testDefNotChars = IO.getBoardData()