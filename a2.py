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
    sind = 0  
    pind = 0  
    result: List[str] = []

    while pind < len(pattern) or sind < len(source):


        if pind == len(pattern) and sind < len(source):
            return None
        elif pattern[pind] == "%":
            if pind == len(pattern) - 1:
                combined = " ".join(source[sind:])
                result.append(combined)
                return result
            else:
                pind += 1
                accum = ""
                while pattern[pind] != source[sind]:
                    accum += source[sind] + " "
                    sind += 1

                    if sind == len(source):
                        return None
                
                result.append(accum.strip())

        elif sind == len(source):
            return None
        elif pattern[pind] == "_":
            result.append(source[sind])
            pind += 1
            sind += 1
        elif pattern[pind] == source[sind]:
            pind += 1
            sind += 1
        else:

            return None


    return result


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
    assert match(["x", "%", "z"], ["x", "y", "z", "z", "z"]) == None, "test 16 failed"

    print("All tests passed!")
