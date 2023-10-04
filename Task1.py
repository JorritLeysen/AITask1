# Task
# Imports
from simpleai.search import CspProblem, backtrack
import streamlit as st

# Function to parse the cryptarithmetic puzzle input and extract unique characters
def parse_puzzle(puzzle):
    puzzle = puzzle.replace(" ", "").replace("=", "").replace("+", "")  # Remove spaces
    unique_chars = list(set(puzzle))
    return unique_chars

def constraint_unique(variables, values):
    return len(values) == len(set(values))  # remove repeated values and count

# def constraint_add(variables, values):
#     factor = int(str(values[0]) + str(values[1]) + str(values[1]))
#     result = int(str(values[3]) + str(values[2]) + str(values[3]) + str(values[4]))
#     return (factor + factor) == result

# Function to generate the constraints based on the puzzle
def generate_constraints(puzzle):
    unique_chars = parse_puzzle(puzzle)
    variables = unique_chars
    domains = {}

    # Split the puzzle into left-hand and right-hand sides
    left, solution = puzzle.split("=")
    factor1, factor2 = left.split("+")
    factor1 = factor1.strip()
    factor2 = factor2.strip()
    solution = solution.strip()

    words = [factor1, factor2, solution]

    for char in unique_chars:
        if char == factor1[0] or char == factor2[0] or char == solution[0]:
            domains[char] = list(range(1, 10))  # Possible values are 1-9 for each first character
        else:
            domains[char] = list(range(10))  # Possible values are 0-9 for other characters

    def constraint_add(variables, values):
        # Counter for words
        counter = 0

        # Initialize
        factor1 = ""
        factor2 = ""
        solution = ""

        # Loop words
        for word in words:
            for letter in word:
                number = str(values[variables.index(letter)])
                if counter == 0:
                    factor1 += number
                if counter == 1:
                    factor2 += number
                if counter == 2:
                    solution += number
            counter += 1

        return int(factor1) + int(factor2) == int(solution)

    constraints = [
        (unique_chars, constraint_unique), # Constraint for unique characters
        (unique_chars, constraint_add), # Constraint for the equation
    ]

    return variables, domains, constraints


# Function to solve the puzzle and return the solution
def solve_puzzle(puzzle):
    variables, domains, constraints = generate_constraints(puzzle)
    problem = CspProblem(variables, domains, constraints)
    solution = backtrack(problem)
    return solution

# Program
st.title('AI Course: Task 1')
puzzle_input = st.text_input("Enter the cryptarithmetic puzzle (e.g., 'TO + GO = OUT'): ").upper()

if st.button("Solve"):
    if not puzzle_input:
        st.error("Please enter a cryptarithmetic puzzle.")
    else:
        solution = solve_puzzle(puzzle_input)
        if solution is not None:
            st.success("Solution:")
            # Split the puzzle into the equation and solution
            equation, result = puzzle_input.split('=')
            equation = equation.strip()
            result = result.strip()

            # Display the formatted puzzle and solution
            st.text(equation)
            st.text(result)
            st.text('-' * max(len(equation), len(result)))  # Separator line
            st.text(solution)  # Display the solution
            for variable, value in solution.items():
                st.write(f"{variable}: {value}")
        else:
            st.error("No solution found.")
