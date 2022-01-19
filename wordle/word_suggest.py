import json
from enum import Enum, auto
from typing import List, Set, Optional, Dict
import string


YES_INPUTS = ["y", "yes", "true", "1"]
GAME_TURNS = 6
WORD_LENGTH = 5


with open("words.json", "r") as f:
    DICTIONARY = json.load(f)


class SuggestionOrdering(Enum):
    REMAINING_OPTIONS = auto()
    ESTIMATED_POINTS = auto()


def ordinal(pos: int) -> str:
    pos_str = str(pos)
    if pos_str.endswith("1") and not pos_str.endswith("11"):
        return f"{pos_str}st"
    if pos_str.endswith("2") and not pos_str.endswith("12"):
        return f"{pos_str}nd"
    if pos_str.endswith("3") and not pos_str.endswith("13"):
        return f"{pos_str}rd"
    return f"{pos_str}th"


class LetterState:
    def __init__(
        self,
        letter: str,
        presence: Optional[bool] = None,
        known_locations: Set[int] = None,
        known_misses: Set[int] = None
    ) -> None:
        super().__init__()
        self.letter = letter
        self.presence = presence
        self.known_locations = known_locations or set()
        self.known_misses = known_misses or set()

    def known_location_state(self, pos: int) -> bool:
        return pos in self.known_locations or pos in self.known_misses

    def matches_word(self, word: str) -> bool:
        # Presence check
        if self.presence is not None and (self.letter in word) != self.presence:
            return False
        # Location checks
        if not all(word[loc] == self.letter for loc in self.known_locations):
            return False
        if any(word[loc] == self.letter for loc in self.known_misses):
            return False
        return True

    def add_known_location(self, pos: int) -> None:
        self.known_locations.add(pos)

    def add_known_miss(self, pos: int) -> None:
        self.known_misses.add(pos)

    def copy(self) -> "LetterState":
        return LetterState(
            self.letter,
            self.presence,
            self.known_locations.copy(),
            self.known_misses.copy()
        )

    def with_presence(self, presence: bool) -> "LetterState":
        other = self.copy()
        other.presence = presence
        return other

    def with_known_location(self, pos: int) -> "LetterState":
        other = self.copy()
        other.add_known_location(pos)
        return other

    def with_known_miss(self, pos: int) -> "LetterState":
        other = self.copy()
        other.add_known_miss(pos)
        return other


