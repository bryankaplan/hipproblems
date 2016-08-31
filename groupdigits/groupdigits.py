"""See the attached README file for what needs to be done.
"""


def group_digits(amount, grouping, separator):
    """Formats an amount according to the grouping strategy in groupings. Groups
    are separated with a `separator` character.

    Args:
        amount: Number - The amount to be formatted.

        grouping: List[int] - Each element is the number of digits in a group;
            elements with higher indices are further left. An element with value
            -1 means that no further grouping is done. An element with value 0
            means that the previous element is used for all groups further left.
        separator: string - The string to use as a separator.

    Returns: A string, consisting of the input amount grouped and with
        separators inserted.
    """
    amount = str(amount)

    if not grouping or grouping[0] == -1: # noop
        return amount

    # Although README.md states that input is a list of integers, in
    # fact there are some floats in the test inputs. The expected test
    # results indicate that we want to work only with the floor of the
    # float, while appending the fraction value to the final result.
    if '.' in amount:
        integer, radix_point, fraction = amount.rpartition('.')
        integer = group_digits(integer, grouping, separator)
        return integer + radix_point + fraction

    # Take the trailing chunk of digits (where the length of the chunk
    # is specified in grouping). Then recurse to determine its prefix.

    prefix = None

    if len(grouping) > 1 and grouping[1] == 0:
        if len(amount) < grouping[0]: # Nothing to do
            return amount
        else:
            prefix_grouping = grouping
    else:
        prefix_grouping = grouping[1:]

    if prefix_grouping:
        prefix = group_digits(amount[0:0-grouping[0]],
                              prefix_grouping,
                              separator)

    chunk = amount[0-grouping[0]:]

    return prefix + separator + chunk if prefix else chunk


def run_tests(test_cases):
    """Contains all the basic tests."""
    failures = 0
    for amount, groupings, separator, expected in test_cases:
        try:
            actual = group_digits(amount, groupings, separator)
        except Exception as e:
            print "ERR : expected %20s got %r" % (expected, e)
            failures += 1
        else:
            if expected != actual:
                print "FAIL: expected %20s got %20s" % (expected, actual)
                failures += 1
            else:
                print "OK  : correct  %20s" % actual

    assert not failures, "Unexpected failures were found."

BASIC_TESTS = [
    (0, [3, 0], ",", "0"),
    (100, [3, 0], ",", "100"),
    (1000, [3, 0], ",", "1,000"),
    (1000, [3, 3, 0], ",", "1,000"),
    (1000000, [3, 3, 0], ",", "1,000,000"),
    (1000000, [3, 0], ",", "1,000,000"),
    (1000000, [3, 0], " ", "1 000 000"),
    (1000000, [3, -1], ",", "1000,000"),
    (1000000, [3, 3, -1], ",", "1,000,000"),
    (700000000, [4, 0], " ", "7 0000 0000"),
    (4154041062, [4, 3, 0], "-", "415-404-1062"),
    (4154041062, [4, 3, -1], "-", "415-404-1062"),
    (10, [1, 1, 1, 1, -1], "! ", "1! 0"),
    (2000.3, [3, 0], " ", "2 000.3"),
    (-12842.42, [3, 0], " ", "-12 842.42"),
    (56781234, [1, 0], "", "56781234"),
    (56781234, [-1], ".", "56781234"),
    (19216801, [1, 1, 3, 0], ".", "192.168.0.1"),
    (8316602, [0], "#", "8316602"),
    (8316602, [], "#", "8316602"),
]


if __name__ == "__main__":
    run_tests(BASIC_TESTS)
