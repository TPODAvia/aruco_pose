#!/usr/bin/env python3

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class DepthImageProcessor:
    def __init__(self):
        # Initialize ROS node
        rospy.init_node('depth_image_processor', anonymous=True)

        # Initialize CV bridge
        self.bridge = CvBridge()

        # Subscribe to the depth image topic
        self.image_sub = rospy.Subscriber('/camera/depth_mod/image_raw', Image, self.image_callback, tcp_nodelay=True)

        # Publisher for the modified image
        self.image_pub = rospy.Publisher('/camera/depth_mod/depth_moddepth_mod', Image, queue_size=10, tcp_nodelay=True)

    def image_callback(self, msg):
        try:
            # Convert ROS Image message to OpenCV image
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")

            # Multiply every pixel by 1.1
            processed_image = cv_image * 1.02

            # Convert back to uint16 if necessary (assuming depth images are uint16)
            processed_image = processed_image.astype(cv_image.dtype)

            # Convert OpenCV image back to ROS Image message
            image_message = self.bridge.cv2_to_imgmsg(processed_image, encoding="passthrough")
            image_message.header.seq = msg.header.seq
            image_message.header.stamp.secs = msg.header.stamp.secs
            image_message.header.stamp.nsecs = msg.header.stamp.nsecs
            image_message.header.frame_id = "oak_rgb_camera_optical_frame"
            # Publish the processed image
            self.image_pub.publish(image_message)

        except CvBridgeError as e:
            rospy.logerr(f"Failed to convert image: {e}")

if __name__ == '__main__':
    try:
        # Create an instance of the DepthImageProcessor class
        depth_image_processor = DepthImageProcessor()

        # Spin to keep the script running
        rospy.spin()

    except rospy.ROSInterruptException:
        pass