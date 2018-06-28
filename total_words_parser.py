"""
Parse all transcripts and output word frequencies for each character found
"""
import re
from collections import Counter

transcript_folder = 'transcripts/'
# all characters and a counter of their words
characters = {}
# counter of number of lines spoken by character
num_lines_character = Counter()
# number of times each word is seen in any dialog
all_words = Counter()
# calculated unique words for each character
character_unique_words = {}


# find what percentage each word makes up of a characters dialog and normalize based off of the overall word use
def calc_word_uniqueness():
    anyone_speaks = sum(all_words.values())

    for person in characters:
        unique_words = {}
        person_speaks = num_lines_character[person]

        counts = characters[person]
        for word in counts:
            anyone_says_word = all_words[word]
            person_says_word = counts[word]

            uniqueness = ((person_says_word**2)/anyone_says_word) * (anyone_speaks/person_speaks)
            unique_words[word] = uniqueness

        character_unique_words[person] = unique_words
    return None


# strip out any contextual information
def remove_context(line):
    # information comes in the forms '* *', '( )', and '[ ]'
    line = re.sub(r"\[(.*?)\]", "", line)
    line = re.sub(r"\*(.*?)\*", "", line)
    line = re.sub(r"\((.*?)\)", "", line)
    return line


def count_words(line):
    # catch unexpected lines
    if len(line) == 2:
        name = line[0].strip()
        dialog = line[1].lower()

        # get individual words
        dialog = dialog.split(' ')
        # remove empty strings
        dialog = list(filter(None, dialog))

        # update words corresponding to characters
        if name in characters:
            counts = characters[name]
            counts.update(dialog)
        else:
            counts = Counter()
            counts.update(dialog)
            characters[name] = counts

        all_words.update(dialog)
        num_lines_character.update([name])


def parse_transcripts():
    _reg_dialog = re.compile('(.*):(.*)\n')

    with open(transcript_folder + 'season1/Anatomy_Park.txt', 'r') as file:
        line = next(file)
        while line:
            if _reg_dialog.match(line):
                # strip grammar and new lines from dialog
                line = re.sub(r"\.?,?\??!?\n?", "", line)
                # strip out any informational text
                line = remove_context(line)
                # split character and dialog
                line = line.split(':')
                count_words(line)

            line = next(file, None)


if __name__ == "__main__":
    parse_transcripts()
    # find word uniqueness for each character
    calc_word_uniqueness()
    # output results
    for character in character_unique_words:
        print("Character: {}".format(character))
        words = character_unique_words[character]
        words_sorted = sorted(words, key=words.__getitem__, reverse=True)
        print(words_sorted)
