from typing import List, Optional


def match(pattern: List[str], source: List[str]) -> List[str]:
    """Attempts to match the pattern to the source.

    % matches a sequence of zero or more words and _ matches any single word

    Args:
        pattern - a pattern using to % and/or _ to extract words from the source
        source - a phrase represented as a list of words (strings)

    Returns:
        None if the pattern and source do not "match" ELSE A list of matched words
        (words in the source corresponding to _'s or %'s, in the pattern, if any)
    """
    sind = 0  # current index we are looking at in source list
    pind = 0  # current index we are looking at in pattern list
    result: List[str] = []  # to store substitutions we will return if matched

    # keep checking as long as we haven't hit the end of either pattern or source while
    # pind is still a valid index OR sind is still a valid index (valid index means that
    # the index is != to the length of the list)
    def helper(pind: int, sind: int) -> Optional[List[str]]:
        if pind == len(pattern) and sind == len(source):
            return []
        if pind == len(pattern):
            return None

        # 2) if the current thing in the pattern is a %
        if pind < len(pattern) and pattern[pind] == '%':
            if pind == len(pattern) - 1:
                return [' '.join(source[sind:])]
            next_pat = pattern[pind + 1]
            for i in range(sind, len(source) + 1):
                if i < len(source) and (next_pat == '_' or next_pat == source[i]):
                    sub_res = helper(pind + 1, i)
                    if sub_res is not None:
                        matched = ' '.join(source[sind:i])
                        return [matched] + sub_res
                elif i == len(source) and next_pat != '%':
                    return None
            return None

        # 3) if we reached the end of the source but not the pattern
        if sind == len(source):
            return None

        # 4) if the current thing in the pattern is an _
        if pattern[pind] == '_':
            sub_res = helper(pind + 1, sind + 1)
            if sub_res is not None:
                return [source[sind]] + sub_res
            return None

        # 5) if the current thing in the pattern is the same as the current thing in the
        # source
        if pattern[pind] == source[sind]:
            return helper(pind + 1, sind + 1)

        # 6) else : this will happen if none of the other conditions are met it
        # indicates the current thing it pattern doesn't match the current thing in
        # source
        return None

    return helper(0, 0)


if __name__ == "__main__":
    assert match(["x", "y", "z"], ["x", "y", "z"]) == [], "test 1 failed"
    assert match(["x", "z", "z"], ["x", "y", "z"]) == None, "test 2 failed"
    assert match(["x", "y"], ["x", "y", "z"]) == None, "test 3 failed"
    assert match(["x", "y", "z", "z"], ["x", "y", "z"]) == None, "test 4 failed"
    assert match(["x", "_", "z"], ["x", "y", "z"]) == ["y"], "test 5 failed"
    assert match(["x", "_", "_"], ["x", "y", "z"]) == ["y", "z"], "test 6 failed"
    assert match(["%"], ["x", "y", "z"]) == ["x y z"], "test 7 failed"
    assert match(["x", "%", "z"], ["x", "y", "z"]) == ["y"], "test 8 failed"
    assert match(["%", "z"], ["x", "y", "z"]) == ["x y"], "test 9 failed"
    assert match(["x", "%", "y"], ["x", "y", "z"]) == None, "test 10 failed"
    assert match(["x", "%", "y", "z"], ["x", "y", "z"]) == [""], "test 11 failed"
    assert match(["x", "y", "z", "%"], ["x", "y", "z"]) == [""], "test 12 failed"
    assert match(["x", "%", "y"], ["x", "z", "z"]) == None, "test 13 failed"
    assert match(["_", "%"], ["x", "y", "z"]) == ["x", "y z"], "test 14 failed"
    assert match(["_", "_", "_", "%"], ["x", "y", "z"]) == [
        "x",
        "y",
        "z",
        "",
    ], "test 15 failed"
    # this last case is a strange one, but it exposes an issue with the way we've
    # written our match function
    assert match(["x", "%", "z"], ["x", "y", "z", "z", "z"]) == None, "test 16 failed"

    print("All tests passed!")
