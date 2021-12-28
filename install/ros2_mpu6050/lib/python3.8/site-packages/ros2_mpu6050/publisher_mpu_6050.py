import smbus
from time import sleep
import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3
from std_msgs.msg import Bool, Empty

from MPU6050 import MPU6050

i2c_bus = 1
device_address = 0x68
# The offsets are different for each device and should be changed
# accordingly using a calibration procedure
x_accel_offset = -5489
y_accel_offset = -1441
z_accel_offset = 1305
x_gyro_offset = -2
y_gyro_offset = -72
z_gyro_offset = -5
enable_debug_output = True

class MPU6050Publisher(Node):

    def __init__(self):
        super().__init__('mpu6050_publisher')
        self.imu_publisher_ = self.create_publisher(Imu, '/mpu6050', 10)
        self.imu_timer_ = self.create_timer(0.1, self.publish_imu)
        self.frame_id = "base_imu"
        self.mpu = MPU6050.MPU6050(i2c_bus, device_address, x_accel_offset, y_accel_offset,
              z_accel_offset, x_gyro_offset, y_gyro_offset, z_gyro_offset,
              enable_debug_output)
        self.mpu.dmp_initialize()
        self.mpu.set_DMP_enabled(True)
        self.mpu_int_status = self.mpu.get_int_status()
        print(hex(self.mpu_int_status))

        self.packet_size = self.mpu.DMP_get_FIFO_packet_size()
        print(self.packet_size)
        self.FIFO_count = self.mpu.get_FIFO_count()
        print(self.FIFO_count)

        self.FIFO_buffer = [0]*64

        self.FIFO_count_list = list()


    def publish_imu(self):
        self.FIFO_count = self.mpu.get_FIFO_count() 

        self.mpu_int_status = self.mpu.get_int_status()

        if (self.FIFO_count == 1024) or (self.mpu_int_status & 0x10):
            self.mpu.reset_FIFO()
            self.get_logger().error('Overflow')
        elif (self.mpu_int_status & 0x02):
            while self.FIFO_count < self.packet_size:
                self.FIFO_count = self.mpu.get_FIFO_count()
            self.FIFO_buffer = self.mpu.get_FIFO_bytes(self.packet_size)
            accel = self.mpu.DMP_get_acceleration_int16(self.FIFO_buffer)
            quat = self.mpu.DMP_get_quaternion_int16(self.FIFO_buffer)
            grav = self.mpu.DMP_get_gravity(quat)
            lin_accel = self.mpu.DMP_get_linear_accel(accel, grav)

            roll_pitch_yaw = self.mpu.DMP_get_euler_roll_pitch_yaw(quat, grav)


            msg = Imu()
            imu_euler_msg = Vector3()
            mag_msg = Vector3()

            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = self.frame_id
            msg.linear_acceleration.x = lin_accel.x
            msg.linear_acceleration.y = lin_accel.y
            msg.linear_acceleration.z = lin_accel.z

            msg.orientation.x = float(quat.x)
            msg.orientation.y = float(quat.y)
            msg.orientation.z = float(quat.z)
            msg.orientation.w = float(quat.w)

            msg.angular_velocity.x = roll_pitch_yaw.x
            msg.angular_velocity.y = roll_pitch_yaw.y
            msg.angular_velocity.z = roll_pitch_yaw.z

            
            self.imu_publisher_.publish(msg)

            self.get_logger().info('Gyro Data: "%s"' % roll_pitch_yaw.x)



def main(args=None):
    rclpy.init(args=args)

    mpu6050_publisher = MPU6050Publisher()

    rclpy.spin(mpu6050_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    mpu6050_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
