
import numpy as np

lines = open("input-2-test.txt").read().splitlines()
lines = open("input-2.txt").read().splitlines()

def report_is_safe(report):
    # Difference between successive elements.
    diff = np.diff(report)

    # Absolute value of those differences.
    delta = np.absolute(diff)

    # Make sure all changes are 1, 2, or 3.
    all_good_range = np.all((delta >= 1) & (delta <= 3))

    # Make sure all changes are in the same direction (the differences of their
    # signs are all zero).
    all_same_sign = np.all(np.diff(np.sign(diff)) == 0)

    return all_good_range and all_same_sign

def with_missing_levels(report):
    return (np.delete(report, i) for i in range(len(report)))

def line_is_safe(line, part):
    report = np.fromstring(line, sep=" ")

    return report_is_safe(report) or \
            (part == 2 and
             any(report_is_safe(report) for report in with_missing_levels(report)))

def do_part(part):
    count = sum(line_is_safe(line, part) for line in lines)
    print(f"Part {part}: {count}")

do_part(1)
do_part(2)

