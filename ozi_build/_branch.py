from dataclasses import dataclass
from typing import Iterator
from typing import List
from typing import Optional

from ._at import EndOfString
from ._char import Character
from ._repeat import FiniteRepeat
from ._repeat import InfiniteRepeat
from ._sequence import Sequence


@dataclass(frozen=True)
class Branch:
    branches: List
    optional: bool = False

    def get_branches(self) -> Iterator:
        for b in self.branches:
            yield b
        if self.optional:
            yield None

    @property
    def starriness(self) -> int:
        return max(b.starriness for b in self.branches)

    @property
    def minimum_length(self) -> int:
        return 0 if self.optional else min(b.minimum_length for b in self.branches)

    def overall_character_class(self) -> Optional[Character]:
        c = Character.ANY()
        for b in self.branches:
            c &= b.overall_character_class()
            if c is None:
                return None
        return c

    def maximal_character_class(self):
        return None  # Really?

    def example(self) -> str:
        if self.optional:
            return ""
        return self.branches[0].example()

    def __len__(self) -> int:
        return len(self.branches) + int(self.optional)

    def __repr__(self) -> str:
        middle = " | ".join(str(b) for b in self.branches)
        return f"BR( {middle} ){'?' if self.optional else ''}"

    def matching_repeats(self):
        for b in self.branches:
            if b.starriness > 0:
                if isinstance(b, InfiniteRepeat):
                    yield b
                elif isinstance(b, Sequence):
                    yield from b.matching_repeats()


def make_branch(branches: List):
    if len(branches) == 1:
        return branches[0]
    optional = False
    non_empty_branches = [b for b in branches if b and not isinstance(b, EndOfString)]
    if not non_empty_branches:
        return None
    if len(non_empty_branches) < len(branches):
        # (ab|cd|) -> (ab|cd)?
        optional = True
    if all(isinstance(b, Character) for b in non_empty_branches):
        # (a|b) -> [ab], (a|b|) -> [ab]?
        c = None
        for b in non_empty_branches:
            c |= b
        if optional:
            return FiniteRepeat(c, 0, 1)
        else:
            return c

    return Branch(non_empty_branches, optional)
