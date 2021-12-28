from setuptools import setup

package_name = 'diff_motor'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu',
    maintainer_email='darren.poulson@gmail.com',
    description='TODO: Control two motors for a diff_drive',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'diff_wheels = diff_motor.wheel_publisher:main',
            'diff_motion = diff_motor.wheel_motion:main',
            'diff_velocity = diff_motor.wheel_velocity:main',
            'diff_odom = diff_motor.diff_tf:main'
        ],
    },
)
