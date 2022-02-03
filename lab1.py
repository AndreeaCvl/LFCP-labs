# initializing a tuple with production values
productions = tuple([
    ('S', 'aD'),
    ('D', 'bE'),
    ('E', 'cF'),
    ('F', 'dD'),
    ('E', 'dL'),
    ('L', 'aL'),
    ('L', 'bL'),
    ('L', 'c')
])

# conversion of the regular grammar into a finite automata
fa = {}
for i in range(len(productions)):
    if len(productions[i][1]) == 2:
        fa[(productions[i][1][1], productions[i][1][0])] = productions[i][0]
    else:
        fa[('Q', productions[i][1])] = productions[i][0]

# the generated finit automata
print(fa)
