import pytest
import task_3

@pytest.mark.parametrize("test_input, expected", [
    ('http://wikipedia.org', True), 
    ('https://ru.wikipedia.org/',True),
    ('griddynamics.com', False)
])
def test_is_http_domain(test_input, expected):
    assert task_3.is_http_domain(test_input) == expected