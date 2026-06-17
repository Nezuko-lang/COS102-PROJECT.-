"""
Calculator Business Logic Module

This module contains the core calculation engine of the application.
It is completely decoupled from the User Interface (GUI) layer. This is a 
fundamental software design principle known as the "Separation of Concerns" (SoC).
By separating the logic from the interface, we can test, modify, or even replace 
the user interface (e.g., convert it to a web app or command-line tool) without 
altering the calculation engine.

Key Educational Concepts Taught in This File:
1. Separation of Concerns (SoC) - Decoupling logic from the GUI.
2. Error Handling - Using try-except blocks to gracefully manage errors like division by zero.
3. Code Cleanliness and Validation - Restricting evaluation inputs to secure math expressions.
4. Python Types - Working with strings, floats, integers, lists, and exception handling.
"""

from typing import List, Tuple, Union

class CalculatorEngine:
    """
    The main calculation engine. It maintains the current state of the math
    expression, processes updates, validates input, and evaluates calculations.
    """
    
    def __init__(self) -> None:
        """
        Initializes a new instance of the CalculatorEngine.
        Sets up the empty expression state and an empty calculation history list.
        """
        # Holds the current active expression as a string (e.g., "12+4.5*3")
        self.expression: str = ""
        
        # Holds the history of calculations as a list of tuples: (expression, result)
        self.history: List[Tuple[str, str]] = []

    def get_expression(self) -> str:
        """
        Returns the current expression state.
        
        Returns:
            str: The active mathematical expression.
        """
        return self.expression

    def clear(self) -> None:
        """
        Resets the expression to an empty string.
        This is triggered when the user clicks the 'C' (Clear) button.
        """
        self.expression = ""

    def backspace(self) -> None:
        """
        Removes the last character from the current expression.
        This is triggered when the user clicks the 'DEL' (Delete/Backspace) button.
        """
        # If the expression is not empty, remove its last character using Python slicing
        if self.expression:
            self.expression = self.expression[:-1]

    def append_character(self, char: str) -> None:
        """
        Appends a character (number, operator, or decimal point) to the current expression,
        applying basic validation rules to prevent obviously invalid expressions.

        Args:
            char (str): The character to append. Expected values: "0"-"9", "+", "-", "*", "/", "."
        """
        # Define lists of valid inputs for easy validation
        operators = {"+", "-", "*", "/"}
        
        # 1. Prevent entering consecutive operators (e.g., "++" or "+*")
        if char in operators and self.expression:
            last_char = self.expression[-1]
            if last_char in operators:
                # Replace the last operator with the new operator to allow the user
                # to correct their mistake (e.g. changing 5 + to 5 *)
                self.expression = self.expression[:-1] + char
                return

        # 2. Prevent starting an expression with * or /
        if char in {"*", "/"} and not self.expression:
            # A math expression usually shouldn't start with multiplication or division
            return

        # 3. Prevent multiple decimals in a single number (e.g., "5.5.5")
        if char == ".":
            # If the expression is empty, allow starting with "." (e.g., ".5" which evaluates to 0.5)
            if not self.expression:
                self.expression += "0."
                return
            
            # Walk backwards from the end of the expression to find if the current
            # number already contains a decimal point.
            # A number is terminated by an operator or the start of the expression.
            has_decimal = False
            for c in reversed(self.expression):
                if c in operators:
                    break
                if c == ".":
                    has_decimal = True
                    break
            
            if has_decimal:
                # If the current number already has a decimal, ignore this input
                return
            
            # If the last character was an operator, pre-pend a '0' for clean formatting (e.g., "+.5" -> "+0.5")
            if self.expression[-1] in operators:
                self.expression += "0."
                return

        # If all validation checks pass, append the character to our expression string
        self.expression += char

    def evaluate(self) -> str:
        """
        Evaluates the current mathematical expression, updates calculation history,
        and returns the result or an error message.

        This method performs input validation for safety before running evaluation.

        Returns:
            str: The evaluated result as a clean string, or "Error" if an exception occurred.
        """
        if not self.expression:
            return ""

        # Remove any trailing operator before evaluating (e.g., "12+4*" becomes "12+4")
        operators = {"+", "-", "*", "/"}
        eval_expr = self.expression
        while eval_expr and eval_expr[-1] in operators:
            eval_expr = eval_expr[:-1]

        if not eval_expr:
            return "Error"

        try:
            # --- SECURITY & SAFETY CHECK ---
            # Python's built-in `eval` evaluates any string as Python code, which can be dangerous
            # if the string comes from an untrusted source.
            # To make it perfectly safe, we strictly validate that the expression only contains
            # digits, basic math symbols, and decimal points.
            allowed_characters = set("0123456789+-*/. ")
            if not all(char in allowed_characters for char in eval_expr):
                raise ValueError("Security violation: Invalid character in math expression.")

            # Evaluate the expression in a restricted global environment with NO standard builtins.
            # This completely blocks access to functions like open(), import, __import__, etc.
            # Format of eval: eval(expression, globals, locals)
            result_num = eval(eval_expr, {"__builtins__": None}, {})

            # Convert result to string and format float numbers nicely
            # (e.g., "5.0" becomes "5", "5.333333333333333" is kept as is)
            if isinstance(result_num, float):
                # If the float represents a whole number, cast it to an integer for a cleaner UI
                if result_num.is_integer():
                    result_str = str(int(result_num))
                else:
                    # Round long decimal numbers to 8 decimal places for display neatness
                    result_str = str(round(result_num, 8))
            else:
                result_str = str(result_num)

            # Add this successful calculation to the history panel
            self.history.append((self.expression, result_str))
            
            # Update current expression state to be the result, so the user can
            # continue calculating using the previous result
            self.expression = result_str
            return result_str

        except ZeroDivisionError:
            # Handle division by zero explicitly (e.g., 5 / 0)
            self.expression = "" # Reset current expression state
            return "Error"
        except (SyntaxError, ValueError, TypeError):
            # Handle malformed expressions (e.g., double operators that slipped past validation)
            # or any other evaluation issues
            self.expression = "" # Reset current expression state
            return "Error"
        except Exception:
            # Catch-all block to prevent the entire GUI application from crashing
            self.expression = ""
            return "Error"

    def get_history(self) -> List[Tuple[str, str]]:
        """
        Returns the list of all past calculations.

        Returns:
            List[Tuple[str, str]]: A list of tuples containing (expression, result).
        """
        return self.history

    def clear_history(self) -> None:
        """
        Clears the calculation history.
        """
        self.history.clear()
