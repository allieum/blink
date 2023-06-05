import array
from ola.ClientWrapper import ClientWrapper


class Light:
    data = array.array('B', [0] * 119)
    start_channel = 12
    brightness = 30

    def __init__(self, i):
        self.i = i
        self.start_index = self.start_channel - 1 + self.i * 6
        self.set_brightness(self.brightness)

    def set(self, color):
        for j, value in enumerate(color):
            print(f"setting data[{self.start_index + j}] to {value}")
            self.data[self.start_index + j] = value


    @staticmethod
    def all_off():
        Light.data[Light.start_channel - 1:] = array.array('B', [0] * (119 - (Light.start_channel - 1)))

    @staticmethod
    def set_brightness(level):
       Light.data[0] = level

    @staticmethod
    def send_frame(wrapper):
        wrapper.Client().SendDmx(0, Light.data, DmxSent)


lights = [Light(i) for i in range(18)]

wrapper = None
loop_count = 0
TICK_INTERVAL = 100 # in ms

def DmxSent(state):
  if not state.Succeeded():
    wrapper.Stop()

def SendDMXFrame():
  # schdule a function call in 100ms
  # we do this first in case the frame computation takes a long time.
  wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)

  # compute frame here
  global loop_count
  print(f"sending frame {loop_count}")
  value = loop_count % 256
  # for light in lights:
  Light.all_off()
  color = 255, 0, 127, 0, 234, 126
  color = 0, 255, 0, 0, 127, 255
  lights[loop_count % 18].set(color)
  lights[(loop_count - 1) % 18].set(map(lambda x: x // 2, color))
  lights[(loop_count - 2) % 18].set(map(lambda x: x // 4, color))
  lights[(loop_count - 3) % 18].set(map(lambda x: x // 6, color))
  lights[(loop_count - 4) % 18].set(map(lambda x: x // 8, color))
  loop_count += 1

  # send
  Light.send_frame(wrapper)

wrapper = ClientWrapper()
wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)
wrapper.Run()

