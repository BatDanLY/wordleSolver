# Wordle Solver

A Python program that uses Selenium to play Wordle automatically on [Wordle Unlimited](https://wordleunlimited.org).

The program reads the current state of the board, works out which letters are correct or in the wrong position, and uses that information to narrow down a list of possible words. It then picks a word from the remaining options and submits it as the next guess.

## How it works

The program is split into two main classes:

### WordleLink

Handles the interaction with the Wordle website using Selenium.

- Opens Wordle Unlimited in Chrome.
- Accepts the cookie consent prompt.
- Finds the game board, including elements inside shadow roots.
- Enters guesses and clears the current row when needed.
- Reads the letters and their evaluations from previous guesses.

The board data is collected and split into three groups:

- **Known characters:** Letters in the correct position (green).
- **Seen characters:** Letters that are in the word but in the wrong position (yellow).
- **Excluded characters:** Letters that are not in the word (grey).

### WordleSolver

Uses the information collected from the board to filter a list of valid Wordle words.

It checks each possible word against the known characters, seen characters and excluded characters. Any word that doesn't match the current information is removed from the list.

The remaining words are used to make the next guess.

## Requirements

You'll need:

- Python 3.10 or later (the program uses `match` statements).
- Google Chrome.
- Selenium.

Install Selenium using pip:

```bash
pip install selenium
```

Selenium Manager should handle the ChromeDriver setup automatically in most cases.

## Setup

1. Clone or download this repository.
2. Make sure Google Chrome is installed.
3. Install the required Python package.
4. Make sure `valid-wordle-words.txt` is in the same directory as the Python script.
5. Run the program:

```bash
python main.py
```

## Notes

The program currently starts with the guesses `raise` and `donut` before using the board information to narrow down the remaining words.

It then makes up to four further guesses. If a submitted guess doesn't appear to update the board, the program clears the row and tries another word from the possible words list.

The browser is left open after the script finishes.

The program was made to work with Wordle Unlimited, so changes to the website's HTML or shadow DOM structure may cause parts of it to stop working.

## Word List

The word list used by this project was taken from [dracos' valid Wordle words gist](https://gist.github.com/dracos/dd0668f281e685bad51479e5acaadb93#file-valid-wordle-words-txt-L10).

Credit goes to the original author for providing the word list.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
