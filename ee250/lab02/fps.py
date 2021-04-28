""" EE 250L Final Project

List team members here.

Insert Github repository link here.
git@github.com:usc-ee250-spring2021/lab02-ArbitaryMouse.git
"""

"""python3 interpreters in Ubuntu (and other linux distros) will look in a 
default set of directories for modules when a program tries to `import` one. 
Examples of some default directories are (but not limited to):
  /usr/lib/python3.5
  /usr/local/lib/python3.5/dist-packages

The `sys` module, however, is a builtin that is written in and compiled in C for
performance. Because of this, you will not find this in the default directories.
"""
import sys
import time
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('../../Software/Python/')
# This append is to support importing the LCD library.
sys.path.append('../../Software/Python/grove_i2c_temp_hum_sensor_mini')

import grovepi
import grove_i2c_temp_hum_mini
import time
import threading
lock = threading.Lock()

def protect(fn):
    def safefn(*arg,**kwarg):
        with lock:
            return fn(*arg,**kwarg)
        return safefn

grovepi.read_i2c_block = protect(grovepi.read_i2c_block)
grovepi.write_i2c_block = protect(grovepi.write_i2c_block)

#patch grove_rgb_lcd
for x in dir(grove_i2c_temp_hum_sensor_mini.bus):
    if '12c' in x or 'read' in x or 'write' in x:
        print('patching->',x)
        fn = grove_i2c_temp_hum_sensor_mini.bus.__getattribute__(x)
        grove_i2c_temp_hum_sensor_mini.bus.__setattr__(x,protect(fn))

"""This if-statement checks if you are running this python file directly. That 
is, if you run `python3 grovepi_sensors.py` in terminal, this if-statement will 
be true"""
t= grove_i2c_temp_hum_mini.th02()
if __name__ == '__main__':
    PORT = 4    # D4
    PORTR = 0
    PORTW = 1
    ldis = -1
    lsen = -1
    while True:
        #So we do not poll the sensors too quickly which may introduce noise,
        #sleep for a reasonable time of 200ms between each iteration.
        time.sleep(0.4)
        try:
                temp = t.getTemperature()
                humid = t.getHumidity()
        except TypeError:
                print ("Error")
        time.sleep(0.1)
        setText(" " + str(temp) + "cm \n " + str(humid) + "cm")
        setRGB(0,255,0)
        buf=list("Grove -Update without erase")
        setText("".join(buf))
        for i in range(len(buf)):
                buf[i]="."
                setText_norefresh("".join(buf))
                time.sleep(.1)
