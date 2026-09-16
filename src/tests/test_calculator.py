"""
Calculator app tests
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from calculator import Calculator

my_calculator = Calculator()

def test_app():
    welcome_message = my_calculator.get_hello_message()
    assert "== Calculatrice v1.0 ==" in welcome_message


def test_addition():
    assert my_calculator.addition(10, 2) == 12


def test_soustraction():
    assert my_calculator.subtraction(10, 2) == 8


def test_multiplication():
    assert my_calculator.multiplication(10, 2) == 20


def test_division():
    assert my_calculator.division(10, 2) == 5


def test_division_par_0():
    assert my_calculator.division(10, 0) == "Erreur : division par zéro"