class GraphOut():
    def __init__(self, x, y, sizes):
        self.x = x
        self.y = y
        self.xsize = sizes[0]
        self.ysize = sizes[1]
        self.xcenter = self.x + self.xsize/2
        self.ycenter = (self.y + self.ysize)/2
        self.qubit = [0,0,0,0]
        self.addData(0,0)
        pass
    
    def _grid(self):
        # Create Vertical Line
        for i in range(11):
            x = self.x + i * (self.xsize / 10)
            self.lines.append([x, self.y, x, self.ysize])
        # Create Horizontal Lines
        for i in range(11):
            y = self.y + i * (self.ysize / 10)
            self.lines.append([self.x, y, self.x + self.xsize, y])
        println(self.lines)
    
    def addData(self, x, y):
        """Draws a line throuch center of angle of x, y"""
        if y == 0:
            self.addAngle(0)
        else:
            a = int(degrees(atan(x/y)))
            print("Degrees: {}".format(a))
            self.addAngle(a)

    def addAngle(self, a):
        """Draws a line through center of angle a in degrees"""
        a = a * 3.1415 / 180
        x = self.xcenter + cos(a)*120
        y = self.ycenter - sin(a)*120
        x1 = self.xcenter - cos(a)*120
        y1 = self.ycenter + sin(a)*120
        print(x, y)
        self.qubit = [x, y, x1, y1]
        
    def display(self):
        # Draw Grid
        #for each in self.lines:
        #    line(*each)
        # Draw Axis
        # x axis
        stroke(255)
        strokeWeight(1)
        line(self.x, self.ycenter, self.x + self.xsize, self.ycenter)
        # Y axis
        line(self.xcenter, self.y, self.xcenter, self.ysize)
        stroke(255,0,0)
        strokeWeight(2)
        line(*self.qubit)
        stroke(255,0,255)
        
        pass
