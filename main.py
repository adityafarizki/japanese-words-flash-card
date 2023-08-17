import argparse
import random
import sys
from termcolor import colored
from typing import List


class Word:
    def __init__(self, japanese: str, romaji: str, english: str):
        self.japanese = japanese
        self.romaji = romaji
        self.english = english

    def __str__(self) -> str:
        return f"{self.japanese}, {self.romaji}, {self.english}"


def main(args: argparse.Namespace):
    level = args.level
    level_word_list: List[Word] = load_level_word_list(level)
    random.shuffle(level_word_list)

    correct = 0
    wrong = 0
    original_len = len(level_word_list)
    all_english = [word.english for word in level_word_list]
    while level_word_list:
        print(f"remaining {original_len - correct}/{original_len}")
        choices = show_word_quizz(level_word_list, all_english, 0)
        answer = get_answer(choices)
        if answer == level_word_list[0].english:
            correct += 1
            show_correct(level_word_list[0])
            level_word_list = level_word_list[1:]
        else:
            wrong += 1
            show_wrong(level_word_list[0])

        random.shuffle(level_word_list)
        delete_previous_quizz()

    print(f"results:")
    print(f"  attempts: {correct + wrong}")
    print(f"  correct: {correct}")
    print(f"  wrong: {wrong}")
    print(f"  correct percentage: {(correct/(correct + wrong)) * 100}%")


def load_level_word_list(level: int) -> List[Word]:
    raw_word_list: List[str] = []
    with open("data.csv") as f:
        raw = f.read()
        raw_word_list = raw.split("\n")

    word_list: List[Word] = []
    for word in raw_word_list:
        word = word.split(",")
        word_list.append(Word(word[0], word[1], ",".join(word[2:])))

    return word_list[(level - 1) * 50 : (level) * 50]


def show_word_quizz(
    word_list: List[Word], possible_choices: List[str], idx: int
) -> List[str]:
    japanese = word_list[idx].japanese
    choices = [word_list[idx].english]
    for _ in range(8):
        random_idx = random.randint(0, len(possible_choices) - 1)
        trial = 0
        while possible_choices[random_idx] in choices and trial < 100:
            random_idx = random.randint(0, len(possible_choices) - 1)
            trial += 1
        choices.append(possible_choices[random_idx])

    random.shuffle(choices)

    print(f"Translate: {japanese}")
    for i in range(len(choices)):
        print(f"{i + 1}. {choices[i]}")

    return choices


def show_correct(answer: str):
    print(colored(f"Correct! {answer}", "green"))
    input(colored("Press enter to continue", "green"))
    sys.stdout.write("\033[F" + " " * 100)  # Cursor up one line
    sys.stdout.write("\033[F" + " " * 100)  # Cursor up one line


def show_wrong(answer: str):
    print(colored(f"Incorrect! {answer}, try again!", "red"))
    input(colored("Press enter to continue", "red"))
    sys.stdout.write("\033[F" + " " * 100)  # Cursor up one line
    sys.stdout.write("\033[F" + " " * 100)  # Cursor up one line


def delete_previous_quizz():
    for _ in range(12):
        sys.stdout.write("\033[F" + " " * 100)  # Cursor up one line
    print("", end="\r")


def get_answer(choices: List[str]) -> str:
    choice = input("answer: ")
    while choice not in [str(int(i) + 1) for i in range(9)]:
        sys.stdout.write("\033[F")  # Cursor up one line
        print(" " * 100)
        sys.stdout.write("\033[F")  # Cursor up one line
        choice = input("invalid answer, try again: ")

    return choices[int(choice) - 1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--level", type=int, default=1)
    args = parser.parse_args()
    main(args)
