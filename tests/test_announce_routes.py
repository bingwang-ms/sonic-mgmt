import pytest

pytestmark = [
    pytest.mark.topology('t0', 't1')
]

def test_announce_routes(fib):
    """Simple test case that utilize fib to announce route in order to a newly setup test bed receive
       BGP routes from remote devices
    """
    assert True
