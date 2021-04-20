import math
from .Circle import Circle
from .logicFuncs import *


def isInCircle(c, x=0, y=0):
    cx = c.getCenter()[0]
    cy = c.getCenter()[1]
    cr = c.getRadius()
    if x <= cx + cr and x >= cx - cr and y <= cy + cr and y >= cy - cr:
        return abs(y - cy) <= math.sqrt(cr**2 - (x - cx)**2)
    return False



def makeCircles(sets):
    circles = []
    coords = getCircleCoords(sets)
    maxSize = max(len(s[1]) for s in sets)
    for i, (x, y) in enumerate(coords):
        c = Circle(int(round(x)), int(round(y)), 100)
        c.name = sets[i][0]
        c.color = COLORS[i]
        c.size = len(sets[i][1])
        c.r = (100 * sqrt(c.size)) / sqrt(maxSize)
        c.set = (sets[i][0], sets[i][1])
        c.updateSet()
        circles.append({'name': sets[i][0], 'circle': c})
    return circles


def draw(s, circles):
    parsed = parse(s)
    print(parsed)
    variables = getVars(s)

    def boolify(statements): # returns f(x, y) which returns a bool
        ls = []
        for i in statements['clauses']:
            if isinstance(i, str):
                c = next(item['circle']
                         for item in circles if item["name"] == i)

                def assignLambda(c):
                    return lambda x, y: isInCircle(c, x, y)
                print('appending for circle: %s' % c)
                ls.append(assignLambda(c))
            else:
                print('recursive call with: ' + str(i))
                ls.append(boolify(i))
        if statements['type'] == 'union':
            return lambda x, y: oor([b(x, y) for b in ls])
        elif statements['type'] == 'intersect':
            return lambda x, y: aand([b(x, y) for b in ls])
        elif statements['type'] == 'not':
            return lambda x, y: nnot([b(x, y) for b in ls])
        elif statements['type'] == 'difference':
            return lambda x, y: aand([ls[0](x, y), nnot([aand([b(x, y) for b in ls])])])
        elif statements['type'] == 'symmetric':
            return lambda x, y: aand([oor([b(x, y) for b in ls]), nnot([aand([b(x, y) for b in ls])])])
        elif statements['type'] == 'passthru':
            return lambda x, y: passthru([b(x, y) for b in ls])

    booled = boolify(parsed)
    # for w in range(500):
    #     for z in range(500):
    #         if booled(w, z):
    #             blob = Point(w, z)
    #             blob.setFill("green")
    #             blob.draw(win)
    return booled

def makeImgData(booled): # return 500x500x4 array of rgba values
    imgdata = []
    
    for x in range(500):
        row = []
        for y in range(500):
            # print('x: %s y: %s' % (x, y))
            if booled(x, y):
                row.append([255, 0, 0, 255]) #red, alpha = 1
            else:
                row.append([255, 255, 255, 0]) # white, alpha = 0
        imgdata.append(row)
    print('imgdata')
    return imgdata

def makeVenn(s, sets=[]):
    context = {}
    context['vars'] = getVars(s)
    if len(context['vars']) != len(sets):
        for i in range(len(sets), len(context['vars'])):
            sets.append((context['vars'][i], [j for j in range(0, (i + 1)*5, i + 1)]))
        if len(context['vars']) < len(sets):
            sets = sets[:len(context['vars'])]
    print(sets)
    circles = makeCircles(sets)
    # maxSize = max(s[1] for s in sizes)
    # for c in circles:
    #     c['circle'].r = (100 * sqrt(c['circle'].size)) / sqrt(maxSize)
    # # map(lambda x: x['circle'].r = (100 * sqrt(x['circle']['size'])) / sqrt(maxSize), circles) # scales all r to be in range 0-100
    context['circles'] = circles
    context['imgData'] = makeImgData(draw(s, context['circles']))
    context['cardinalities'] = overlapValues(sets)
    context['final'] = calculateFinal(s, sets)
    return context


# def main():
#     win = GraphWin("Venn  Diagrams", 500, 500)
#     userin = '(A ∩ !(B ∪ C))'
#     circles = makeCircles(userin)
#     for c in circles:
#         c['circle'].draw(win)
#     draw(userin, circles, win)

#     for c in circles:
#         c['circle'].undraw()
#         c['circle'].draw(win)

#     win.getMouse()
#     win.close()


# main()