import pyb, sensor, image, time, math

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()

f_x = (2.8 / 3.984) * 160 # find_apriltags defaults to this if not set
f_y = (2.8 / 2.952) * 120 # find_apriltags defaults to this if not set
c_x = 160 * 0.5 # find_apriltags defaults to this if not set (the image.w * 0.5)
c_y = 120 * 0.5 # find_apriltags defaults to this if not set (the image.h * 0.5)

def degrees(radians):
   return (180 * radians) / math.pi

uart = pyb.UART(3,9600,timeout_char=1000)
uart.init(9600,bits=8,parity = None, stop=1, timeout_char=1000)

while(True):
   clock.tick()
   img = sensor.snapshot()
   for tag in img.find_apriltags(fx=f_x, fy=f_y, cx=c_x, cy=c_y): # defaults to TAG36H11
      img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
      '''
      if ((degrees(tag.y_rotation()) <= 5) | (degrees(tag.y_rotation()) >= 355)):
         img.draw_rectangle(tag.rect(), color = (255, 0, 0))
         img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
         uart.write(("a\n").encode())
         print("a\n")
      else:
         img.draw_rectangle(tag.rect(), color = (0, 0, 255))
         img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
         if (degrees(tag.y_rotation()) <= 180):
            uart.write(("l\n").encode())
            print("l\n")
         elif (degrees(tag.y_rotation()) > 180):
            uart.write(("r\n").encode())
            print("r\n")

      #print_args = (degrees(tag.x_rotation()), degrees(tag.y_rotation()), degrees(tag.z_rotation()))
      #print ("Rx %f, Ry %f, Rz %f" % print_args)
      '''
      if (tag.cx() < 50):
         img.draw_rectangle(tag.rect(), color = (0, 100, 255))
         uart.write(("d").encode())
         print("%d d" % tag.cx())
      elif (tag.cx() > 110):
         img.draw_rectangle(tag.rect(), color = (0, 100, 255))
         uart.write(("a").encode())
         print("%d a" % tag.cx())
      else:
         img.draw_rectangle(tag.rect(), color = (255, 0, 0))
         uart.write(("w").encode())
         print("%d w" % tag.cx())
      time.sleep(0.3)
