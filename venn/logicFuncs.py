from math import pi, sqrt, acos
from sympy import symbols, solve, Eq, sin, cos, lambdify
INTERSECT = '\u2229'
UNION = '\u222A'
SYMMETRIC = '\u0394'
DIFFERENCE = '-'

COLORS = ["blue", "orange", "purple", "green", "yellow"]


def nextBiggestNumber(n, ls):
    temp = max(ls) + 1
    for i in ls:
        if i > n and i < temp:
            temp = i
    return temp


def findPairs(s):
    opens = []
    closes = []

    for i in range(len(s)):
        if s[i] == '(':
            opens.append(i)
        elif s[i] == ')':
            closes.append(i)

    pairs = []
    for i in reversed(range(len(opens))):
        nextBiggest = nextBiggestNumber(opens[i], closes)
        pairs.append([opens[i], nextBiggest])
        opens.remove(opens[i])
        closes.remove(nextBiggest)

    return pairs


def findMatchingParen(n, pairs):
    for i in pairs:
        if i[0] == n:
            return i[1]
    print("here")


def splitClauses(s):
    pairs = findPairs(s)
    clauses = []
    openLocation = -1

    clause = ''
    ignoreUntil = 0
    for i in range(len(s)):
        if i >= ignoreUntil:
            clause += s[i]
            if s[i] == INTERSECT or s[i] == UNION or s[i] == SYMMETRIC or s[i] == DIFFERENCE:
                if len(clause.strip()) > 1:
                    clauses.append(clause[:-1].strip())
                clauses.append(s[i])
                clause = ''

            elif s[i] == '!':
                if s[i + 1] == '(':
                    clause = ''
                    ignoreUntil = findMatchingParen(i+1, pairs) + 1
                    clauses.append(['!', splitClauses(s[i+2:ignoreUntil])])
                else:
                    clauses.append(['!', s[i+1]])
                    clause = ''
                    ignoreUntil = i + 2

            elif s[i] == '(':
                if len(clause.strip()) > 1:
                    clauses.append(clause[:-1].strip())
                clause = ''
                ignoreUntil = findMatchingParen(i, pairs) + 1
                clauses.append(splitClauses(s[i+1:ignoreUntil]))
            elif s[i] == ')':
                if len(clause.strip()) > 1:
                    clauses.append(clause[:-1].strip())
                clause = ''
    if len(clause.strip()) > 0:
        clauses.append(clause.strip())
    if len(clauses) > 0:
        return clauses
    else:
        return s


def getType(ls):
    prevElement = ''
    for i in range(len(ls)):
        if isinstance(ls[i], list): # list of clauses
            if len(ls) > 1:
                prevElement = getType(ls[i])
            else:
                return getType(ls[i])
        elif ls[i] == INTERSECT or ls[i] == UNION or ls[i] == SYMMETRIC or ls[i] == DIFFERENCE:
            temp = {
                'type': '',
                'clauses': []}
            if ls[i] == INTERSECT:
                temp['type'] = 'intersect'
            elif ls[i] == UNION:
                temp['type'] = 'union'
            elif ls[i] == SYMMETRIC:
                temp['type'] = 'symmetric'
            elif ls[i] == DIFFERENCE:
                temp['type'] = 'difference'

            if isinstance(prevElement, str) or isinstance(prevElement, dict):
                temp['clauses'].append(prevElement)
            else:
                temp['clauses'].append(getType(prevElement))

            for j in range(i+1, len(ls)):
                if isinstance(ls[j], str) and ls[j] != INTERSECT and ls[j] != UNION and ls[j] != SYMMETRIC and ls[j] != DIFFERENCE: # variable
                    temp['clauses'].append(ls[j])
                elif ls[j] == INTERSECT:
                    temp['clauses'][-1] = {'type': 'intersect',
                                           'clauses': [temp['clauses'][-1], getType(ls[j+1:])]}
                    break
                elif ls[j] == UNION:
                    temp['clauses'][-1] = {'type': 'union',
                                           'clauses': [temp['clauses'][-1], getType(ls[j+1:])]}
                    break
                elif ls[j] == SYMMETRIC:
                    temp['clauses'][-1] = {'type': 'symmetric',
                                           'clauses': [temp['clauses'][-1], getType(ls[j+1:])]}
                    break
                elif ls[j] == DIFFERENCE:
                    temp['clauses'][-1] = {'type': 'difference',
                                           'clauses': [temp['clauses'][-1], getType(ls[j+1:])]}
                    break
                elif ls[j] == '!':
                    temp['clauses'][-1] = {'type': 'not',
                                           'clauses': [getType(ls[j+1:])]}
                    break
                else:
                    temp['clauses'].append(getType(ls[j]))
            return temp
        elif ls[i] == '!':
            temp = {
                'type': 'not',
                'clauses': []}

            if isinstance(ls[i+1], str):
                temp['clauses'].append(ls[i+1])
            else:
                temp['clauses'].append(getType(ls[i+1]))
            return temp
        else:  # ls[i] is a variable
            prevElement = ls[i]
    return {'type': 'passthru', 'clauses': [prevElement]}


