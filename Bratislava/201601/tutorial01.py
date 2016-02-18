#######################################################
## Andrej Mosat                                      ##
## v0.3                                              ##
## STMBED20 v01, build alpha                         ##
## code implemented on STMBED20                      ##
## 30/11/2015                                        ##
#######################################################
import pyb
from pyb import Pin
from pyb import SPI
from pyb import Timer

DEBUG=True

# Timers init - micros ticks in 1 us, micros2 in 100 us
micros = pyb.Timer(5, prescaler=59, period=0x3fffffff)
micros.counter(0)

class PinClass(Pin):
  """
  PinClass Pin derived class, positive logic
  .on() = pin high
  .off() = pin low
  """
  def __init__(self, pin):
    self.pin = pin
  def on(self):
    if (self.pin.pull() != self.pin.PULL_DOWN):
      self.pin.low()
    else:
      self.pin.high()
  def off(self):
    if (self.pin.pull() != self.pin.PULL_DOWN):
      self.pin.high()
    else:
      self.pin.low()
  def toggle(self):
    val=self.pin.value()
    self.off()
    val2=self.pin.value()
    if (val==val2):
      self.on()


class Led(PinClass):
  """
  Led is a PinClass Pin derived class, positive logic, pullup
  .on() = turn LED on
  .off() = turn LED off
  """
  def __init__(self, pin):
    self.pin = pin
    if (pin.pull() != pin.PULL_DOWN):
      pin.init(pyb.Pin.OUT_PP, pull=pyb.Pin.PULL_UP)

class PinOutNeg(PinClass):
  """
  PinOutNeg PinClass derived, negative logic, pullup
  .on() = sets pin low
  .off() = sets pin high
  """
  def __init__(self, pin):
    self.pin = pin
    pin.init(pyb.Pin.OUT_PP, pull=pyb.Pin.PULL_UP, af=-1)
  def on(self):
    self.pin.low()
  def off(self):
    self.pin.high()

class PinOut(PinClass):
  """
  PinOutNeg PinClass derived, positive logic, pulldown
  .on() = sets pin high
  .off() = sets pin low
  """
  def __init__(self, pin):
    self.pin = pin
    pin.init(pyb.Pin.OUT_PP, pull=pyb.Pin.PULL_DOWN, af=-1)
  def on(self):
    self.pin.high()
  def off(self):
    self.pin.low()


r=Led(Pin.cpu.A1) 
g=Led(Pin.cpu.A2)
b=Led(Pin.cpu.A3)

def off():
  r=Led(Pin.cpu.A1) 
  g=Led(Pin.cpu.A2)
  b=Led(Pin.cpu.A3)
  r.off()
  g.off()
  b.off()

off()


##############################
btn1=Pin(Pin.cpu.B0, mode=Pin.IN, pull=pyb.Pin.PULL_DOWN) # pin 38
btn2=Pin(Pin.cpu.B10, mode=Pin.IN, pull=pyb.Pin.PULL_DOWN) # pin 40




#########################################



############### BASIC LED on off #############

r.on()
r.off()

g.on()
g.off()

b.on()
b.off()

#####################  read out button states ################
btn1.value()
btn2.value()


##################### define callbacks for buttons ################
def callback1(line):
  print("Callback 1: turn green led ON")
  g.on()

def callback2(line):
  print("Callback 1: turn green led OFF")
  g.off()

extint1 = pyb.ExtInt(btn1, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_DOWN, callback1)
extint2 = pyb.ExtInt(btn2, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_DOWN, callback2)

############################  Redefine callback for buttons ############
def callback3(line):
  print("Callback 3: green led toggle")
  g.toggle()

def callback4(line):
  print("Callback 4: blue led toggle")
  b.toggle()

extint1 = pyb.ExtInt(btn1, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_DOWN, None)
extint1 = pyb.ExtInt(btn1, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_DOWN, callback3)
extint2 = pyb.ExtInt(btn2, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_DOWN, None)
extint2 = pyb.ExtInt(btn2, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_DOWN, callback4)


