# wordle_bot
A quick and dirty bot to play wordle. 

# Usage
import wordle
wordle.solver(word_length).solve()


or


wordle.solver(word_length, wordle.wordle(your_word)).solve()

if you want to manually enter guesses before running the automated solver you can call solver.guess(your_guess) before running solve
