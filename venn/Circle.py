class Circle():
    def __init__(self, x, y, r, name='', color='black', size=10, values=[]):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.name = name
        self.size = size # cardinality
        self.set = values
        if len(values) < 1:
            self.set = (self.name, [i for i in range(size)])
        self.set_str = str(self.set[1])[1:-1] #string version without brackets
    def getRadius(self):
        return self.r
    
    def getCenter(self):
        return self.x, self.y
    
    def updateSet(self):
        self.size = len(self.set[1])
        self.set_str = str(self.set[1])[1:-1]
    
    def getDict(self):
        print(self.set)
        return {
            'x': round(self.x),
            'y': round(self.y),
            'r': round(self.r),
            'name': self.name,
            'color': self.color,
            'size': len(self.set[1]),
            'set': self.set,
            'set_str': str(self.set[1])[1:-1],
        }
    def __str__(self):
        return str(self.getDict())