def parse(s):
    return getType(splitClauses(s.strip()))


def aand(ls):
    for b in ls:
        if not b:  # b is false
            return False
    return True


def oor(ls):
    for b in ls:
        if b:
            return True
    return False


def nnot(a):
    return not a[0]


def passthru(a):
    return a[0]


def getVars(s):
    v = []
    for i in s:
        if i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and i not in v:
            v.append(i)
    return v


def getCircleCoords(sets):
    center = 250
    n = len(sets)
    r = 100 # base size
    r2 = r/2  # distance circles are from center
    ls = []
    maxSize = max(len(s[1]) for s in sets)
    sizes = list(map(lambda s: r * sqrt(len(s[1])) / sqrt(maxSize), sets)) # scales all sizes to be in range 0-100
    distances = calculateOverlap(sets)
    if n == 1:
        ls.append((center, center))
    elif n == 2:
        ls.append((center-distances[0]/2, center))
        ls.append((center+distances[0]/2, center))
    elif n == 3:
        print('distances %s' % distances)
        trih = distances[1] * sin(acos((distances[0]**2 + distances[1]**2 - distances[2]**2)/(2*distances[0]*distances[1])))
        aoffset = distances[2] * cos(acos((distances[2]**2 + distances[0]**2 - distances[1]**2)/(2*distances[2]*distances[0])))
        # height of triangle formed by the distances between the circles
        ls.append([0, 0]) # circle 1
        ls.append([distances[0], 0]) # circle 2
        ls.append([aoffset, trih]) # circle 3
        for i in ls:
            i[0] += center - aoffset
            i[1] += center - (trih/2)
        
        # boundingBox = (max(sizes[0] + sizes[1] + distances[0], 2*sizes[2]), max(sizes[0], sizes[1]) + sizes[2] + trih)
        # width = boundingBox[0]
        # height = boundingBox[1]
        # ls.append((center- width/2 + , center-r2))
        # r2 = sizes[1]/2
        # ls.append((center+r2, center-r2))
        # r2 = sizes[2]/2
        # ls.append((center, center+r2))
    elif n == 4:
        ls.append((center-(distances[0]/2), center-(distances[3]/2)))
        ls.append((center+(distances[0]/2), center-(distances[1]/2)))
        ls.append((center+(distances[2]/2), center+(distances[1]/2)))
        ls.append((center-(distances[2]/2), center+(distances[3]/2)))
        r2 = sizes[3]/2
        
    elif n == 5:
        raise IOError('too many variables entered')
    #     r2 = 0.65*size[0]
    #     ls.append((center, center-r2))
    #     r2 = 0.65*size[1]
    #     ls.append((center+(sin((2*pi)/5)*r2), center-(cos((2*pi)/5)*r2)))
    #     r2 = 0.65*size[2]
    #     ls.append((center+(sin((4*pi)/5)*r2), center+(cos(pi/5)*r2)))
    #     r2 = 0.65*size[3]
    #     ls.append((center-(sin((4*pi)/5)*r2), center+(cos(pi/5)*r2)))
    #     r2 = 0.65*size[4]
    #     ls.append((center-(sin((2*pi)/5)*r2), center-(cos((2*pi)/5)*r2)))
    return ls