##############################
# introduce Timers
# introduce PWM
# introduce gradients

#r: A1 pin Timers 2,5
#g: A2 pin Timers 2,5,9
#b: A3 pin Timers 2,5,9


def gradient(ri,gi,bi,rf,gf,bf,wait,cycles):
  """
  ri = initial,  percent
  rf = final,  percent m
  gradient(0,10,0,0,100,0,10,4)
  for inverting:
  gradient(20,255,255,95,255,255,10,2)
  """
  tim = Timer(2, freq=1000)
  cr = tim.channel(2, Timer.PWM_INVERTED, pin=r.pin)
  cg = tim.channel(3, Timer.PWM_INVERTED, pin=g.pin)
  cb = tim.channel(4, Timer.PWM_INVERTED, pin=b.pin)
  for i in range(cycles):
    for a in range(100):
      cr.pulse_width_percent((rf-ri)*0.01*a+ri)
      cg.pulse_width_percent((gf-gi)*0.01*a+gi)
      cb.pulse_width_percent((bf-bi)*0.01*a+gi)
      pyb.delay(wait)
    for a in range(100):
      cr.pulse_width_percent((rf-ri)*0.01*(100-a)+ri)
      cg.pulse_width_percent((gf-gi)*0.01*(100-a)+gi)
      cb.pulse_width_percent((bf-bi)*0.01*(100-a)+gi)
      pyb.delay(wait)

gradient(0,0,0,200,0,0,10,3)
gradient(0,0,50,100,0,200,10,3)
gradient(40,0,250,0,40,80,10,3)



r=Led(Pin.cpu.A1) 
g=Led(Pin.cpu.A2)
b=Led(Pin.cpu.A3)

adc = pyb.ADC(Pin.cpu.A4)
val = adc.read()
ADCMAX=4096
F=100
wait=10
tim = Timer(2, freq=1000)
cr = tim.channel(2, Timer.PWM_INVERTED, pin=r.pin)
cg = tim.channel(3, Timer.PWM_INVERTED, pin=g.pin)
cb = tim.channel(4, Timer.PWM_INVERTED, pin=b.pin)

################ Red color intensity by PWM 

while True:
  val = adc.read()
  width=int(F*val/ADCMAX)
  tim = Timer(2, freq=1000)
  cb = tim.channel(4, Timer.PWM_INVERTED, pin=b.pin)
  cb.pulse_width_percent(width)
  pyb.delay(wait)


############### R  B color variation 
while True:
  val = adc.read()
  wb=int(F*val/ADCMAX)
  wr=int(F*(-val/ADCMAX+1))
  cb.pulse_width_percent(wb)
  cr.pulse_width_percent(wr)
  pyb.delay(wait)

#######################  Attempt R G B color wheel
tim = Timer(2, freq=1000)
cr = tim.channel(2, Timer.PWM_INVERTED, pin=r.pin)
cg = tim.channel(3, Timer.PWM_INVERTED, pin=g.pin)
cb = tim.channel(4, Timer.PWM_INVERTED, pin=b.pin)
import math
bufb=[0]*100
bufg=[0]*100
bufr=[0]*100
for i in range(1,50):
  bufr[i] = 59 + int(40 * math.sin(2 * math.pi * i / 100))

for i in range(1,50):
  bufb[i+25] = 59 + int(40 * math.sin(2 * math.pi * i / 100))

for i in range(1,50):
  bufg[i+49] = 59 + int(40 * math.sin(2 * math.pi * i / 100))

while True:
  val = adc.read()
  percent=int(F*val/ADCMAX)
  cr.pulse_width_percent(bufr[percent])
  cg.pulse_width_percent(bufg[percent])
  print(bufg[percent])
  cb.pulse_width_percent(bufb[percent])
  pyb.delay(wait)




