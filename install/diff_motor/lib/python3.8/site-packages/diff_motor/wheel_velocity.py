import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_msgs.msg import Float32

class WheelVelocity(Node):

    def __init__(self):
        super().__init__('wheel_velocity')
        self.nodename = "wheel_velocity" 
        self.get_logger().info("%s started" % self.nodename)

        self.w = self.declare_parameter("base_width", 0.2).value
        self.dx = 0
        self.dr = 0
        self.ticks_since_target = 0

        self.pub_lmotor = self.create_publisher(Float32, 'lwheel_vtarget', 10)
        self.pub_rmotor = self.create_publisher(Float32, 'rwheel_vtarget', 10)
        self.create_subscription(Twist, 'cmd_vel', self.twist_callback, 10)

        self.rate_hz = self.declare_parameter("rate_hz", 50).value

        self.create_timer(1.0/self.rate_hz, self.calculate_left_and_right_target)

    def calculate_left_and_right_target(self):
        # dx = (l + r) / 2
        # dr = (r - l) / w

        right = Float32()
        left = Float32()
        
        right.data = 1.0 * self.dx + self.dr * self.w / 2.0
        left.data = 1.0 * self.dx - self.dr * self.w / 2.0
        
        self.pub_lmotor.publish(left)
        self.pub_rmotor.publish(right)

        self.ticks_since_target += 1

    def twist_callback(self, msg):
        self.ticks_since_target = 0
        self.dx = msg.linear.x
        self.dr = msg.angular.z


def main(args=None):
    rclpy.init(args=args)
    try:
        wheel_velocity = WheelVelocity()
        rclpy.spin(wheel_velocity)
    except rclpy.exceptions.ROSInterruptException:
        pass

    wheel_velocity.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