class WordleState:
    def __init__(self) -> None:
        self.state = {
            letter: LetterState(letter)
            for letter in string.ascii_lowercase
        }

    def set_presence(self, letter: str, presence: bool) -> None:
        self.state[letter].presence = presence

    def add_known_miss(self, letter: str, not_pos: int) -> None:
        self.state[letter].add_known_miss(not_pos)

    def add_known_location(self, letter: str, pos: int) -> None:
        self.state[letter].add_known_location(pos)

    def build_state(self) -> None:
        next_word = input("What word have you entered? ")
        for pos, letter in enumerate(next_word):
            # Ask about presence
            if self.state[letter].presence is None:
                matched = input(f"Did the {ordinal(pos+1)} letter, \"{letter}\" match at all? [Y/N] ")
                self.set_presence(letter, matched.lower() in YES_INPUTS)
            # Ask about location
            if self.state[letter].presence is True and not self.state[letter].known_location_state(pos):
                correct_loc = input(f"Was the {ordinal(pos+1)} letter, \"{letter}\" in the right location? [Y/N] ")
                if correct_loc.lower() in YES_INPUTS:
                    self.add_known_location(letter, pos)
                else:
                    self.add_known_miss(letter, pos)
        return

    def remaining_words(self) -> List[str]:
        matching = []
        for word in DICTIONARY:
            if all(letter_state.matches_word(word) for letter_state in self.state.values()):
                matching.append(word)
        return matching

    def word_could_give(self, word: str) -> List[Dict[str, LetterState]]:
        states = [self.state.copy()]
        for pos, letter in enumerate(word):
            if self.state[letter].presence is True:
                if pos in self.state[letter].known_locations:
                    continue
                new_states = [
                    {**state, letter: state[letter].with_known_location(pos)}
                    for state in states
                ] + [
                    {**state, letter: state[letter].with_known_miss(pos)}
                    for state in states
                ]
                states = new_states
            else:
                new_states = [
                    {**state, letter: state[letter].with_presence(False)}
                    for state in states
                ] + [
                    {**state, letter: state[letter].with_known_location(pos)}
                    for state in states
                ] + [
                    {**state, letter: state[letter].with_known_miss(pos)}
                    for state in states
                ]
                states = new_states
        return states

    def word_leave_options_via_states(self, word: str, other_words: List[str]) -> List[int]:
        states = self.word_could_give(word)
        options = [
            len(self.matches_state(state, other_words))
            for state in states
        ]
        result = sorted(options, reverse=True)
        print(f"Word: {word} would leave options: {result}")
        return result

    def word_leave_options(self, word: str, other_words: List[str]) -> List[int]:
        remaining_options = [other_words.copy()]
        for pos, letter in enumerate(word):
            if self.state[letter].presence is True:
                if pos in self.state[letter].known_locations:
                    continue
                new_remaining = []
                for remaining_words in remaining_options:
                    new_remaining.append([word for word in remaining_words if word[pos] != letter])
                    new_remaining.append([word for word in remaining_words if word[pos] == letter])
                remaining_options = new_remaining
            else:
                new_remaining = []
                for remaining_words in remaining_options:
                    new_remaining.append([word for word in remaining_words if word[pos] == letter])
                    new_remaining.append([word for word in remaining_words if letter in word and word[pos] != letter])
                    new_remaining.append([word for word in remaining_words if letter not in word])
                remaining_options = new_remaining
        options = [
            len(remaining_option)
            for remaining_option in remaining_options
        ]
        result = sorted(options, reverse=True)
        return result

    def matches_state(self, state: Dict[str, LetterState], words: List[str]) -> List[str]:
        matching = []
        for word in words:
            if all(letter_state.matches_word(word) for letter_state in state.values()):
                matching.append(word)
        return matching

    def word_would_leave(self, word: str, other_words: List[str]) -> int:
        remaining = other_words[:]
        for pos, letter in enumerate(word):
            if self.state[letter].presence is True:
                if pos in self.state[letter].known_locations:
                    continue
                remaining = [w for w in remaining if w[pos] != letter]
            else:
                remaining = [w for w in remaining if letter not in w]
        return len(remaining)

    def expected_clue_points_for_word(self, word: str, remaining_words: List[str]) -> float:
        points = [self.clue_points_if_word(word, remaining) for remaining in remaining_words]
        return sum(points) / len(points)

    def clue_points_if_word(self, guess: str, answer: str) -> int:
        points = 0
        for pos, letter in enumerate(answer):
            if guess[pos] == letter:
                points += 2
            elif letter in guess:
                points += 1
        return points

    def suggest_matching(
            self,
            suggestions: int = -1,
            order_by: Optional[SuggestionOrdering] = SuggestionOrdering.ESTIMATED_POINTS
    ) -> None:
        all_matching = self.remaining_words()
        print(f"There are {len(all_matching)} matching words")
        print(f"Matching words: ")
        if order_by is None:
            for word in all_matching:
                print(word)
        elif order_by == SuggestionOrdering.REMAINING_OPTIONS:
            match_counts = {
                word: self.word_leave_options(word, all_matching)
                for word in all_matching
            }
            all_count = len(all_matching)
            for match, counts in sorted(match_counts.items(), key=lambda pair: pair[1])[:suggestions]:
                print(f"{match}: Could rule out at least {all_count - counts[0]} options")
        else:
            match_points = {
                word: self.expected_clue_points_for_word(word, all_matching)
                for word in all_matching
            }
            for match, exp_points in sorted(match_points.items(), key=lambda pair: pair[1], reverse=True)[:suggestions]:
                print(f"{match}: Could give an average of {exp_points:.02f} points")

    def game_won(self) -> bool:
        return sum(
            len(letter_state.known_locations)
            for letter_state in self.state.values()
        ) == WORD_LENGTH

    def winning_word(self) -> Optional[str]:
        word_letters: List[Optional[str]] = [None] * WORD_LENGTH
        for letter_state in self.state.values():
            for loc in letter_state.known_locations:
                word_letters[loc] = letter_state.letter
        if None in word_letters:
            return None
        return "".join(word_letters)


def play():
    state = WordleState()
    print("For your first word, may I suggest:")
    state.suggest_matching(25)
    turn = 1
    while not state.game_won() and turn < GAME_TURNS:
        state.build_state()
        state.suggest_matching()
        turn += 1
    if state.game_won():
        print("You won, congrats")
        print(f"The word was: {state.winning_word()}")
    else:
        print("You lost.")
        remaining_words = state.remaining_words()
        if len(remaining_words) > 1:
            print(f"There were {len(remaining_words)} remaining words")
        elif len(remaining_words) == 1:
            print(f"There was one word left: {remaining_words[0]}")
        else:
            print("I cannot find a valid solution")


if __name__ == "__main__":
    play()