def calculateFinal(s, sets):
    parsed = parse(s)
    def flatten(ls):
        templs = []
        for i in ls:
            templs += i
        return templs
    def findUnion(sets):
        lst = []
        for i in flatten(sets):
            if i not in lst:
                lst.append(i)
        return lst
    def findIntersect(sets):
        lst = []
        for i in sets[0]:
            for j in sets[1:]:
                if i not in j:
                    break
                lst.append(i)
        return lst
    def findDifference(sets): # only 2 clauses allowed
        lst = []
        for i in sets[0]:
            if i not in sets[1]:
                lst.append(i)
        return lst
    def findSymmetric(sets): # only 2 clauses allowed
        return findDifference(findUnion(sets), findIntersect(sets))
    def findNot(sets): # only 1 clause allowed
        return findDifference([[i for i in range(-1000, 1001)], sets[0]])

    def calculate(statements): # returns f(x, y) which returns a bool
        ls = []
        for i in statements['clauses']:
            if isinstance(i, str): # variable
                s = next(item[1]
                         for item in sets if item[0] == i)
                ls.append(s.copy())
            else:
                print('recursive call with: ' + str(i))
                ls.append(calculate(i))
        if statements['type'] == 'union':
            return findUnion(ls)
        elif statements['type'] == 'intersect':
            return findIntersect(ls)
        elif statements['type'] == 'not':
            return findNot(ls)
        elif statements['type'] == 'difference':
            return findDifference(ls)
        elif statements['type'] == 'symmetric':
            return findSymmetric(ls)
        elif statements['type'] == 'passthru':
            return ls[0]
    final = calculate(parsed)
    if len(final) > 100:
        return['∞', '∞']
    return [len(final), str('{' + str(final)[1:-1] + '}')]

# print(calculateFinal('(A ∩ B) ∩ !(A ∩ B ∩ C))', [
#     ('A', [0, 1, 2, 3, 4]),
#     ('B', [0, 2, 4, 6, 8]),
#     ('C', [0, 3, 6, 9, 12]),
# ]))

def overlapValues(sets): # returns overlapping values 
    # sets=[('A', [0, 1, 2, 3]), ...]
    def findOverlap(s1, s2): # returns the values that overlap between 2 sets
        o = []
        for i in s1:
            if i in s2:
                o.append(i)
        return o

    ls = []
    for i in sets:
            ls.append('%s (%s): {%s}' % (i[0], len(i[1]), str(i[1])[1:-1]))
        
    if len(sets) == 1:
        return ls
    elif len(sets) == 2:
        ls.append('%s (%s): {%s}' % (str(sets[0][0] + ' \u2229 ' + sets[1][0]), len(findOverlap(sets[0][1], sets[1][1])), str(findOverlap(sets[0][1], sets[1][1]))[1:-1]))
        return ls
    nextIndex = 0
    for i, (v, s) in enumerate(sets):
        nextIndex = i + 1
        if nextIndex == len(sets):
            nextIndex = 0
        ls.append('%s (%s): {%s}' % (str(v + ' \u2229 ' + sets[nextIndex][0]), len(findOverlap(s, sets[nextIndex][1])), str(findOverlap(s, sets[nextIndex][1]))[1:-1]))
        
    if len(sets) == 3:
        # intersection of A, B, C
        intersectOfAll = findOverlap(findOverlap(sets[0][1], sets[1][1]), sets[2][1])
        ls.append('%s \u2229 %s \u2229 %s (%s): {%s}' % (sets[0][0], sets[1][0], sets[2][0], len(intersectOfAll), str(intersectOfAll)[1:-1]))
        return ls
    
    elif len(sets) == 4:
        # intersection of A, B, C
        intersectOfThree = findOverlap(findOverlap(sets[0][1], sets[1][1]), sets[2][1])
        ls.append('%s \u2229 %s \u2229 %s (%s): {%s}' % (sets[0][0], sets[1][0], sets[2][0], len(intersectOfThree), str(intersectOfThree)[1:-1]))
        intersectOfThree = findOverlap(findOverlap(sets[1][1], sets[2][1]), sets[3][1])
        ls.append('%s \u2229 %s \u2229 %s (%s): {%s}' % (sets[1][0], sets[2][0], sets[3][0], len(intersectOfThree), str(intersectOfThree)[1:-1]))
        intersectOfThree = findOverlap(findOverlap(sets[2][1], sets[3][1]), sets[0][1])
        ls.append('%s \u2229 %s \u2229 %s (%s): {%s}' % (sets[2][0], sets[3][0], sets[0][0], len(intersectOfThree), str(intersectOfThree)[1:-1]))
        intersectOfThree = findOverlap(findOverlap(sets[3][1], sets[0][1]), sets[1][1])
        ls.append('%s \u2229 %s \u2229 %s (%s): {%s}' % (sets[3][0], sets[0][0], sets[1][0], len(intersectOfThree), str(intersectOfThree)[1:-1]))
        intersectOfAll = findOverlap(findOverlap(findOverlap(sets[0][1], sets[1][1]), sets[2][1]), sets[3][1])
        ls.append('%s \u2229 %s \u2229 %s \u2229 %s (%s): {%s}' % (sets[0][0], sets[1][0], sets[2][0], sets[3][0] , len(intersectOfAll), str(intersectOfAll)[1:-1]))
        return ls


