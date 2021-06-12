import pyb, sensor, image, time, math
enable_lens_corr = False # turn on for straighter lines...
sensor.reset()
sensor.set_pixformat(sensor.RGB565) # grayscale is faster
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()

# All lines also have `x1()`, `y1()`, `x2()`, and `y2()` methods to get their end-points
# and a `line()` method to get all the above as one 4 value tuple for `draw_line()`.

uart = pyb.UART(3,9600,timeout_char=1000)
uart.init(9600,bits=8,parity = None, stop=1, timeout_char=1000)

while(True):
   clock.tick()
   img = sensor.snapshot()
   if enable_lens_corr: img.lens_corr(1.8) # for 2.8mm lens...

   # `merge_distance` controls the merging of nearby lines. At 0 (the default), no
   # merging is done. At 1, any line 1 pixel away from another is merged... and so
   # on as you increase this value. You may wish to merge lines as line segment
   # detection produces a lot of line segment results.

   # `max_theta_diff` controls the maximum amount of rotation difference between
   # any two lines about to be merged. The default setting allows for 15 degrees.
   is_line = 0
   for l in img.find_line_segments(merge_distance = 30, max_theta_diff = 45):
      if ((40 <= l.x1()) & (l.x1() <= 120) & (40 <= l.x2()) & (l.x2() <= 120)):
         # print("get line: (%d, %d)->(%d, %d)" %(l.x1(), l.y1(), l.x2(), l.y2()))
         img.draw_line(l.line(), color = (0, 255, 0))
         is_line = 1
      else:
         img.draw_line(l.line(), color = (255, 0, 0))

   if is_line == 1:
      uart.write("1 %d %d %d %d\r\n" % (l.x1(), l.y1(), l.x2(), l.y2())
   else:
      uart.write("0\r\n")

   print("FPS %f" % clock.fps())

