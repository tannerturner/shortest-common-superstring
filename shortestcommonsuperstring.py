"""
        Author: Tanner Turner

        Here is my solution for a programming challenge dealing with a variant of the shortest common superstring 
        problem, which is NP-complete. This algorithm would not work well with strings that have repeats in them, 
        e.g. if the original string was a transcript from Larry David that said "Pretty, pretty, pretty, pretty good." 
        As far as the complexity goes, if n is the number of strings in the original set, and m is the length of the 
        longest string in the set, this algorithm is O(mn^2 + n^3). 
"""


def parse_input():
    """
    Reads from STDIN, creates list of strings sorted by length.

    :rtype : list
    """

    strings = raw_input().split(';')
    strings.sort(key=len, reverse=True)

    return strings


def sort_strings(x, y):
    """
    Sorts two strings by length.

    :param x, y: two strings in unclear order
    :rtype : string, string
    """

    temp_list = [x, y]
    temp_list.sort(key=len)

    return temp_list[1], temp_list[0]


def shallow_del(s, str_in_set):
    """
    Removes a string from the dictionary set.

    :param s: string to delete
    :param str_in_set: dictionary storing whether or not a string is in the set
    :rtype : dict
    """

    str_in_set[s] = str_in_set.get(s, 1) - 1
    if str_in_set[s] < 1:
        str_in_set.pop(s, None)
    # end if
    return str_in_set


def find_overlap(s1, s2, max_val_i=0, overlap_string=''):
    """
    Finds an overlap between two strings, if it exists.

    :param s1: longer string
    :param s2: shorter string
    :param max_val_i: max overlap length of s1 and s2
    :param overlap_string: string formed when s1 and s2 lined up on max overlap
    :rtype : int, string
    """

    marker = len(s2) - 1
    for k in xrange(marker, 1, -1):
        if s1[:k] == s2[-k:]:
            max_val_i = k
            overlap_string = s2 + s1[k:]
            break
        # end if
        elif s1[-k:] == s2[:k]:
            max_val_i = k
            overlap_string = s1 + s2[k:]
            break
            # end elif
    # end for
    return max_val_i, overlap_string


def attempt_overlap_search(i, new_old_str_map, s1, str_in_set, strings, val_to_str_map, max_overlap_val, first=False):
    """
    Determines if a valid overlap can be found. If so, also deals with the overlap data accordingly.

    :param i: index of outer loop
    :param new_old_str_map: dictionary storing which "old" strings formed each "new" string
    :param s1: string from outer loop
    :param str_in_set: see shallow_del function
    :param strings: list of strings representing the current set of strings
    :param val_to_str_map: dictionary storing which "new" strings were created with an overlap of the size of the key
    :param max_overlap_val: current max overlap length of all pairs of strings
    :param first: boolean representing whether or not this is the initial call of this function
    :rtype : dict, dict, dict, int
    """

    for j in xrange(i + 1, len(strings)):
        if not first:
            s1 = strings[0]
            if not str_in_set.get(s1, 0):
                break
            # end if
            s1, s2 = sort_strings(strings[0], strings[j])
        # end if
        else:
            s2 = strings[j]
        # end else
        if str_in_set.get(s2, 0):
            if s2 in s1:
                str_in_set = shallow_del(s2, str_in_set)
            # end if
            else:
                max_val_i, overlap_string = find_overlap(s1, s2)

                if max_val_i not in val_to_str_map:
                    val_to_str_map[max_val_i] = []
                # end if

                if max_val_i > 0:
                    val_to_str_map[max_val_i].append(overlap_string)
                    new_old_str_map[overlap_string] = [s1, s2]
                # end if

                if max_val_i > max_overlap_val:
                    max_overlap_val = max_val_i
                # end if
            # end else
        # end if
    # end for
    return new_old_str_map, str_in_set, val_to_str_map, max_overlap_val


def delete_redundant_str(str_in_set):
    """
    Deletes redundant strings from the set.

    :param str_in_set: see shallow_del function
    :rtype : list
    """

    return list(str_in_set.keys())


def merge(new_str_to_add, s1, s2, str_in_set):
    """
    Adds a new, larger string and removes the two strings that formed it.

    :param new_str_to_add: new string to be added to the set
    :param s1, s2: old strings that formed new string
    :param str_in_set: see shallow_del function
    :rtype : dict, list
    """

    str_in_set = shallow_del(s1, str_in_set)
    str_in_set = shallow_del(s2, str_in_set)
    strings = delete_redundant_str(str_in_set)
    str_in_set[new_str_to_add] = str_in_set.get(new_str_to_add, 0) + 1
    strings.insert(0, new_str_to_add)

    return str_in_set, strings


