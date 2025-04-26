#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import sys
import termios
import tty

# Hàm đọc phím nhấn không cần enter
def getKey():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key

def main():
    rospy.init_node('keyboard_control')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)

    msg = """
Điều khiển robot bằng bàn phím:
  W/S: Tiến/Lùi
  A/D: Quay trái/Quay phải
  Q: Thoát
"""
    print(msg)

    twist = Twist()
    while not rospy.is_shutdown():
        key = getKey()
        if key == 'w':
            twist.linear.x = 0.02
            twist.angular.z = 0.0
        elif key == 's':
            twist.linear.x = -0.02
            twist.angular.z = 0.0
        elif key == 'a':
            twist.linear.x = 0.0
            twist.angular.z = 0.08
        elif key == 'd':
            twist.linear.x = 0.0
            twist.angular.z = -0.08
        elif key == 'q':
            print("Thoát...")
            break
        else:
            twist.linear.x = 0.0
            twist.angular.z = 0.0

        pub.publish(twist)
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
