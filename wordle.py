import string

class wordle:
    def __init__(self, word):
        self.correct_word = word.upper()

    def guess(self, guess):
        correct_letters = []
        partial_letters = []
        incorrect_letters = set()
        for i in range(len(self.correct_word)):
            if guess[i] == self.correct_word[i]:
                correct_letters.append((i,guess[i]))
            elif guess[i] in self.correct_word:
                partial_letters.append((i,guess[i]))
            else:
                incorrect_letters.add(guess[i])
        return correct_letters, partial_letters, incorrect_letters

class manual_wordle:
    def __init__(self):
        return

    def guess(self, guess):
        print(guess)
        correct_letters = []
        partial_letters = []
        incorrect_letters = set()
        for pos in range(len(guess)):
            letter = guess[pos]
            status = input(letter+' correct? (y/n/p): ')
            if status=='y':
                correct_letters.append((pos,letter))
            elif status=='p':
                partial_letters.append((pos,letter))
            else:
                incorrect_letters.add(letter)
        return correct_letters, partial_letters, incorrect_letters

class solver:
    def __init__(self, length, wordle=manual_wordle(), word_bank=None):
        self.length = length
        self.available_letters = set(list(string.ascii_uppercase))
        self.correct_letters = set()
        self.wordle = wordle
        if word_bank != None:
            self.word_bank = word_bank
        else:
            self.word_bank = build_word_bank(length)
    
    def guess(self, guess):
        guess = guess.upper()
        print(guess)
        print(len(self.word_bank))
        corrects, partials, incorrects = self.wordle.guess(guess)
        # print(corrects)
        # print(partials)
        # print(incorrects)
        for correct in corrects:
            self.trim_from_correct(correct)
        for incorrect in incorrects:
            self.trim_from_incorrect(incorrect)
        for partial in partials:
            self.trim_from_partial(partial)
        if guess in self.word_bank:
            if len(self.word_bank) == 1:
                return guess
            self.word_bank.remove(guess)
        #TODO: see if there are extra pieces of information ini what's left in the bank
        return -1

    def trim_from_correct(self, correct):
        misses = set()
        for word in self.word_bank:
            if word[correct[0]] != correct[1]:
                misses.add(word)
        self.word_bank-=misses
        self.correct_letters.add(correct)

    def trim_from_partial(self, partial):
        misses = set()
        for word in self.word_bank:
            if partial[1] not in word:
                misses.add(word)
        self.word_bank-=misses
        for word in self.word_bank:
            if word[partial[0]] == partial[1]:
                misses.add(word)
        self.word_bank-=misses

    def trim_from_incorrect(self, incorrect):
        try:
            self.available_letters.remove(incorrect)
        except:
            pass
        misses = set()
        for word in self.word_bank:
            if incorrect in word:
                misses.add(word)
        self.word_bank-=misses

    def solve(self):
        ans = -1
        count = 0
        while ans == -1:
            count += 1
            ans = self.guess(self.select_best_guess())
        return ans,count

    def select_best_guess(self):
        if len(self.word_bank) == 1 or len(self.correct_letters) < self.length-1:
            return self.select_most_used_letters()
        return self.downselect()
        
    def downselect(self):
        remaining_letters = set()
        for word in self.word_bank:
            for letter in word:
                remaining_letters.add(letter)
        for correct_letter in self.correct_letters:
            try:
                remaining_letters.remove(correct_letter[1])
            except:
                pass
        # remaining_letters-=self.correct_letters
        fresh_bank = build_word_bank(self.length)
        best_word = ''
        best_count = 0
        for word in fresh_bank:
            count = 0
            for letter in remaining_letters:
                if letter in word:
                    count+=1
            if count > best_count:
                best_word = word
                best_count = count
        return best_word

        

    def select_most_used_letters(self, available_letters=None):
        #TODO: don't reuse letters?
        #TODO: position based filtering?
        letter_freq = 'ESIARNTOLCDUGPMKHBYFVWZXQJ'
        if available_letters == None:
            available_letters = set(self.available_letters)
        temp_word_bank = set(self.word_bank)
        for _ in range(self.length):
            best_letter = 'J'
            count = 0
            for letter in available_letters:
                letter_count = 0
                for word in self.word_bank:
                    if letter in word:
                        letter_count+=1
                if letter_count >= count:
                    possible = False
                    for word in temp_word_bank:
                        if letter in word:
                            possible = True
                            break
                    if possible:
                        if letter_count==count:
                            #when equal prefer dictionary frequency of the letter
                            if letter_freq.find(letter) > letter_freq.find(best_letter):
                                continue
                        count = letter_count
                        best_letter = letter
            if count == 0:
                break
            remove_bank = set()
            available_letters.remove(best_letter)
            for word in temp_word_bank:
                if best_letter not in word:
                    remove_bank.add(word)
            temp_word_bank-=remove_bank
        return list(temp_word_bank)[0]

    def select_most_used_letters_recursive(self):
        #Filters after each letter is selected, so it does the most likely letter if the word includes the first letter
        available_letters = set(self.available_letters)
        temp_word_bank = set(self.word_bank)
        for _ in range(self.length):
            best_letter = ''
            count = 0
            for letter in available_letters:
                letter_count = 0
                for word in temp_word_bank:
                    if letter in word:
                        letter_count+=1
                if letter_count > count:
                    count = letter_count
                    best_letter = letter
            if best_letter == '':
                break
            remove_bank = set()
            available_letters.remove(best_letter)
            for word in temp_word_bank:
                if best_letter not in word:
                    remove_bank.add(word)
            temp_word_bank-=remove_bank
        return list(temp_word_bank)[0]

def build_word_bank(length):
    word_bank = set()
    with open('word_list.txt', 'r') as f:
        for line in f.readlines():
            word = line.strip()
            if len(word) == length:
                word_bank.add(word.upper())
    return word_bank
