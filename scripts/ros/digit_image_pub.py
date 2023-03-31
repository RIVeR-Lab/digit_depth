#!/usr/bin/env python3

""" ROS RGB image publisher for DIGIT sensor """
import os
import rospkg
import yaml
from cv_bridge import CvBridge
from pathlib import Path
import rospy
from sensor_msgs.msg import CompressedImage
from digit_depth.digit.digit_sensor import DigitSensor


class ImageFeature:
    def __init__(self):
        self.image_pub = rospy.Publisher("/digit/rgb/image_raw/compressed",
                                         CompressedImage, queue_size=10)
        self.br = CvBridge()

def rgb_pub():
    ros_pack = rospkg.RosPack()
    # Read yaml data
    with open(os.path.join(ros_pack.get_path('digit_depth'),'config','digit.yaml')) as f:
        cfg = yaml.safe_load(f)

    digit_sensor = DigitSensor(cfg['sensor']['fps'], "QVGA", cfg['sensor']['serial_num'])
    ic = ImageFeature()
    rospy.init_node('image_feature', anonymous=True)
    digit_call = digit_sensor()
    br = CvBridge()
    while True:
        frame = digit_call.get_frame()
        msg = br.cv2_to_compressed_imgmsg(frame, "png")
        msg.header.stamp = rospy.Time.now()
        ic.image_pub.publish(msg)
        rospy.loginfo("Published image")


if __name__ == "__main__":
    rgb_pub()