# print(overlapValues([
#     ('A', [0, 1, 2, 3]),
#     ('B', [0, 1, 5, 6]),
#     ('C', [0, 10, 20, 3]),
#     ('D', [0, 10, 5, 60]),
#     # ('C', [11, 0, 2, 6]),
# ]))

def calculateOverlap(sets): # returns distace between circles for desired overlap
    def findOverlap(s1, s2): # returns the number of values that overlap between 2 sets
        o = 0
        for i in s1:
            if i in s2:
                o += 1
        return o
    maxSize = max(len(s[1]) for s in sets)
    ls = []
    radiuses = []
    for s in sets:
        radiuses.append(100 * sqrt(len(s[1])) / sqrt(maxSize))
    print(radiuses)
    for i, (v, s) in enumerate(sets):
        nextIndex = i + 1
        if nextIndex == len(sets):
            nextIndex = 0
        print(findOverlap(s, sets[nextIndex][1]))
        overlapArea = (findOverlap(s, sets[nextIndex][1])/len(s)) * (pi * radiuses[i]**2)
        print('overlap: ' + str(overlapArea))
        
        # overlapArea = circular segment 1 + circular segment 2
        def f(overlap, r1, r2):
            x = symbols('x') # 1/2 angle of c1
            y = symbols('y') # 1/2 angle of c2
            # eq1 = Eq((2/3)*(2*r1*sin(x))*r1*(1-cos(x)) + ((r1*(1-cos(x)))**3)/(4*r1*sin(x)) + (2/3)*(2*r2*sin(y))*r2*(1-cos(y)) + ((r2*(1-cos(y)))**3)/(4*r2*sin(y)) - overlap, 0)
            # eq2 = Eq(r1*sin(x) - r2*sin(y), 0)
            # ans = solve((eq1, eq2), (x, y))
            # print(ans)
            expr1 = (2/3)*(2*r1*sin(x))*r1*(1-cos(x)) + ((r1*(1-cos(x)))**3)/(4*r1*sin(x)) + (2/3)*(2*r2*sin(y))*r2*(1-cos(y)) + ((r2*(1-cos(y)))**3)/(4*r2*sin(y))
            g = lambdify([x, y], expr1)
            bestGuess = (0, 0, 0)
            for d in range(round(r1) + round(r2)):
                for theta in range(90):
                    try:
                        ans = g(theta*(pi/180), acos((d - r1*cos(theta*(pi/180)))/r2))
                        # print('x: %s y: %s ans: %s'% (theta*(pi/180), acos((d - r1*cos(theta*(pi/180))/r2)), ans))
                        if abs(bestGuess[0] - overlap) > abs(ans - overlap):
                            bestGuess = (ans, theta*(pi/180), acos((d - r1*cos(theta*(pi/180)))/r2))
                            # print(bestGuess)
                    except:
                        # print('error at d: %s theta: %s' % (d, theta))
                        pass
            return r1*cos(bestGuess[1]) + r2*cos(bestGuess[2])
            # return r1*cos(ans[0][0]) + r2*cos(ans[0][1])
        
        if overlapArea == 0:
            ls.append(radiuses[i] + radiuses[nextIndex])
        elif overlapArea == pi*(radiuses[i]**2) or overlapArea == pi*(radiuses[nextIndex]**2):
            ls.append(0)
        else:
            ls.append(f(overlapArea, radiuses[i], radiuses[nextIndex]))
        if len(sets) == 2:
            return ls
    return ls
# print(calculateOverlap([
#     ('A', [0, 1, 2, 3, 4]),
#     ('B', [0, 1, 2, 3, 4]),
# ]))

# print(getCircleCoords([
#     ('A', [0, 1, 2, 3, 4]),
#     ('B', [0, 2, 7, 5, 6]),
#     ('C', [0, 2, 3, 9, 10, 11, 12]),
# ]))


# a = "(A ∩ !((B ∪ C) ∩ D))"
# b = "A ∩ B"
# s = "(1 ∩ !(2 ∪ !3) ∪ 4 ∪ ((5 ∪ 6) ∪ 7)))"
# # parsed = parse(a)
# print(splitClauses(b))

# s = '(' + s + ')'  # enclose statement in parentheses
