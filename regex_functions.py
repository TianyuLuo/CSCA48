"""
Tianyu Luo
# Copyright Nick Cheng, Brian Harrington, Danny Heap, 2013, 2014, 2015, 2016
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2016
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from regextree import RegexTree, StarTree, DotTree, BarTree, Leaf

# Do not change anything above this comment except for the copyright
# statement

# Student code below this comment.

base_regex = ['0', '1', '2', 'e']
star = '*'
non_star_oprs = ['|', '.']


def find_left_parenthesis(s):
    ''' (str) -> int or None
    Return the index of the first left bracket. If the left bracket DNE, return
    None
    >>> find_left_parenthesis('))).((')
    4
    >>> find_left_parenthesis('(((')
    None
    '''
    i = 0
    found = False
    while i < len(s) and not found:
        if s[i] == '(':
            return i
        i += 1
    return None


def find_right_parenthesis(s):
    ''' (str) -> int or None
    Return the index of the first right bracket. If the left bracket DNE,
    return None
    >>> find_right_parenthesis('()')
    1
    >>> find_right_parenthesis('((')
    None
    '''
    i = 0
    found = False
    while i < len(s) and not found:
        if s[i] == ')':
            return i
        i += 1
    return None


def seperate_parenthesis(s):
    ''' (str) -> [str, str]
    Return a list of strings which are the regexes seperated by operations,
    the operations between regexes and the operations at the end of the
    seperated string.
    REQ: the s must contain at least one pair of parenthesis.
    >>> seperate_parenthesis('(2|0)**.(0*.(1|0))****')
    ['(2|0)', '**.', '(0*.(1|0))', '****']
    '''
    # find the left bracket of the second regex
    first_right_index = find_right_parenthesis(s)
    if first_right_index is None:
        return None
    left_after_right_index = find_left_parenthesis(s[first_right_index:])
    if left_after_right_index is None:
        return None
    second_regex_left_index = first_right_index + left_after_right_index
    # find the right bracket of the second regex, then find the second regex
    index = 0
    found_index = False
    while index < len(s) and not found_index:
        if s[-index - 1] == ')':
            last_right_index = -index - 1
            found_index = True
        index += 1
    # if there are no stars at the end of the string
    if last_right_index == -1:
        last_oprs = []
        second_regex = s[second_regex_left_index:]
    # if there are stars at the end of the string
    else:
        last_oprs = s[last_right_index + 1:]
        second_regex = s[second_regex_left_index:last_right_index + 1]
    # find the right bracket of the first regex
    j = 0
    found_1 = False
    while (j < len(s[left_after_right_index:second_regex_left_index]) and
           not found_1):
        if s[left_after_right_index:second_regex_left_index][-j - 1] == ')':
            first_regex_right_index = -j - 1
            found_1 = True
        j += 1
    # find the first regex
    first_regex = s[:second_regex_left_index + first_regex_right_index + 1]
    # return the first regex, the operations between two regex and the
    # second regex
    return [first_regex,
            s[second_regex_left_index + first_regex_right_index + 1:
              second_regex_left_index], second_regex, last_oprs]


def is_regex(s):
    ''' (str) -> bool
    Return True if it is a valid regular expression.
    >>> is_regex('((1.(0|1)*).(2.(1|0)))')
    True
    >>> is_regex('1|*')
    False
    '''
    if s in base_regex:
        return True
    count_right = 0
    count_left = 0
    for i in range(len(s)):
        if s[i] == '(':
            count_left += 1
        elif s[i] == ')':
            count_right += 1
    # if the the number of left bracket is not equal to the number of the
    # right bracket,
    if count_left != count_right:
        # return False
        return False
    if s[0] == '(' and s[-1] == ')':
        # if the string next to '(' is other than base regex and '(',
        if s[1] not in base_regex and s[1] != '(':
            # return False
            return False
        # if the string before last ')' is other than base regex and ')',
        if s[-2] not in base_regex and s[-2] != ')' and s[-2] != star:
            return False
        for i in range(1, len(s) - 1):
            # the form of (base_regex + star) is False
            if i < len(s) - 2:
                if (s[i] in base_regex and s[i-1] == '(' and
                    s[i + 1] == '*' and s[i + 2] == ')'):
                    return False
            # the base_regex must followed by star or operation or ')'.
            if (s[i] in base_regex and s[i+1] != star and
                s[i + 1] not in non_star_oprs and s[i + 1] != ')'):
                return False
            # the non-star operations must followed by base_regex or '('
            elif (s[i] in non_star_oprs and
                s[i + 1] not in base_regex and s[i + 1] != '('):
                return False
            # the star must followed by ')' or non-star operations
            elif (s[i] == star and s[i + 1] != star and
                  s[i + 1] not in non_star_oprs and s[i + 1] != ')'):
                return False
            elif s[i] == star and s[i + 1] in base_regex:
                return False
            # the '(' must followed by base_regex and or another '('
            elif s[i] == '(' and s[i + 1] != '(' and s[i + 1] not in base_regex:
                return False
            elif s[i] == '(' and s[i + 1] == ')':
                return False
            # ')' must followed by operations or another ')'
            elif (s[i] == ')' and s[i + 1] != ')' and
                  s[i + 1] not in base_regex and s[i + 1] != star and
                  s[i + 1] not in non_star_oprs):
                return False
            # the form of '(base_regex)' is not correct
            elif s[i] in base_regex and s[i - 1] == '(' and s[i + 1] == ')':
                return False
            # the form of (regex operation base_regex operation) is False
            elif (s[i - 1] in non_star_oprs and
                  s[i + 1] != star and s[i + 1] != ')' and s[i] in base_regex):
                return False
            # the form of (base_regex operation base_regex + star base_regex)
            # is False
            if (i < len(s) - 5 and s[i - 1] in non_star_oprs and
                s[i + 1] == '*' and s[i + 2] in non_star_oprs):
                return False
            # the form of (regex) operation (regex) is False
        return True
    elif s[0] == '(' and s[-1] == '*':
        return is_regex(s[:-1])
    elif s[0] in base_regex and s[-1] == '*':
        return is_regex(s[:-1])
    else:
        return False


def all_perms(s):
    ''' (str) -> set of strs
    Return all the permutations of s
    >>> all_perms('(|1')
    {(|1, (1|, 1(|, 1|(, |1(, |(1}
    '''
    # the code is from my ex7.
    # base case
    if len(s) == 0:
        return {s}
    else:
        res = all_perms(s[1:])
        result = set()
        for item in res:
            for p in range(len(item) + 1):
                result.add(item[:p] + s[0] + item[p:])
        return result


def all_regex_permutations(s):
    ''' (str) -> set of str
    Return a set of strings which are the valid permutation of s
    >>> all_regex_permutations('()|1')
    set()
    >>> all_regex_permutations('.1()e')
    {(1.e), (e.1)}
    '''
    new_s = set()
    all_p = all_perms(s)
    for item in all_p:
        if is_regex(item):
            new_s.add(item)
    return new_s


def regex_match(r, s):
    ''' (subclass of RegexTree or RegexTree, str) -> bool
    Return True iff the s matches the RegexTree, otherwise, return False.
    >>> br1 = RegexTree('0', [])
    >>> br2 = RegexTree('1', [])
    >>> br3 = RegexTree('2', [])
    >>> br4 = RegexTree('e', [])
    >>> dt = DotTree(br1, br2)
    >>> bt = BarTree(dt, br2)
    >>> dt2 = DotTree(br1, br2)
    >>> st = StarTree(dt)
    >>> regex_match(st, '1111')
    True
    >>> regex_match(st, '0101')
    True
    >>> regex_match(st, '1010')
    False
    '''
    # if r is in the base regex which has length 1.
    if r.get_symbol() in base_regex:
        if s == r.get_symbol():
            return True
        elif s == '' and r.get_symbol() == 'e':
            return True
        return False
    # if r is a bar.
    elif r.get_symbol() == '|':
        # if the right child is a Leaf
        if r.get_right_child().get_symbol() in base_regex:
            # if s matches the right subtree
            if s == r.get_right_child().get_symbol():
                return True
            elif s == '' and r.get_right_child().get_symbol() == 'e':
                return True
        # if the left child is a Leaf
        if r.get_left_child().get_symbol() in base_regex:
            # if s matches the left subtree, then s match the tree
            if s == r.get_left_child().get_symbol():
                return True
            elif s == '' and r.get_left_child().get_symbol() == 'e':
                return True
            # if s does not match the left and right subtree
            return False
        # if Neither left child nor right child is Leaf
        else:
            # if s matches the left subtree,
            if regex_match(r.get_left_child(), s):
                # then s match the tree.
                return True
            # if s matches the right subtree,
            if regex_match(r.get_right_child(), s):
                # then s matches the tree
                return True
            # if s does not match right subtree and left subtree, return False.
            return False
    # if r is a star and the child is leaf.
    elif r.get_symbol() == '*':
        # if the child is in base regex,
        if r.get_child().get_symbol() in base_regex:
            if s == '' and r.get_child().get_symbol() == 'e':
                return True
            # if one of the character in the string does not equal to the
            # base_regex,
            for i in range(len(s)):
                if s[i] != r.get_child().get_symbol():
                    # return False
                    return False
            # if every character in the string is the same as the base_regex,
            # return True.
            return True
        # if the child of the star is a tree that rooted at a bar,
        elif r.get_child().get_symbol() == '|':
            # check if the recursive part of string match the bar's rule
            for i in range(1, len(s)):
                # if the first cycle of the string match the bar's rule
                if not regex_match(r.get_child, s[:i]):
                    cyc1 = i
                    # check if the string is recursive.
                    for c1 in range(0, len(s), cyc):
                        # if the string is non-recursive,
                        if s[:cyc1] != s[c1:c1 + cyc1]:
                            # return False
                            return False
                    # if the string is recursive, return True
                    return True
            # if the whole string match the bar's rule, return True
            return True
        # if the child of the star is a tree that rooted at a dot
        elif r.get_child().get_symbol() == '.':
            # check if the non-recursive part of the string match the dot's rule
            for i2 in range(1, len(s)):
                # find the index i2 such that s[:i2] matches the the
                # string.
                if regex_match(r.get_child(), s[:i2]):
                    # find the j such that s[j:] does not match
                    # the string
                    for j in range(1, len(s[i2:])):
                        # find the index such that after the s[:index]
                        # does not match the string
                        if not regex_match(r.get_child(), s[:i2 + j]):
                            cyc2 = i2 + j - 1
                            for c2 in range(0, len(s), cyc2):
                                if s[:cyc2] != s[c2:c2 + cyc2]:
                                    return False
                            return True
                    return True
            return False
        return False
    # if r is a dot.
    elif r.get_symbol() == '.':
        # if the left child and right child are e
        if (r.get_left_child().get_symbol() == 'e' and
            r.get_right_child().get_symbol() == 'e'):
            # if s is an empty string, return True
            if s == '':
                return True
            # if s is not equal to empty string, return False
            return False
        # if the left child are e, then s match the right child
        elif (r.get_left_child().get_symbol() == 'e' and
              r.get_right_child().get_symbol() == s):
            return True
        # if the right child are e, then the s match the left child
        elif (r.get_right_child().get_symbol() == 'e' and
              r.get_left_child().get_symbol() == s):
            return True
        # if the string has length 2 and each character match the corresponding
        # child.
        elif (len(s) == 2 and r.get_left_child().get_symbol() == s[0] and
              r.get_right_child().get_symbol() == s[1]):
            return True
        # if the left child is leaf and the right child is not a leaf
        elif r.get_left_child().get_symbol() == s[0]:
            if (len(s) == 1):
                return False
            for i in range(2, len(s) + 1):
                if not regex_match(r.get_right_child(), s[1:i]):
                    return False
            return True
        # if the right child is the leaf and the left child is not a leaf
        elif r.get_right_child().get_symbol() == s[-1]:
            if (len(s) == 1):
                return False
            for i in range(1, len(s) - 1):
                # if the the first part of string does not match the string
                # then s does not match the string
                if not regex_match(r.get_left_child(), s[:i]):
                    return False
            return True
        # neither of the children is the leaf
        else:
            for i in range(1, len(s)):
                # check if the tree rooted at left child matches the former part
                # of the string.
                if not regex_match(r.get_left_child(), s[:i]):
                    # if the tree rooted at left child does not match the former
                    # part of the string,
                    if i == 1:
                        # return False
                        return False
                    # if right child does not match the latter part of the
                    # string,
                    elif not regex_match(r.get_right_child(), s[i-1:]):
                        # return False
                        return False
                    # if the tree rooted at left child matches the former
                    # part of the string and the tree rooted at right child
                    # matches the latter part of the string, return True.
                    return True
                # if the tree rooted at left child matches all the string,
                # return False
                return False
    else:
        return False


def build_regex_tree(valid_r):
    ''' (str) -> RegexTree or subclass of RegexTree
    Return the root of the tree which has been tranformed from the valid regex
    expression valid_r.
    REQ: valid_r must be valid regex expression.
    >>> build_regex_tree('(1|(0*.e))')
    BarTree(Leaf('1'), DotTree(StarTree(Leaf('0')), Leaf('e')))
    >>> build_regex_tree('0***')
    StarTree(StarTree(StarTree(Leaf('0'))))
    '''
    # base case
    # if valid_r is the base regex which the length is one.
    # the form of 'base_regex'
    if valid_r in base_regex:
        root = Leaf(valid_r)
        return root
    # if the valid_r is the base regex with star(s).
    # the form of 'base_regex + star(s)'
    elif valid_r[0] in base_regex:
        # if there is with only one star
        l1 = Leaf(valid_r[0])
        root = StarTree(l1)
        # if there are more than one stars
        if len(valid_r) > 2:
            for i in range(len(valid_r) - 2):
                root = StarTree(root)
        return root
    # the form of '(regex)'
    elif valid_r[0] == '(' and valid_r[-1] == ')':
        # if valid_r takes bar operation with two leaves,
        # the form of (base_regex + star(s) operation base_regex)
        if valid_r[1] in base_regex and valid_r[-2] in base_regex:
            r_c1 = Leaf(valid_r[-2])
            l_c_r1 = build_regex_tree(valid_r[1:-3])
            opr1 = valid_r[-3]
            if opr1 == '.':
                root = DotTree(l_c_r1, r_c1)
            elif opr1 == '|':
                root = BarTree(l_c_r1, r_c1)
            return root
        # if the left side of the bar is not in base regex and the right side
        # of the bar is in base regex,
        # the form of ((regex) + star(s) operation base_regex)
        elif valid_r[1] == '(' and valid_r[-2] in base_regex:
            r_c2 = Leaf(valid_r[-2])
            l_c_r2 = build_regex_tree(valid_r[1:-3])
            opr2 = valid_r[-3]
            if opr2 == '.':
                root = DotTree(l_c_r2, r_c2)
            elif opr2 == '|':
                root = BarTree(l_cr2, r_c2)
            return root
        # the form of ((regex) + star(s) operation (regex)/base_regex  (star(s))
        elif valid_r[1] == '(' and valid_r[-2] == star:
            # find the operation and base regex on the left side
            ind = 0
            found = False
            while ind < len(valid_r) - 1 and not found:
                if valid_r[-ind - 2] in base_regex or valid_r[-ind - 2] == ')':
                    rr_index = -ind - 2
                    found = True
                ind += 1
            # the form of ((regex) operation(s) base_regex (star(s)))
            if valid_r[rr_index] in base_regex:
                r_c3 = build_regex_tree(valid_r[rr_index:-1])
                l_c_r3 = build_regex_tree(valid_r[1:rr_index - 1])
                opr3 = valid_r[rr_index - 1]
                if opr3 == '.':
                    root = DotTree(l_c_r3, r_c3)
                elif opr3 == '|':
                    root = BarTree(l_c_r3, r_c3)
                return root
            # the form of ((regex) operation(s) (r) + (star(s)))
            if valid_r[rr_index] == ')':
                seperated_list = seperate_parenthesis(valid_r[1:-1])
                l_c_r4 = build_regex_tree(seperate_list[0] +
                                          [seperate_list[1][:-1]])
                r_c_r4 = build_regex_tree(seperate_list[2] + seperate_list[3])
                opr4 = seperate_list[1][-1]
                if opr4 == '.':
                    root = DotTree(l_c_r4, r_c_r4)
                elif opr4 == '|':
                    root = BarTree(l_c_r4, r_c_r4)
                return root
        # if the right side of the bar is not in base regex and the left side
        # of the bar is in base_regex.
        # the form of (base_r operation(s) (r))
        elif valid_r[1] in base_regex and valid_r[-2] == ')':
            # find the parenthesis on the right side of the non star operation.
            j = 2
            found_right = False
            while j < len(valid_r) - 2 and not found_right:
                if valid_r[j] == '(':
                    found_right = True
                    right_ind = j
                j += 1
            l_c_r5 = build_regex_tree(valid_r[1:right_ind - 1])
            r_c_r5 = build_regex_tree(valid_r[right_ind:-1])
            opr5 = valid_r[right_ind - 1]
            if opr5 == '.':
                root = DotTree(l_c_r5, r_c_r5)
            elif opr5 == '|':
                root = BarTree(l_c_r5, r_c_r5)
            return root
        # the form of (base_r + operation(s) + (r)/base_r + star(s))
        elif valid_r[1] in base_regex and valid_r[-2] == star:
            k = 2
            found_r = False
            while k < len(valid_r) - 2 and not found_r:
                if valid_r[k] in non_star_oprs:
                    opr6_ind = k
                    found_r = True
                k += 1
            opr6 = valid_r[opr6_ind]
            right_r = valid_r[opr6_ind + 1]
            l_c6 = build_regex_tree(valid_r[1:opr6_ind])
            r_c6 = build_regex_tree(valid_r[opr6_ind + 1:-1])
            if opr6 == '.':
                root = DotTree(l_c6, r_c6)
            elif opr6 == '|':
                root = BarTree(l_c6, r_c6)
            return root
        # the form of ((r) + operations + (r))
        elif valid_r[1] == '(' and valid_r[-2] == ')':
            s_list = seperate_parenthesis(valid_r[1:-1])
            opr7 = s_list[1][-1]
            l_c_r7 = build_regex_tree(s_list[0])
            r_c_r7 = build_regex_tree(s_list[2])
            if opr7 == '.':
                root = DotTree(l_c_r7, r_c_r7)
            elif opr7 == '|':
                root = BarTree(l_c_r7, r_c_r7)
            return root
    # the form of (r)*
    elif valid_r[0] == '(' and valid_r[-1] == star:
        for i in range(len(valid_r)):
            if valid_r[-i - 1] == ')':
                r_ind = -i - 1
                c = build_regex_tree(valid_r[0:r_ind + 1])
                root = StarTree(c)
                if len(valid_r[r_ind:]) > 2:
                    for i in range(len(valid_r[r_ind:]) - 2):
                        root = StarTree(root)
                return root


if __name__ == '__main__':
    br1 = RegexTree('0', [])
    br2 = RegexTree('1', [])
    br3 = RegexTree('2', [])
    br4 = RegexTree('e', [])
    dt = DotTree(br1, br2)
    bt = BarTree(dt, br2)
    dt2 = DotTree(br1, br2)
    st = StarTree(dt)
    print('THEY MATCH -> ' + str(regex_match(st, '1111')))
    print('THEY MATCH -> ' + str(regex_match(dt, '01')))
    print('THEY MATCH -> ' + str(regex_match(bt, '01')))
    print('THEY MATCH -> ' + str(regex_match(dt2, '01')))
    print('THEY MATCH -> ' + str(regex_match(bt, '1')))
    #print('perm'+ str(all_regex_permutations('((1|0*).0)')))
    a = build_regex_tree('1')
    print(a)
    b = build_regex_tree('((1.0)|(0*.1))')
    print(b)
    c = build_regex_tree('(1*.0)')
    print(c)
    print(c.get_left_child().get_child().get_symbol())
    d = build_regex_tree('(1*|0***)')
    print(d)
    e = build_regex_tree('(1|0)**')
    print(e)
    f = build_regex_tree('((1.(0|1)**).0)')
    print(f)
    print(all_regex_permutations('()1.2'))
