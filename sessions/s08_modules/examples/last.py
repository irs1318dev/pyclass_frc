import sys

last_word = sys.argv[1].lower()
for word in sys.argv[2:]:
    word = word.lower()
    if word > last_word:
        last_word = word
print("last: ", last_word)
