from dataclasses import dataclass
from typing import List
from typing import Optional

from ._char import Character
from ._repeat import InfiniteRepeat


@dataclass(frozen=True)
class Sequence:
    elements: List

    @property
    def starriness(self):
        return sum(e.starriness for e in self.elements)

    def __len__(self):
        return len(self.elements)

    def example(self) -> str:
        return "".join(e.example() for e in self.elements)

    @property
    def minimum_length(self) -> int:
        accum: int = 0
        for e in self.elements:
            accum += e.minimum_length
        return accum

    def exact_character_class(self) -> Optional[Character]:
        """
        aa*a -> a, abc -> None, [ab][abc] -> None
        """
        first = self.elements[0].exact_character_class()
        if first is None:
            return None
        for c in self.elements[1:]:
            if c != first:
                return None
        return c

    def overall_character_class(self) -> Optional[Character]:
        """
        aa*a -> a, abc -> None, [ab][abc] -> [ab]
        a?b -> b, a+b -> None, [ab]+b* -> b
        """
        c = Character.ANY()
        for e in self.elements:
            c &= e.overall_character_class()
            if not c:
                return None
        return c

    def matching_repeats(self):  # noqa: C901
        """Complicated way to get the possible character classes for a sequence"""
        c = Character.ANY()
        has_mandatory = False
        optionals = []
        starriness = 0
        minimum_length = 0
        for e in self.elements:
            if e.minimum_length:
                c &= e.overall_character_class()
                if not c:
                    return None
                has_mandatory = True
                starriness += e.starriness
                minimum_length += e.minimum_length
            elif e.starriness > 0:
                optionals.append(e)
        possibilities = {c: starriness} if has_mandatory else {}
        for e in optionals:
            if new_c := e.overall_character_class() & c:
                if new_c in possibilities:
                    possibilities[new_c] += e.starriness
                else:
                    possibilities[new_c] = e.starriness

        if len(possibilities) > 1:
            # (a*[ab]*a*[bc]*[bcd]*.+a*)*@ has classes:
            # {.: 1, [a]: 5, [[a-b]]: 2, [[b-c]]: 3, [[b-d]]: 2, [b]: 3}
            # This could blow up!
            poss_chars = list(possibilities.items())
            merged_chars = {}
            while poss_chars:
                c_a, s_a = poss_chars.pop()
                for c_b, s_b in poss_chars:
                    if (merged := c_a & c_b) is not None:
                        if merged == c_a:
                            possibilities[c_a] += s_b
                        elif merged == c_b:
                            possibilities[c_b] += s_a
                        else:
                            if merged not in merged_chars:
                                merged_chars[merged] = set()
                            merged_chars[merged] |= {(c_a, s_a), (c_b, s_b)}
            for merged, set_of_chars in merged_chars.items():
                possibilities[merged] = sum(s for _, s in set_of_chars)

        for cc, s in possibilities.items():
            if s:
                yield InfiniteRepeat(cc, minimum_length, forced_starriness=s)

    def maximal_character_class(self) -> Character:
        """
        Only useful when this Sequence is inside a Repeat
        a*b -> [ab], ab* -> [ab]
        Since forcing backtracking for (bc*)$
        """
        c = None
        for e in self.elements:
            if (mcc := e.maximal_character_class()) is not None:
                c = mcc | c
        return c

    def __repr__(self) -> str:
        return "SEQ{ " + " ".join(str(e) for e in self.elements) + " }"
