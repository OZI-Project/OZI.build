import sre_constants
import sre_parse
from typing import List, Optional, Set, Tuple, Union  # noqa: I100, I201

from ._at import EndOfString
from ._branch import Branch, make_branch
from ._categories import Category, covers_any
from ._char import Character
from ._groupref import subpattern_to_groupref
from ._repeat import FiniteRepeat, InfiniteRepeat
from ._sequence import Sequence

SreConstant = sre_constants._NamedIntConstant
SreOpData = Union[Tuple, List, int, SreConstant, None]
SreOp = Tuple[SreConstant, SreOpData]


class SreOpParser:
    def __init__(self):
        self._groups = {}
        self.negative_lookahead: Optional[Character] = None

    def parse_sre(self, pattern: str, flags: int = 0):
        return self.sequence_or_singleton(sre_parse.parse(pattern, flags))

    def parse_op(self, op: SreConstant, data: SreOpData):
        return getattr(self, f"from_{op.name}")(data)

    def sequence_or_singleton(self, ops: List[SreOp]):
        elems = []
        for p in (self.parse_op(*op) for op in ops):
            if p is not None:
                if isinstance(p, Sequence):
                    elems.extend(p.elements)
                else:
                    elems.append(p)
        if len(elems) == 0:
            return None
        if len(elems) == 1:
            return elems[0]
        return Sequence(elems)

    def from_SUBPATTERN(self, data: Tuple[int, int, int, List[SreOp]]):
        ref = data[0]
        elements = data[3]
        result = self.sequence_or_singleton(elements)
        self._groups[ref] = result
        return result

    def from_MAX_REPEAT(
        self,
        data: Tuple[
            int,
            Union[int, SreConstant],
            List[SreOp],
        ],
    ) -> Union[FiniteRepeat, InfiniteRepeat, Branch, None]:
        minimum, maximum, elements = data
        infinite = maximum is sre_constants.MAXREPEAT
        # TODO support negative lookahead before repeat with minimum = 0
        negative_lookahead = self.use_negative_lookahead()
        repeatable = self.sequence_or_singleton(elements)
        if repeatable is None:
            return None
        if (
            minimum == 0
            and maximum == 1
            and repeatable.starriness
            and not repeatable.overall_character_class()
        ):
            # Interesting (starry) optional sequences as branches (ab*)? -> (ab*|)
            return make_branch([repeatable, None])
        if infinite:
            if (
                negative_lookahead is not None
                and minimum > 0
                and isinstance(repeatable, Character)
            ):
                return Sequence(
                    [
                        negative_lookahead & repeatable,
                        InfiniteRepeat(repeatable, minimum - 1),
                    ]
                )
            return InfiniteRepeat(repeatable, minimum)
        if (
            negative_lookahead is not None
            and minimum > 0
            and maximum > 1
            and isinstance(repeatable, Character)
        ):
            return Sequence(
                [
                    negative_lookahead & repeatable,
                    FiniteRepeat(repeatable, minimum - 1, maximum - 1),
                ]
            )
        return FiniteRepeat(repeatable, minimum, maximum)

    def from_MIN_REPEAT(self, data):
        return self.from_MAX_REPEAT(data)

    def from_BRANCH(
        self, data: Tuple[None, List[List[SreOp]]]
    ) -> Union[Branch, FiniteRepeat, Character, None]:
        # sre already transforms (a|b|c) -> [abc]
        branches = data[1]
        negative_lookahead = self.use_negative_lookahead()
        processed_branches = []
        for branch in branches:
            self.negative_lookahead = negative_lookahead
            processed_branches.append(self.sequence_or_singleton(branch))
        self.negative_lookahead = None
        return make_branch(processed_branches)

    def from_AT(self, at: SreConstant):
        # TODO: handling for multiline
        # TODO: handling for \\b
        self.use_negative_lookahead()
        if at is sre_constants.AT_END:
            return EndOfString()
        return None

    def from_ANY(self, _: None) -> Character:
        if negative_lookahead := self.use_negative_lookahead():
            return negative_lookahead
        return Character.ANY()

    def from_LITERAL(self, literal: int) -> Character:
        if negative_lookahead := self.use_negative_lookahead():
            return Character.LITERAL(literal) & negative_lookahead
        return Character.LITERAL(literal)

    def from_NOT_LITERAL(self, not_literal: int) -> Character:
        if negative_lookahead := self.use_negative_lookahead():
            return (
                Character(literals={not_literal}, positive=False) & negative_lookahead
            )
        return Character(literals={not_literal}, positive=False)

    def from_IN(self, data: List[SreOp]) -> Character:
        literals: Optional[Set[int]] = None
        categories: Optional[Set] = None
        positive = True
        if len(data) > 1 and data[0] == (sre_constants.NEGATE, None):
            positive = False
            data = data[1:]
        for in_op, in_data in data:
            if in_op is sre_constants.LITERAL:
                if literals is None:
                    literals = set()
                literals.add(in_data)
            elif in_op is sre_constants.RANGE:
                if literals is None:
                    literals = set()
                min_val, max_val = in_data
                literals.update(range(min_val, max_val + 1))
            elif in_op is sre_constants.CATEGORY:
                if categories is None:
                    categories = set()
                categories.add(Category[in_data.name[9:]])

        if categories and covers_any(categories):
            return self.from_ANY(None) if positive else None
        if negative_lookahead := self.use_negative_lookahead():
            return Character(literals, categories, positive) & negative_lookahead
        return Character(literals, categories, positive)

    def from_GROUPREF(self, ref: int):
        return subpattern_to_groupref(self._groups.get(ref))

    @staticmethod
    def from_GROUPREF_EXISTS(_) -> None:
        return None  # No intention to implement this properly

    @staticmethod
    def from_ASSERT(_) -> None:
        return None  # No intention to implement this properly

    def from_ASSERT_NOT(self, data) -> None:
        typ, ops = data
        if typ == 1:
            if len(ops) == 1:
                character_op = ops[0]
                if character_op[0] in (
                    sre_constants.LITERAL,
                    sre_constants.NOT_LITERAL,
                    sre_constants.IN,
                ):
                    negative_lookahead = self.use_negative_lookahead()
                    not_assertion = self.parse_op(*character_op)
                    if not_assertion and (assertion := not_assertion.negate()):
                        self.negative_lookahead = assertion
                        if negative_lookahead is not None:
                            self.negative_lookahead &= negative_lookahead
                    else:
                        self.negative_lookahead = negative_lookahead

        return None  # No intention to implement this fully

    def use_negative_lookahead(self) -> Optional[Character]:
        if self.negative_lookahead is not None:
            negative_lookahead = self.negative_lookahead
            self.negative_lookahead = None
            return negative_lookahead