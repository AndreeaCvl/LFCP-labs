class NFA:
    # define a NFA class to parse the initial input and represent the NFA

    def __init__(self, a, states, transitions):
        """
            The constructor of the NFA
                :param a: 2d tuple
                    The transition table
                :param states: 1-d list
                    All states of the NFA
                :param states: 1-d list
                    All transition variables of the NFA
        """

        # Setting up the hyper-parameters
        self.nfa_dict = {}
        self._a = a
        self._states = states
        self._transitions = transitions

    def parse_input(self):

        """
            Reads the input and converts it into a NFA
                :return: dict
                    Analytical representation of the NFA
        """

        # initializing an empty dict with states and transition variables as keys

        for Q in self._states:
            self.nfa_dict[Q] = {}
            for T in self._transitions:
                self.nfa_dict[Q][T] = ''

        for i in range(len(self._a)):
            # saving the current needed values in some variables for more readable code
            state = self._a[i][0]
            transition = self._a[i][1]
            dest = self._a[i][2]

            # assigning the keys with corresponding values
            dest += self.nfa_dict[state][transition]
            self.nfa_dict[state][transition] = dest

        return self.nfa_dict


class DFA:
    # define a DFA class to parse store the DFA and the functions for converting the NFA to DFA

    def __init__(self, nfa):
        """
            The constructor of the DFA
                :param nfa: dict
                    The NFA to convert
        """

        # Setting up the hyper-parameters
        self.T = None
        self.Q = None
        self._nfa = nfa

    def convert(self):
        """
            Function to convert NFA to DFA
        """

        def initiate():
            print('CONVERTING THE NFA TO DFA:')

            # Q - a new set of states of the DFA.
            # T - a new transition table of the DFA.
            self.Q = []
            self.T = {}
            print(f'Step 1: T = {self.T}')
            add_starting_state()

        def add_starting_state():

            # Add q0 to Q and transitions of start state q0 to the transition table T
            self.Q.append('q0')
            self.T['q0'] = self._nfa['q0']
            print(f'Step 2: T = {self.T}')
            print('Step 3:')
            add_new_states('q0')

        def add_new_states(last_key):
            """
                Function to add new states and transitions until no new states in T
                    :param last_key: string
                        Last added state in T
            """

            print(f'T = {self.T}')

            # iterating trough every transition state of the last added state
            for transition in self.T[last_key]:
                state = self.T[last_key][transition]

                if len(state) == 2:
                    if state not in self.Q:
                        self.Q.append(state)
                        self.T[state] = self._nfa[state]

                        # calling the function recursively for a new added state
                        add_new_states(state)

                elif len(state) > 2:
                    # in case of nondeterminism (multiple states for a single transition)
                    remove_nondeterminism(state)

            return self.T

        def remove_nondeterminism(string):
            """
                Function to add new states and transitions when there are multiple destination states
                    :param string: string
                        The 'list' of destination-states
            """
            i = 0
            set_of_states = set()

            # creating a set with all states after a transition
            # (because sets are unordered, so it will allow us to compare with sets of states already present in Q)
            while i < len(string):
                s = string[i] + string[i + 1]
                set_of_states.add(s)
                i += 2

            if set_of_states not in self.Q:
                self.T[string] = {}
                self.Q.append(set_of_states)

                # finding the 'destination-states' for each transition of the states in the built above set
                for key in self.T['q0']:
                    set_of_dest = set()
                    dest = ''

                    for state in set_of_states:
                        if len(self._nfa[state][key]) == 2:
                            set_of_dest.add(self._nfa[state][key])
                        elif len(self._nfa[state][key]) > 2:
                            i = 0

                            while i < len(self._nfa[state][key]):
                                s = self._nfa[state][key][i] + self._nfa[state][key][i + 1]
                                set_of_dest.add(s)
                                i += 2

                    # adding the detected destination-states for a given key and initial state to the transition table
                    for d in set_of_dest:
                        dest = dest + d
                    self.T[string][key] = dest
                # calling the addNewStates function for the last added key (destination-state)
                add_new_states(string)

        initiate()
        return self.T


# the input
st = ['q0', 'q1', 'q2', 'q3']
tr = ['a', 'b']

nfa_input = (('q0', 'a', 'q1'),
             ('q1', 'b', 'q2'),
             ('q2', 'b', 'q3'),
             ('q3', 'a', 'q1'),
             ('q2', 'b', 'q2'),
             ('q1', 'a', 'q1'))

my_nfa = NFA(nfa_input, st, tr).parse_input()
my_dfa = DFA(my_nfa).convert()

print()
print(f'The NFA: {my_nfa}')
print(f'The DFA: {my_dfa}')
