# bottom up synthesis for flashfill from BUSTLE (2020)
# https://arxiv.org/abs/2007.14381

# A function to perform bottom-up synthesis of a program that satisfies a given set of input-output examples.
# The function takes as input a set of input-output examples, a set of primitive functions, and a set of variables.
# The function returns a program that satisfies the input-output examples, if one exists.
# If no such program exists, the function returns None.

import itertools

# Class for add
class Add:
    def __init__(self):
        self.args_count = 2
        self.return_type = int

    def args(self):
        return [int, int]

    def str(self, x, y) -> int:
         return f"Add({x}, {y})"
    
    def calc(self, x, y) -> int:
        return x+y

# Class for subtract
class Subtract:
    def __init__(self):
        self.args_count = 2
        self.return_type = int

    def args(self):
        return [int, int]

    def str(self, x, y) -> int:
         return f"Subtract({x}, {y})"
    
    def calc(self, x, y) -> int:
        return x-y

# Class for multiply
class Multiply:
    def __init__(self):
        self.args_count = 2
        self.return_type = int

    def args(self):
        return [int, int]

    def str(self, x, y) -> int:
         return f"Multiply({x}, {y})"
    
    def calc(self, x, y) -> int:
        return x*y

# Class for first letter (Left(S, I))
class Left:
    def __init__(self):
        self.args_count = 2
        self.return_type = str

    def str(self, x, y) -> str:
         return f"Left({x}, {y})"

    def args(self):
            return [str, int]
    
    def calc(self, x: str, y: int) -> str:
            return x[:int(y)]

# Class for last letter (Right(S, I))
class Right:
    def __init__(self):
        self.args_count = 2
        self.return_type = str

    def str(self, x, y) -> str:
         return f"Right({x}, {y})"

    def args(self):
            return [str, int]

    def calc(self, x: str, y: int) -> str:
        return x[int(y)*-1:]

# Class for string concatenation (Concatenate,(S, S))
class Concatenate:
    def __init__(self):
        self.args_count = 2
        self.return_type = str

    def str(self, x, y) -> str:
        return f"Concatenate({x}, {y})"
    
    def args(self):
            return [str, str]

    def calc(self, x: str, y: str) -> str:
        return x+y

# Class for variables
class StrVariable:
    def __init__(self):
        self.args_count = 0
        self.return_type = str
    
    def str(self, key) -> str:
         return key
    
    def calc(self, value) -> str:
        return value

# Class for Int Variables
class IntVariable:
    def __init__(self):
        self.args_count = 0
        self.return_type = int

    def str(self, key) -> str:
         return key
    
    def calc(self, value) -> int:
        return value

# Class for Constants
class StrConstant:
    def __init__(self):
        self.args_count = 0
        self.return_type = str
    
    def str(self, key) -> str:
         return key
    
    def calc(self, value) -> str:
        return value

# Class for Constants
class IntConstant:
    def __init__(self):
        self.args_count = 0
        self.return_type = int
    
    def str(self, key) -> str:
         return key
    
    def calc(self, value) -> int:
        return value

operations = [Add(),
              Subtract(),]

# Define the examples
left_examples = [
    ({'x': 'hello'}, 'h'),
    ({'x': 'world'}, 'w'),
]

right_examples = [
    ({'x': 'hello'}, 'o'),
    ({'x': 'world'}, 'd'),
]

concat_examples = [
    ({'x': 'hello', 'y': 'world'}, 'helloworld'),
    ({'x': 'world', 'y': 'domination'}, 'worlddomination'),
]

add_examples = [
    ({'x': 1, 'y': 2}, 3),
    ({'x': 2, 'y': 4}, 6),
]

sub_examples = [
    ({'x': 4, 'y': 2}, 2),
    ({'x': 7, 'y': 6}, 1),
]

mult_examples = [
    ({'x': 4, 'y': 2}, 8),
    ({'x': 7, 'y': 6}, 42),
]

constants = [(IntConstant, [1])]

program_bank = []

# Create level one.
def __init__level__one(examples):
    for tup in examples:

        for key, value in tup[0].items():

            if type(value) == str:
                program_bank.append((StrVariable, [key, value]))
            if type(value) == int:
                program_bank.append((IntVariable, [key, value]))
    
    program_bank.extend(constants)

# Recursive function for program synthesis
def synthesize_program(examples, program_bank, levels):
    __init__level__one(examples)

    for i in range(levels):
        level_program_bank = []

        for operation in operations:
            permutations = list(itertools.permutations(program_bank, operation.args_count))

            for children in permutations:
                all_arg_types_match = True

                for i, child in enumerate(children):
                    if isinstance(child, tuple):
                        
                        instance = child[0]
                        if callable(instance):
                            instance = child[0]()

                        if instance.return_type != operation.args()[i]:
                            all_arg_types_match = False
                    else:
                        if child.return_type != operation.args()[i]:
                            all_arg_types_match = False

                if all_arg_types_match:
                    level_program_bank.append((operation, children))

        program_bank.extend(level_program_bank)

        # Check if any of the synthesized programs match the output of the current example
        for program in level_program_bank:
            op, children = program

            # Extract the values from the examples as inputs
            all_programs = True

            for example in examples:
                result = op.calc(*(example[0].values()))

                if result != example[1]:
                    all_programs = False
                    
            if all_programs:
                return op, children

    # If no program satisfies the current example, return None
    return None

def render_program(program):
    op, children = program

    if op is StrVariable or StrConstant or IntVariable or IntConstant:
        children_strings = []
        for tup in children:
            children_strings += tup[1][0]

        return op.str(*children_strings)
    else:
        return op.str(*(render_program(child) for child in children))

# Arithmetic
# Add
final_program = synthesize_program(add_examples, program_bank, 3)
if (final_program is not None):
    output = render_program(final_program)
    print("output", output)
    print("number of programs", len(final_program))

program_bank = []

# Subtract
final_program = synthesize_program(sub_examples, program_bank, 2)
if (final_program is not None):
    output = render_program(final_program)
    print("output", output)
    print("number of programs", len(final_program))

program_bank = []