import rclpy
from rclpy.node import Node
import Encoder

from std_msgs.msg import Int32

class WheelPublisher(Node):

    def __init__(self):
        super().__init__('my_droid')
        self.enc_r = Encoder.Encoder(24,23)
        self.enc_l = Encoder.Encoder(27,22)
        self.lwheel = self.create_publisher(Int32, 'lwheel', 10)
        self.rwheel = self.create_publisher(Int32, 'rwheel', 10)
        timer_period = 0.01
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        l = Int32()
        r = Int32()
        l.data = int(self.enc_l.read())
        r.data = int(self.enc_r.read())
        self.lwheel.publish(l)
        self.rwheel.publish(r)
        self.i += 1
        

def main(args=None):
    rclpy.init(args=args)
    my_droid = WheelPublisher()
    rclpy.spin(my_droid)
    my_droid.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
