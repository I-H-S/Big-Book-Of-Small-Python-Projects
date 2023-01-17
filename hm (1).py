import random, sys
GARBAGE_CHARS = '~!@#$%^&*()_+-={}[]|;:,.<>?/'
with open('sevenletterwords.txt') as wordListFile:
    WORDS = wordListFile.readlines()
for i in range(len(WORDS)):
    WORDS[i] = WORDS[i].strip().upper()

def main():
    """Run a single game of Hacking."""
    print('''Hacking Minigame, by Al Sweigart al@inventwithpython.com
    Find the password in the computer's memory. You are given clues after each guess. For example, if the secret password is MONITOR but the player guessed CONTAIN, they are given the hint that 2 out of 7 letters were correct, because both MONITOR and CONTAIN have the letter O and as their 2nd and 3rd letter. You get four guesses.\n''')
    input('Press Enter to begin...')

    gameWords = getWords()
    computerMemory = getComputerMemoryString(gameWords)
    secretPassword = random.choice(gameWords)

    print(computerMemory)
    for triesRemaining in range(4, 0, -1):
        playerMove = askForPlayerGuess(gameWords, triesRemaining)
        if playerMove == secretPassword:
            print('A C C E S S G R A N T E D')
            return
        else:
            numMatches = numMatchingLetters(secretPassword, playerMove)
            print('Access Denied ({}/7 correct)'.format(numMatches))
    print('Out of tries. Secret password was {}.'.format(secretPassword))

def getWords():
    """Return a list of 12 words that could possibly be the password. The secret password will be the first word in the list. To make the game fair, we try to ensure that there are words with a range of matching numbers of letters as the secret word."""
    secretPassword = random.choice(WORDS)
    words = [secretPassword]

    while len(words) < 3:
        randomWord = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) == 0:
            words.append(randomWord)
    for i in range(500):
        if len(words) == 5:
            break # Found 5 words, so break out of the loop.

        randomWord = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) == 3:
            words.append(randomWord)

    for i in range(500):
        if len(words) == 12:
                    break

        randomWord = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) != 0:
            words.append(randomWord)
    while len(words) < 12:
        randomWord = getOneWordExcept(words)
        words.append(randomWord)
        
    assert len(words) == 12
    return words
    
def getOneWordExcept(blocklist=None):
    """Returns a random word from WORDS that isn't in blocklist."""
    if blocklist == None:
        blocklist = []
        
    while True:
        randomWord = random.choice(WORDS)
        if randomWord not in blocklist:
            return randomWord
            
def numMatchingLetters(word1, word2):
    """Returns the number of matching letters in these two words."""
    matches = 0
    for i in range(len(word1)):
        if word1[i] == word2[i]:
            matches += 1
    return matches
    
    
def getComputerMemoryString(words):
    """Return a string representing the "computer memory"."""
    
    linesWithWords = random.sample(range(16 * 2), len(words))
    memoryAddress = 16 * random.randint(0, 4000)
    
    computerMemory = [] # Will contain 16 strings, one for each line.
    nextWord = 0
    for lineNum in range(16):
        leftHalf = ''
        rightHalf = ''
        for j in range(16):
            leftHalf += random.choice(GARBAGE_CHARS)
            rightHalf += random.choice(GARBAGE_CHARS)
            
        if lineNum in linesWithWords:
            insertionIndex = random.randint(0, 9)
            leftHalf = (leftHalf[:insertionIndex] + words[nextWord]
                + leftHalf[insertionIndex + 7:])
            nextWord += 1
        if lineNum + 16 in linesWithWords:
            insertionIndex = random.randint(0, 9)
            rightHalf = (rightHalf[:insertionIndex] + words[nextWord]
                + rightHalf[insertionIndex + 7:])
            nextWord += 1
            
        computerMemory.append('0x' + hex(memoryAddress)[2:].zfill(4)
                    + '  ' + leftHalf + '    '
                    + '0x' + hex(memoryAddress + (16*16))[2:].zfill(4)
                    + ' ' + rightHalf)
        memoryAddress += 16 # Jump from, say, 0xe680 to 0xe690.
        
    return '\n'.join(computerMemory)
    
def askForPlayerGuess(words, tries):
    """Let the player enter a password guess."""
    while True:
        print('Enter password: ({} tries remaining)'.format(tries))
        guess = input('> ').upper()
        if guess in words:
            return guess
        print('That is not one of the possible passwords listed above.')
        print('Try entering "{}" or "{}".'.format(words[0], words[1]))
        
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit() # When Ctrl-C is pressed, end the program.