import time
import board
import busio
import adafruit_mlx90640

PRINT_TEMPERATURES = True
PRINT_ASCIIART = False

i2c = busio.I2C(scl=board.GP17, sda=board.GP16, frequency=800000)

mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C")
print([hex(i) for i in mlx.serial_number])

mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

frame = [0] * 768
while True:
    stamp = time.monotonic()
    try:
        mlx.getFrame(frame)
    except ValueError:
        # these happen, no biggie - retry
        continue
    for h in range(24):
        max_temp = -273.15
        for w in range(32):
            t = frame[h * 32 + w]
            if PRINT_TEMPERATURES:
                max_temp = t if t > max_temp else max_temp
                # print("%0.1f, " % t, end="")
            if PRINT_ASCIIART:
                c = "&"
                # pylint: disable=multiple-statements
                if t < 20:
                    c = " "
                elif t < 23:
                    c = "."
                elif t < 25:
                    c = "-"
                elif t < 27:
                    c = "*"
                elif t < 29:
                    c = "+"
                elif t < 31:
                    c = "x"
                elif t < 33:
                    c = "%"
                elif t < 35:
                    c = "#"
                elif t < 37:
                    c = "X"
                # pylint: enable=multiple-statements
                print(c, end="")
    print("max temp is %0.1f, \n" % max_temp, end="")
