from dataclasses import dataclass
from typing import List, Tuple, Union, Iterable
from functools import cache, reduce

from iter_utils import grouper


Register = int


@dataclass(frozen=True)
class State:
    w: Register
    x: Register
    y: Register
    z: Register

    def __str__(self) -> str:
        return f"w: {self.w} | x: {self.x} | y: {self.y} | z: {self.z}"


def tuple_as_python(t: Union[Tuple, int, str]) -> str:
    if isinstance(t, (int, str)):
        return str(t)

    operator, a, b = t

    return f"({tuple_as_python(a)}{operator}{tuple_as_python(b)})"


def tuple_as_lisp(t: Union[Tuple, int, str]) -> str:
    if isinstance(t, (int, str)):
        return str(t)

    return f"({' '.join(tuple_as_lisp(e) for e in t)})"


@dataclass(frozen=True)
class Instruction:
    operation: str
    args: List[str]

    def __str__(self) -> str:
        return f"{self.operation} {' '.join(self.args)}"

    @classmethod
    def from_str(cls, string: str) -> "Instruction":
        operation, *args = string.strip().split()
        return cls(operation, args)


@dataclass(frozen=True)
class LispState:
    input_counter: int = 0

    w: Union[Tuple, int, str] = "w"
    x: Union[Tuple, int, str] = "x"
    y: Union[Tuple, int, str] = "y"
    z: Union[Tuple, int, str] = "z"

    def modified_copy(self, **kwargs) -> "LispState":
        state = {
            "w": self.w,
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "input_counter": self.input_counter,
        }
        state.update(kwargs)

        return LispState(**state)

    def parsed_args(self, args) -> Tuple:
        a, b = args
        try:
            b = int(b)
        except ValueError:
            b = getattr(self, b)

        return (a, getattr(self, a), b)

    def do_inp(self, args) -> "LispState":
        (a,) = args
        next_state = {
            a: f"i{self.input_counter}",
            "input_counter": self.input_counter + 1,
        }

        return self.modified_copy(**next_state)

    def do_operation(self, args, sign: str) -> "LispState":
        target, a, b = self.parsed_args(args)
        next_state = {target: (sign, a, b)}

        return self.modified_copy(**next_state)

    def do_add(self, args) -> "LispState":
        target, a, b = self.parsed_args(args)
        if b == 0:
            return self.modified_copy(**{target: a})

        if a == 0:
            return self.modified_copy(**{target: b})

        return self.do_operation(args, sign="+")

    def do_mod(self, args) -> "LispState":
        target, a, b = self.parsed_args(args)
        if a == 0:
            return self.modified_copy(**{target: 0})

        return self.do_operation(args, sign="%")

    def do_mul(self, args) -> "LispState":
        target, a, b = self.parsed_args(args)
        if b == 0 or a == 0:
            return self.modified_copy(**{target: 0})

        if b == 1:
            return self.modified_copy(**{target: a})

        if a == 1:
            return self.modified_copy(**{target: b})

        return self.do_operation(args, sign="*")

    def do_div(self, args) -> "LispState":
        target, a, b = self.parsed_args(args)
        if b == 1:
            return self.modified_copy(**{target: a})

        if isinstance(a, int) and isinstance(b, int) and a < b:
            return self.modified_copy(**{target: 0})

        return self.do_operation(args, sign="//")

    def do_eql(self, args) -> "LispState":
        target, a, b = self.parsed_args(args)
        if a == b:
            return self.modified_copy(**{target: 1})

        if isinstance(a, str) and isinstance(b, int) and not (0 <= b <= 9):
            return self.modified_copy(**{target: 0})

        if isinstance(b, str) and isinstance(a, int) and not (0 <= a <= 9):
            return self.modified_copy(**{target: 0})

        return self.do_operation(args, sign="==")

    def next_state(self, instruction: Instruction) -> "LispState":
        doers = {
            "inp": self.do_inp,
            "add": self.do_add,
            "mod": self.do_mod,
            "mul": self.do_mul,
            "div": self.do_div,
            "eql": self.do_eql,
        }

        return doers[instruction.operation](instruction.args)

    def __str__(self) -> str:
        registers = "wyxz"
        return "\n".join(f"{name}: {(getattr(self, name))}" for name in registers)


CHUNK_CACHE = {}
def chunked_evaluation(program: List, iteration_order: Iterable, position: int = 0, previous_z: int = 0):
    """Foo.

    Since the only dependency between "positions" is the z "variable" it should
    be quite easy to evaluate position for position and create a cache of
    calculations for each position and incoming z-value minimizing the need of
    calculations.

    Another limitation is that the valid licenses should only contain numbers
    1-9.

    These limitiations gives us a theoretical max:
    positions * len(possible z-values) * 9

    Which should be entirely doable to calculate.

    """

    program_end = len(program) - 1

    cache_key = (position, previous_z)
    if cache_key in CHUNK_CACHE:
        #print("cache hit", cache_key)
        return CHUNK_CACHE[cache_key]

    for i in iteration_order:
        # print(" " * position + str(i))
        this_z = program[position](i, previous_z)

        if position < program_end:
            license = chunked_evaluation(
                program=program, position=position + 1, previous_z=this_z,
                iteration_order=iteration_order,
            )

            if license:
                license = str(i) + license
                print(" " * position + license)
                CHUNK_CACHE[cache_key] = license

                return license

        else:
            if this_z == 0:

                return str(i)

    CHUNK_CACHE[cache_key] = None
    return None


def python_from_instructions(strings: List[str]):
    """"""
    program = [Instruction.from_str(line) for line in strings]
    chunked_program = list(map(list, grouper(program, n=18)))
    python_strings = [
        tuple_as_python(reduce(
            lambda state, instruction: state.next_state(instruction),
            chunk,
            LispState(),
        ).z)
        for chunk in chunked_program
    ]
    for ps in python_strings:
        print(ps)

    return python_strings