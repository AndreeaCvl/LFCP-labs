import re


class SimpleParser:
    def __init__(self, inp):
        """
            The constructor of the parser
            :param inp: the input grammar
        """
        self.inp = inp # the grammar
        self.p = {} # productions dict
        self.vt = [] # list of terminals
        self.vn = [] # list of nonterminals
        self.first = {} # first dict
        self.last = {} # last dict
        self.simple_pr_table = [] # the simple precedence table
        self.all_symbols_enc = {} # all terminals + nonterminals of the grammar encoded by row/col in precedence table

    # function to parse the input
    def parse_input(self):
        """
            Function to parse the input grammar
            :return: dict
                the transition table
        """

        # splitting transitions when -> encountered and building a dict
        for transition in self.inp:
            transition = re.sub(r"\s+", "", transition)
            parts = transition.split("->")
            self.p[parts[0]] = parts[1].split("|")

        return self.p

    # function to build the sets of terminals and non-terminals
    def get_vt_vn(self):
        """
            Function to build the sets of terminals and nonterminals
        """
        # set of non-terminals = all keys in the dict
        self.vn = [x for x in self.p.keys()]

        # adding terinals to the vt set, by iterating trough values of the keys and finding lowercase characters
        for prod in self.p.values():
            for rule in prod:
                for symbol in rule:
                    if symbol.islower() and symbol not in self.vt:
                        self.vt.append(symbol)

    def find_first_last(self, key, first_last):
        """
            Builds the first / last matrices
                :param key: char
                    the character for which the program is looking for the first / last values
                :param first_last: string
                    has value "first" in case the program is looking for first values
                    has value "last" in case the program is looking for last values
                :return: dict
                    the found values
        """

        # initialize an empty set for storing all found first symbols
        found = set()

        # iterating through the list of productions of a key
        for rule in self.p[key]:

            # finding the index of the added element to add to the set of found first / last values
            if first_last == "first":
                idx = 0
            elif first_last == "last":
                idx = len(rule) - 1

            # if the first element is a terminal - add to the last_found set
            if rule[idx] in self.vt:
                found.add(rule[idx])

            # add non-terminals which are not yet in the list to the found set and recall the function
            elif rule[idx] != key:
                if rule[idx] in self.vn and rule[idx] not in found:
                    found.add(rule[idx])
                    to_append = self.find_first_last(rule[idx], first_last)
                    found.update(to_append)

            # if element is non-terminal equal to key
            else:
                found.add(rule[idx])

        return found

    def build_prec_table(self):
        """
            Initializes empty precedence table
        """
        # getiting the list of al symbols
        all_symbols = self.vn + self.vt + ["$"]

        # initializing an empty matrix
        self.simple_pr_table = [[[] for x in range(len(all_symbols) + 1)] for y in range(len(all_symbols) + 1)]

        idx = 1

        # adding he row and column names to the matrix
        for symbol in all_symbols:
            self.simple_pr_table[0][idx].append(symbol)
            self.simple_pr_table[idx][0].append(symbol)

            # encoding the symbols from the grammar according to their place in the marix
            self.all_symbols_enc[symbol] = idx
            idx += 1

    def complete_prec_table(self):
        """
            Completes the precedence table according to the rules
        :return:
        """
        def x1_equal_x2(prod):
            """
                Completes the precedence matrix according to the first rule
                    :param prod:
                        The production which is being evaluated
            """

            # if production consists of 2 elements - put equal sign between them
            if (len(prod)) == 2:
                x = self.all_symbols_enc[prod[0]]
                y = self.all_symbols_enc[prod[1]]
                self.simple_pr_table[x][y].append("=")

            # if production consists of 3+ elements - put equal sign between each pair of 2 elements
            elif len(prod) > 2:
                idx = 0
                while idx < len(prod) - 1:
                    x = self.all_symbols_enc[prod[idx]]
                    y = self.all_symbols_enc[prod[idx + 1]]
                    self.simple_pr_table[x][y].append("=")
                    idx += 1

        def x1_smaller_x2(prod):
            """
                Completes the precedence matrix according to the second rule
                    :param prod:
                        The production which is being evaluated
            """
            # if more than 2 elements in a production
            if len(prod) >= 2:
                idx = 0
                while idx < len(prod) - 1:
                    # if there is a pair where the first element is a terminal and the second a non-terminal, add <
                    if prod[idx] in self.vt and prod[idx + 1] in self.vn:
                        x = self.all_symbols_enc[prod[idx]]
                        for symbol in self.first[prod[idx + 1]]:
                            y = self.all_symbols_enc[symbol]
                            self.simple_pr_table[x][y].append("<")
                    idx += 1

        def x1_greater_x2(prod):
            """
                Completes the precedence matrix according to the third rule
                    :param prod:
                        The production which is being evaluated
            """
            # if the length of the production is >2, iterate trough pairs of 2 elements
            if len(prod) >= 2:
                idx = 0
                while idx < len(prod) - 1:
                    # if the first elements is a non-terminal and the second is a terminal
                    if prod[idx] in self.vn and prod[idx + 1] in self.vt:
                        y = self.all_symbols_enc[prod[idx + 1]]
                        for symbol in self.last[prod[idx]]:
                            x = self.all_symbols_enc[symbol]
                            self.simple_pr_table[x][y].append(">")

                    # if both elements in a pair are non-terminals
                    elif prod[idx] in self.vn and prod[idx + 1] in self.vn:
                        for s1 in self.last[prod[idx]]:
                            x = self.all_symbols_enc[s1]
                            for s2 in self.first[prod[idx + 1]]:
                                if s2.islower():
                                    y = self.all_symbols_enc[s2]
                                    self.simple_pr_table[x][y].append(">")
                    idx += 1

        def dollar_signs():
            """
                Add the signs for dollar elements to the matrix
            """

            # initialize empty sets for storing all first and all last elements
            all_first = set()
            all_last = set()

            # completing the wets with first and last elements
            for key in self.p:
                for prod in self.first[key]:
                    all_first.add(prod)
                for prod in self.last[key]:
                    all_last.add(prod)

            # adding the corresponding signs to the matrix

            for c in all_first:
                x = self.all_symbols_enc["$"]
                y = self.all_symbols_enc[c]
                self.simple_pr_table[x][y].append("<")

            for c in all_last:
                x = self.all_symbols_enc[c]
                y = self.all_symbols_enc["$"]
                self.simple_pr_table[x][y].append(">")

        # iterating trough every production and applying the rules
        for k in self.p:
            for production in self.p[k]:
                x1_equal_x2(production)
                x1_smaller_x2(production)
                x1_greater_x2(production)

        # adding the signs for the dollar elements
        dollar_signs()

        # make the matrix beautiful
        for i in range(len(self.simple_pr_table)):
            for j in range(len(self.simple_pr_table[i])):
                if not self.simple_pr_table[i][j]:
                    self.simple_pr_table[i][j].append(" ")

    def build_parser(self):
        """
            Builds the parser
        """

        # reading the input grammar and findint terminals and non-terminals
        self.parse_input()
        self.get_vt_vn()

        # finding the first and last values
        for symbol in self.vn:
            self.first[symbol] = self.find_first_last(symbol, "first")
            self.last[symbol] = self.find_first_last(symbol, "last")

        # building and completing the precedence table
        self.build_prec_table()
        self.complete_prec_table()

    def word_init(self, word):
        """
            Adding signs to the initial word
            :param word: string
                Word to be parsed
            :return: string
                the modified word
        """

        # adding dollar signs in the end and beginning
        word = "$" + word + "$"

        # generating a new word with placed signs
        new_word = ''
        for c in range(len(word) - 1):
            x = self.all_symbols_enc[word[c]]
            y = self.all_symbols_enc[word[c + 1]]

            new_word += word[c] + self.simple_pr_table[x][y][0]

        # adding a "$" at the end of the string
        new_word += "$"

        return new_word

    def find_sequence(self, new_word):
        """
            Finds sequence between "<" and ">"
                :param new_word: string
                    the word to be analyzed
                :return:
                    seq: string, the sequence to be substituted
                    start: int, index of the "<" symbol
                    end: int, index of the ">" symbol
        """
        start = 0
        end = 0

        # finding he first time '>' is encountered
        for i in range(len(new_word)):
            if new_word[i] == '>':
                end = i
                break

        # finding the index of the last '<' before the first '>'
        for i in range(end):
            if new_word[i] == '<':
                start = i

        # finding the sequence to be substituted
        seq = new_word[start + 1: end]

        return seq, start, end

    def find_substitution(self, seq, before, after):
        """
            Find substitution for a given sequence
                :param seq: string,
                    the sequence to be substituted
                :param before: string,
                    the element before the sequence
                :param after: string
                    the element after the sequence
                :return: string
                    the string used for making the substitution
        """

        subst = ''

        # if the sequence consists of only one element
        if len(seq) == 1:
            idx = self.all_symbols_enc[before]

            # finding the symbol equal to the symbol before
            for i in range(len(self.simple_pr_table[idx])):
                if self.simple_pr_table[idx][i][0] == '=':
                    subst = list(self.all_symbols_enc.keys())[list(self.all_symbols_enc.values()).index(i)]

        # if more than 2 elements in the sequence
        elif len(seq) >= 3:
            st = ''
            subst = ''
            # making a string with symbols from the grammar contained in the sequence
            for i in range(len(seq)):
                if seq[i] in self.vt or seq[i] in self.vn:
                    st += seq[i]
            # making the sbstitution if the string is encountered in the ist of productions
            for key in self.p.keys():
                for prod in self.p[key]:
                    if st in prod:
                        subst = key
                        break

        if subst == '':
            return "ERROR"

        return subst

    def find_signs(self, subst, before, after):
        """
            Finds the signs to add before and after the substituted sequence
            :param subst: string
                the new added symbol
            :param before: string
                the element before the substituted sequence
            :param after: string
                the element before the substituted sequence
            :return:
                before_sign: the sign to place before the substituted sequence
                after_signt: the sign to place after the substituted sequence
        """
        # finding the sign before the substituted sequence
        x = self.all_symbols_enc[before]
        y = self.all_symbols_enc[subst]
        before_sign = self.simple_pr_table[x][y][0]

        # finding the sign after the substituted sequence
        x = self.all_symbols_enc[subst]
        y = self.all_symbols_enc[after]
        after_sign = self.simple_pr_table[x][y][0]

        return before_sign, after_sign

    def parse(self, word):
        """
            Function to parse the word
            :param word: string
                word to be parsed
        """

        # adding signs to the original word
        new_word = self.word_init(word)
        print(new_word)

        # cycle executed while parsing is not done
        while len(new_word) > 5:

            # finds sequence between "<" and ">"
            seq, start, end = self.find_sequence(new_word)

            # finding the symbols which are before and after the sequence to be substituted
            before = new_word[start - 1]
            after = new_word[end + 1]

            # find substitution for the detected sequence
            subst = self.find_substitution(seq, before, after)

            # finding the new signs to add before and after the substited sequence
            before_sign, after_sign = self.find_signs(subst, before, after)

            # generating the new sequence to add
            new_seq = before_sign + subst + after_sign

            # splitting the string in 2 parts
            s1 = new_word[:start]
            s2 = new_word[end + 1:]

            # generating the new word
            new_word = s1 + new_seq + s2

            # make the last output beautiful
            if new_word == '$ S $':
                new_word = '$<S>$'

            # print the result for current iteration
            print(new_word)
