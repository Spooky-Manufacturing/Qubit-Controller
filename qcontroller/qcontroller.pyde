add_library('controlP5')
add_library('serial')
add_library('arduino')

from bsphere import BlochSphere
from gout import GraphOut

off = color(4, 79, 111)
on  = color(84, 145, 158)

blochSphere = BlochSphere(color(100),150,150,100)
graphOut = GraphOut(320, 4, [300, 300])

class TextListener(ControlListener):
    global lc
    global output
    
    def cmd(self, e):
        try:
            l = e.getStringValue().lower()
            cmd = l.split(' ')
            if cmd[0] == 'add':
                if cmd[1] == 'data':
                    # add data
                    Print(int(cmd[2]), int(cmd[3]))
                    self.addData(float(cmd[2]), float(cmd[3]))
                    pass
                else:
                    pass
            elif cmd[0] == 'angle':
                Print(int(cmd[1]))
                self.addAngle(float(cmd[1]))
            elif cmd[0] in ('h', 'hadamard'):
                Hadamard()
                pass
            elif cmd[0] in ('r', 'random'):
                Random(int(''.join(cmd[1:])))
                pass
            elif cmd[0] in ('t', 'test'):
                Println('test')
            elif cmd[0] == 'reset':
                self.reset()
            elif cmd[0] == 'clear':
                self.clear()
            elif cmd[0] == 'save':
                self.save()
            else:
                Print(str(''.join([c for c in cmd])))
                try:
                    # for debugging purposes only
                    #exec(''.join([str(c) for c in cmd]))
                    pass
                except:
                    pass
        except Exception as e:
            Print(e)
            
    def clear(self):
        output.clear()
        output.setText('Output: \n')
    
    def reset(self):
        graphOut.addData(10, 0)
        blochSphere.plot(0, 0)
        blochSphere.angle(0)

    def addAngle(self, a, b=False):
        if lc.getDataSet("Angle").size()>10:
            lc.removeData("Angle", 0)
        lc.addData("Angle", radians(a%360))
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
        if angle % 360 > 45 and angle % 360 < 225:
            angle = 1
        elif angle % 360 < 45 and angle % 360 > -225:
            angle = 0
        else:
            angle = 0.5
        lc.addData("Bool", angle)
            
    def save(self, out='output.txt'):
        with open(out, 'w') as f:
            f.write(output.getText())
        self.clear()

    def addData(self, x, y):
        graphOut.addData(x, y)
        blochSphere.plot(x, y)
        self.addBool(x, y)

    def controlEvent(self, e):
        println(e)
        self.cmd(e)

def Hadamard(e):
    global arduino
    global cp5
    
    Print("Hadamard!")
    
def hbutton(cp5, font):
    hButton = cp5.addButton("HGate")
    hButton.setPosition(0,300)
    hButton.setSize(120,30)
    hButton.setFont(font)
    hButton.onClick(Hadamard)
    return hButton

def Random(e):
    Print("random!")
    Print(e)

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
    output.setColorForeground(color(255,100))
    output.setScrollForeground(color(255))
    output.setScrollBackground(color(0))
    output.setText("Output: \n")
    output.show()
    output.showArrow()
    output.showBar()
    return output


def inputTxt(cp5, font, tlistener):
    c = cp5.addTextfield("carat")
    c.setPosition(0,560).setSize(14,40).setFont(font)
    c.setColor(color(128)).setColorBackground(color(0,0))
    c.setColorForeground(color(255,255))
    c.setText(">")
    ip = cp5.addTextfield("input")
    ip.setPosition(14, 560).setSize(686,40).setFont(font)
    ip.setColor(color(128)).setColorBackground(color(0,0))
    ip.setColorForeground(color(255,255))
    cp5.getController("input").addListener(tlistener)
    return ip

def LineChart(cp5):
    lc = cp5.addChart("")
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
    lc.setCaptionLabel("Angle (pink) and Boolean (green)")
    return lc

def setup():
    global arduino
    global cp5
    global output
    global lc
    size(800, 600, P3D)
    font = createFont("sansserif", 20)
    
    # Setup Arduino
    port = 0
    arduino = Arduino(this, Arduino.list()[port], 9600)
    tlistener = TextListener()
    # Setup CP5
    cp5 = ControlP5(this)
    output = outputTxt(cp5, font)
    ip = inputTxt(cp5, font, tlistener)
    hButton = hbutton(cp5, font)
    rButton = rbutton(cp5, font)
    lc = LineChart(cp5)


def Print(*args, **kwargs):
    global output
    print(args, kwargs)
    output.append(''.join([str(arg) + ',' for arg in args]).strip(',') + '\n')

 
def draw():
    global H
    global V
    global output
    background(0)
#    noStroke()
    H = arduino.analogRead(0)
    V = arduino.analogRead(1)
    blochSphere.display()
    graphOut.display()
