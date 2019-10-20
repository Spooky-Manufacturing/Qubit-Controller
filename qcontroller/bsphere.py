

class BlochSphere:
    def __init__(self, c, xpos, ypos, r):
        self.c = c
        self.xpos = xpos
        self.ypos = ypos
        self.r = r
        self._rotate = None
        self.graph = [
                 {
                  'id': 'x',
                  'stroke': [0, 255, 0],
                  'weight': 1,
                  'line':{'xstart':0, 'ystart':0, 'zstart':self.r, 'xend':self.r, 'yend':0, 'zend':self.r},
                  'label':{'text': "X", 'x':0, 'y':14, 'z':self.r}
                  },
                 {
                  'id': 'y',
                  'stroke': [255,0,0],
                  'weight': 1,
                  'line':{'xstart':0, 'ystart':0, 'zstart': self.r, 'xend':0, 'yend':-self.r, 'zend':self.r},
                  'label':{'text':"Y", 'x': -14, 'y': -14, 'z': self.r}
                  },
                 {
                  'id': 'z',
                  'stroke': [0,0,255],
                  'weight': 1,
                  'line':{'xstart':0, 'ystart':0, 'zstart':self.r, 'xend':self.r, 'yend':-self.r, 'zend':-self.r},
                  'label':{'text':"Z", 'x':14, 'y':-18, 'z': self.r}
                  }
                 ]
        
    def plot(self, x, y):
        if y == 0:
            self._rotate = 0
        else:
            self._rotate = atan(x/y)

    def angle(self, a):
        self._rotate = radians(a)
        
    def display(self):
        pushMatrix()
        ortho()
        ellipseMode(CENTER)
        stroke(self.c)
        noFill()
        lights()
        translate(self.xpos, self.ypos, 0)
        sphere(self.r)
        sphereDetail(10)
        popMatrix()
        pushMatrix()
        translate(self.xpos, self.ypos, 0)
        # Draw X Axis
        for each in self.graph:
            stroke(*each['stroke'])
            strokeWeight(each['weight'])
            line(each['line']['xstart'], each['line']['ystart'], each['line']['zstart'],
                 each['line']['xend'], each['line']['yend'], each['line']['zend'])
            text(each['label']['text'], each['label']['x'], each['label']['y'], each['label']['z'])
        # Draw Bloch Labels
        text("0", 0, -self.r-2, self.r/2)
        text("1", 0, self.r+14, self.r/2)
        popMatrix()
        
        pushMatrix()
        rectMode(CORNER)
        translate(self.xpos, self.ypos, 0)
        stroke(200)
        fill(200)
        strokeWeight(5)
        if self._rotate != None:
            rotate(-self._rotate)
        box(self.r, 5, self.r/2)
        popMatrix()