def clear_old_str(new_old_str_map, val_to_str_map, s1, s2):
    """
    Removes relational data concerning strings no longer valid.

    :param new_old_str_map: see attempt_overlap_search function
    :param val_to_str_map: see attempt_overlap_search function
    :param s1, s2: old strings
    :rtype : dict, dict
    """

    str_to_del = []
    for key, val in new_old_str_map.iteritems():
        if s1 in val or s2 in val:
            str_to_del.append(key)
        # end if
    # end for
    for s in str_to_del:
        if s in new_old_str_map:
            new_old_str_map.pop(s, None)
        # end if
        for key, val in val_to_str_map.iteritems():
            if s in val:
                val_to_str_map[key].remove(s)
                if not val_to_str_map[key]:
                    val_to_str_map.pop(key, None)
                    break
                # end if
            # end if
        # end for
    # end for
    return new_old_str_map, val_to_str_map


def get_max_val(val_to_str_map):
    """
    Returns the maximum possible overlap value, if one exists. Otherwise, returns -1.

    :param val_to_str_map: see attempt_overlap_search function
    :rtype : int
    """

    return -1 if len(val_to_str_map) == 0 else max(val_to_str_map.keys())


def find_max_overlap_str(max_overlap_val, new_old_str_map, str_in_set, val_to_str_map, strings, no_merge_success):
    """
    Finds the largest overlap between two valid strings and deals with the new string and old strings accordingly.

    :param max_overlap_val: see attempt_overlap_search function
    :param new_old_str_map: see attempt_overlap_search function
    :param str_in_set: see shallow_del function
    :param val_to_str_map: see attempt_overlap_search function
    :param strings: see attempt_overlap_search function
    :param no_merge_success: boolean representing whether or not we've found two valid strings to merge
    :rtype : int, string, dict, dict, list, boolean
    """

    new_str_to_add = ''
    if val_to_str_map[max_overlap_val]:
        new_str_to_add = val_to_str_map[max_overlap_val].pop(0)
    # end if
    if not val_to_str_map[max_overlap_val]:
        val_to_str_map.pop(max_overlap_val, None)
    # end if
    old_strings = new_old_str_map.get(new_str_to_add, ['', ''])
    s1 = old_strings[0]
    s2 = old_strings[1]
    if str_in_set.get(s1, 0) and str_in_set.get(s2, 0):
        str_in_set, strings = merge(new_str_to_add, s1, s2, str_in_set)
        no_merge_success = False
    # end if
    new_old_str_map, val_to_str_map = clear_old_str(new_old_str_map, val_to_str_map, s1, s2)
    max_overlap_val = get_max_val(val_to_str_map)

    return max_overlap_val, new_str_to_add, str_in_set, val_to_str_map, new_old_str_map, strings, no_merge_success


def main():
    """
    - Initializes data structures.
    - Builds table of all possible overlaps of initial set of strings.
    - Greedily merges pair of strings with largest overlap until one is left.
    - Prints final string formed, which is an approximate shortest common superstring of the initial set of strings.

    :return:
    """

    strings = parse_input()
    str_in_set = {}
    val_to_str_map = {}
    new_old_str_map = {}
    max_overlap_val = 0

    for s in strings:
        str_in_set[s] = str_in_set.get(s, 0) + 1
    # end for

    for i in xrange(0, len(strings) - 1):
        s1 = strings[i]
        new_old_str_map, str_in_set, val_to_str_map, max_overlap_val = \
            attempt_overlap_search(
                i, new_old_str_map, s1, str_in_set,
                strings[:], val_to_str_map, max_overlap_val, True)
    # end for
    strings = delete_redundant_str(str_in_set)
    need_merge = (len(strings) > 1)

    while need_merge:
        no_merge_success = True
        while no_merge_success and max_overlap_val > -1:
            max_overlap_val, new_str_to_add, str_in_set, val_to_str_map, new_old_str_map, strings, no_merge_success = \
                find_max_overlap_str(
                    max_overlap_val, new_old_str_map, str_in_set,
                    val_to_str_map, strings[:], no_merge_success)
        # end while
        if len(strings) == 1:
            break
        # end if
        if str_in_set.get(new_str_to_add, 0):
            s1 = new_str_to_add
            new_old_str_map, str_in_set, val_to_str_map, max_overlap_val = \
                attempt_overlap_search(0, new_old_str_map, s1, str_in_set, strings[:], val_to_str_map, max_overlap_val)
        # end if
        strings = delete_redundant_str(str_in_set)
        need_merge = (len(strings) > 1)
    # end while
    print strings[0]
    return strings[0]


main()