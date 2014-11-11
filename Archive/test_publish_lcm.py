import bemis100LCM
import lcm

frame = bemis100LCM.frame_t()
frame.n_pixels = 150
frame.red = [255] * frame.n_pixels
frame.green = [0] * frame.n_pixels
frame.blue = [0] * frame.n_pixels

lc = lcm.LCM()
lc.publish('BEMIS_100_DRAW', frame.encode())