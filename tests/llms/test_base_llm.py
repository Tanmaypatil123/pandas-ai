"""Unit tests for the base LLM class"""

import pytest

from pandasai.exceptions import APIKeyNotFoundError
from pandasai.llm import LLM


class TestBaseLLM:
    """Unit tests for the base LLM class"""

    def test_type(self):
        with pytest.raises(APIKeyNotFoundError):
            LLM().type

    def test_is_pandasai_llm(self):
        assert LLM().is_pandasai_llm() is True

    def test_polish_code(self):
        code = "python print('Hello World')"
        assert LLM()._polish_code(code) == "print('Hello World')"
        code = "py print('Hello World')"
        assert LLM()._polish_code(code) == "print('Hello World')"
        code = "`print('Hello World')`"
        assert LLM()._polish_code(code) == "print('Hello World')"
        code = "print('Hello World')"
        assert LLM()._polish_code(code) == "print('Hello World')"

    def test_is_python_code(self):
        code = "python print('Hello World')"
        assert LLM()._is_python_code(code) is False
        code = "py print('Hello World')"
        assert LLM()._is_python_code(code) is False
        code = "`print('Hello World')`"
        assert LLM()._is_python_code(code) is False
        code = "print('Hello World')"
        assert LLM()._is_python_code(code) is True
        code = "1 +"
        assert LLM()._is_python_code(code) is False
        code = "1 + 1"
        assert LLM()._is_python_code(code) is True

    def test_extract_code(self):
        code = """Sure, here is your code:
```python
print('Hello World')
```
"""
        assert LLM()._extract_code(code) == "print('Hello World')"

        code = """Sure, here is your code:

```
print('Hello World')
```
"""
        assert LLM()._extract_code(code) == "print('Hello World')"

        code = """Sure, here is your code:

```py
print('Hello World')
```
"""

        assert LLM()._extract_code(code) == "print('Hello World')"

    def test_extract_answer(self):
        llm = LLM()
        response = "<answer>This is the answer.</answer>"
        expected_answer = "This is the answer."
        assert llm._extract_answer(response) == expected_answer

    def test_extract_answer_with_temp_chart(self):
        llm = LLM()
        response = (
            "<answer>This is the answer. It returns a temp_chart.png. "
            "But it shouldn't.</answer>"
        )
        expected_answer = "This is the answer. But it shouldn't."
        assert llm._extract_answer(response) == expected_answer
