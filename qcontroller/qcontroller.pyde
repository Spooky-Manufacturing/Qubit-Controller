add_library('controlP5')
add_library('serial')
add_library('arduino')
off = color(4, 79, 111)
on  = color(84, 145, 158)

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

blochSphere = BlochSphere(color(100),150,150,100)

class GraphOut():
    def __init__(self, x, y, sizes):
        self.x = x
        self.y = y
        self.xsize = sizes[0]
        self.ysize = sizes[1]
        self.xcenter = self.x + self.xsize/2
        self.ycenter = (self.y + self.ysize)/2
        self.qubit = [0,0,0,0]
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

graphOut = GraphOut(320, 4, [300, 300])
graphOut.addData(10,0)


class TextListener(ControlListener):
    global lc

    def cmd(self, e):
        try:
            print(e)
            l = e.getStringValue().lower()
            cmd = l.split(' ')
            if cmd[0] == 'add':
                if cmd[1] == 'data':
                    # add data
                    print(cmd[2], cmd[3])
                    self.addData(float(cmd[2]), float(cmd[3]))
                    pass
                else:
                    pass
            elif cmd[0] == 'angle':
                self.addAngle(float(cmd[1]))
            elif cmd[0] in ('h', 'hadamard'):
                Hadamard()
                pass
            elif cmd[0] in ('r', 'random'):
                Random()
                pass
            elif cmd[0] in ('t', 'test'):
                println('test')
            elif cmd[0] == 'reset':
                self.reset()
            else:
                print(cmd)
        except Exception as e:
            print(e)
    
    def reset(self):
        graphOut.addData(10, 0)
        blochSphere.plot(0, 0)
        blochSphere.angle(0)

    def addAngle(self, a, b=False):
        if lc.getDataSet("Angle").size()>10:
            lc.removeData("Angle", 0)
        lc.push("Angle", radians(a%360))
        if b == False:
            self.addBool(angle=a)
            # Set blochsphere
            blochSphere.angle(a)
            # set graphOut
            graphOut.addAngle(a)
        
    def addBool(self, x=0, y=0, angle=None):
        if lc.getDataSet("Bool").size()>10:
            lc.removeData("Bool", 0)
        if angle == None:
            angle = degrees(atan(x/y))
            self.addAngle(angle, True)
        if angle % 360 >= 180 and angle % 360 <= 360:
            angle = 1
        else:
            angle = 0
        lc.push("Bool", angle)
            
    
    def addData(self, x, y):
        print(x, y)
        graphOut.addData(x, y)
        blochSphere.plot(x, y)
        self.addBool(x, y)
        pass
        
    def controlEvent(self, e):
        self.cmd(e)
    
def Hadamard():
    global arduino
    global cp5
    
    print("Hadamard!")
    
def hbutton(cp5, font):
    hButton = cp5.addButton("HGate")
    hButton.setPosition(0,300)
    hButton.setSize(120,30)
    hButton.setFont(font)
    hButton.onClick(Hadamard)
    return hButton

def Random(e):
    print("random!")

def rbutton(cp5, font):
    rButton = cp5.addButton("Random")
    rButton.setPosition(122, 300)
    rButton.setSize(120, 30)
    rButton.setFont(font)
    rButton.onClick(Random)
    return rButton
    
def outputTxt(cp5, font):
    output = cp5.addTextarea("output")
    output.setPosition(700,0).setSize(100,600).setFont(font).setLineHeight(14)
    output.setColor(color(128)).setColorBackground(color(255,100))
    output.setColorForeground(color(255,100)).setScrollActive(1)
    output.setScrollForeground(color(193)).setScrollBackground(color(12,43))
    output.setText("Output: \n")
    return output

def inputTxt(cp5, font):
    c = cp5.addTextfield("carat")
    c.setPosition(0,560).setSize(14,40).setFont(font)
    c.setColor(color(128)).setColorBackground(color(0,0))
    c.setColorForeground(color(255,255))
    c.setText(">")
    ip = cp5.addTextfield("input")
    ip.setPosition(14, 560).setSize(686,40).setFont(font)
    ip.setColor(color(128)).setColorBackground(color(0,0))
    ip.setColorForeground(color(255,255))
    cp5.getController("input").addListener(TextListener())
    return ip

def LineChart(cp5):
    lc = cp5.addChart("line")
    lc.setPosition(0,335)
    lc.setSize(700,200)
    lc.setRange(0,1)
    lc.setView(Chart.LINE)
    lc.getColor().setBackground(color(255,100))
    lc.addDataSet("Angle")
    lc.addDataSet("Bool")
    lc.setColors("Angle", color(255,0,255), color(255,0,0))
    lc.setColors("Bool", color(0,255,0), color(0,255,255))
    lc.setData("Angle", [0.0 for i in range(20)])
    lc.setData("Bool", [0.0 for i in range(20)])
    lc.setStrokeWeight(1.5)
    return lc

def setup():
    global arduino
    global cp5
    size(800, 600, P3D)
    font = createFont("sansserif", 20)
    
    # Setup Arduino
    port = 0
    arduino = Arduino(this, Arduino.list()[port], 9600)
    
    # Setup CP5
    cp5 = ControlP5(this)
    output = outputTxt(cp5, font)
    ip = inputTxt(cp5, font)
    hButton = hbutton(cp5, font)
    rButton = rbutton(cp5, font)
    global lc
    lc = LineChart(cp5)



 
 
def draw():
    global H
    global V
    background(0)
#    noStroke()
    H = arduino.analogRead(0)
    V = arduino.analogRead(1)
    blochSphere.display()
    graphOut.display()
