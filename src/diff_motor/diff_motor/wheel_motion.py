import rclpy
from rclpy.node import Node
import RPi.GPIO as GPIO

from std_msgs.msg import Float32, Int32

class WheelMotion(Node):

    def __init__(self):
        super().__init__("wheel_motion")
        self.nodename = "wheel_motion"
        self.get_logger().info(f"{self.nodename} started")
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        # Left wheel
        GPIO.setup(13, GPIO.OUT)
        GPIO.setup(19, GPIO.OUT)
        self.ma_left_pwm = GPIO.PWM(13, 1000)
        self.mb_left_pwm = GPIO.PWM(19, 1000)
        self.ma_left_pwm.start(0)
        self.mb_left_pwm.start(0)

        # Right wheel
        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)
        self.ma_right_pwm = GPIO.PWM(12, 1000)
        self.mb_right_pwm = GPIO.PWM(18, 1000)
        self.ma_right_pwm.start(0)
        self.mb_right_pwm.start(0)

        #### subscribers/publishers
        self.create_subscription(Float32, 'rwheel_vtarget', self.target_rwheel_callback, 10)
        self.create_subscription(Float32, 'lwheel_vtarget', self.target_lwheel_callback, 10)
        self.create_subscription(Int32, 'rwheel', self.rwheel_callback, 10)
        self.create_subscription(Int32, 'lwheel', self.lwheel_callback, 10)

    def target_rwheel_callback(self, msg):
        speed = msg.data
        if speed > 0:
            self.ma_right_pwm.ChangeDutyCycle(0)
            self.mb_right_pwm.ChangeDutyCycle(speed * 100)
        if speed < 0:
            self.ma_right_pwm.ChangeDutyCycle(speed * 100 * -1)
            self.mb_right_pwm.ChangeDutyCycle(0)
        if speed == 0:
            self.ma_right_pwm.ChangeDutyCycle(0)
            self.mb_right_pwm.ChangeDutyCycle(0)

    def target_lwheel_callback(self, msg):
        speed = msg.data
        if speed > 0:
            self.ma_left_pwm.ChangeDutyCycle(0)
            self.mb_left_pwm.ChangeDutyCycle(speed * 100)
        if speed < 0:
            self.ma_left_pwm.ChangeDutyCycle(speed * 100 * -1)
            self.mb_left_pwm.ChangeDutyCycle(0)
        if speed == 0:
            self.ma_left_pwm.ChangeDutyCycle(0)
            self.mb_left_pwm.ChangeDutyCycle(0)

    def rwheel_callback(self, msg):
        x = 1

    def lwheel_callback(self, msg):
        x = 1


def main(args=None):
    rclpy.init(args=args)
    try:
        wheel_motion = WheelMotion()
        rclpy.spin(wheel_motion)
    except rclpy.exceptions.ROSInterruptException:
        pass

    wheel_motion.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
        

