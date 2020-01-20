import pytest

from lab_11.tasks.tools.calculator import (
    Calculator,
    CalculatorError,
    EmptyMemory,
    NotNumberArgument,
    WrongOperation,
)
@pytest.fixture()
def calculator(scope='module'):
    return Calculator()


test_parameter_exception = [
    (6, 6, 6, WrongOperation),
    ('*', 2, None, EmptyMemory),
    ('/', 5, 0, CalculatorError),
    ('/', 6, 'abc', NotNumberArgument),
    ('*', 'abcd', 10, NotNumberArgument),
    ('#', 2, 1, WrongOperation),

]

test_parameter_ok = [
    ('+', '-2', '5', 3),
    ('+', '1', '7', 8),
    ('-', '5', '4', 1),
    ('-', '0', '7', -7),
    ('*', '20', '0.25', 5),
    ('*', '0', '0', 0),
    ('/', '2', '5', 0.4),
    ('/', '2', '8', 0.25),

]


@pytest.mark.parametrize("operator, arg1, arg2, expected", test_parameter_ok)
def test_run_ok_parameter(operator, arg1, arg2, expected, calculator):
    counting_result = calculator.run(operator, arg1, arg2)
    assert counting_result == expected


@pytest.mark.parametrize("operator, arg1, arg2, exception", test_parameter_exception)
def test_run_exception_parameter(operator, arg1, arg2, exception, calculator):
    with pytest.raises(exception):
        calculator.run(operator, arg1, arg2)


def test_calculator_memory(calculator: Calculator):
    calculator.run('*', 2, 2)
    assert calculator._short_memory == 4
    calculator.memorize()
    assert calculator.memory == 6
    calculator.clean_memory()
    with pytest.raises(EmptyMemory):
        calculator.memory()
    with pytest.raises(EmptyMemory):
        calculator.in_memory()
    calculator.run('+', 7, 7)
    assert calculator._short_memory == 14