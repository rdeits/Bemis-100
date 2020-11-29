using PiGPIO
using PiGPIO: spi_open, spi_write

pi = Pi()
spi = spi_open(pi, 0, 4000000)

num_pixels = 1
header = zeros(UInt8, 4)
trailer_size = num_pixels ÷ 16
if num_pixels % 16 == 0
    trailer_size += 1
end
trailer = fill(0xff, trailer_size)

buffer = vcat(header,
              [0x80, 0xff, 0x00, 0x00],
              trailer)
spi_write(pi, 0, buffer)
