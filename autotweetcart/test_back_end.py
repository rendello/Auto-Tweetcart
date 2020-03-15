#!/usr/bin/python3.7

from hypothesis import given, example
from hypothesis.strategies import text

# Local imports
import back_end


@given(s=text())
def test_grab_title(s):
    if not ("--" in s or "//" in s):
        new_s = back_end.grab_title(s)
        assert new_s == s or new_s is None


@given(s=text())
@example(s="printh")
@example(s="reload")
@example(s="cstore")
def test_intercept_restricted_tokens(s):
    new_s = back_end.intercept_restricted_tokens(s)
    if any(bad_token in s for bad_token in ["cstore", "reload", "printh"]):
        assert s != new_s
    else:
        assert s == new_s


if __name__ == "__main__":
    test_grab_title()
    test_intercept_restricted_tokens()
