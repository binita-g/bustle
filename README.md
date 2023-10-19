# BUSTLE
Bottom up program synthesis for COMPSCI252.
Both the files use the same implementation, so it is agnostic for two languages. The only differences are 1) the examples used and 2) the constants used. 

# Implementation
This program works by first defining classes for every possible function (Add, Subtract, etc.) as well as classes for every type of variable and constant.
This allows us to have control over the argument types and return types for each class, which is especially important because many of the functions require specifically typed arguments.

We then instantiate any necessary operations and define our constants.

It is then important to create an L1 program bank, that holds just the example inputs and the constants.

We then use recursion to generate possible programs.

Lastly, we evaluate to check with synthesized programs match the output of the current example.

## Arithmetic
To run, please run python arithmetic.py

## String Manipulation
To run, please run python string.py
