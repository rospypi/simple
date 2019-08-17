import os

import rospy
import std_msgs.msg
import tf2_ros


def callback(msg):
    print(msg)


os.environ['ROS_MASTER_URI'] = 'http://localhost:11311'
os.environ['ROS_PYTHON_LOG_CONFIG_FILE'] = '|'  # specify dummy file
rospy.init_node("hoge")
rospy.loginfo('start')
sub = rospy.Subscriber("sub", std_msgs.msg.String, callback)
pub = rospy.Publisher('pub', std_msgs.msg.Int16, queue_size=10)
tf_buffer = tf2_ros.Buffer()
listener = tf2_ros.TransformListener(tf_buffer)
rate = rospy.Rate(1)
while not rospy.is_shutdown():
    pub.publish(3)
    try:
        # run this command in another termninal beforehand
        # > rosrun tf static_transform_publisher 0 1 2 0 0 0 1 map odom 1000
        t = tf_buffer.lookup_transform('map', 'odom', rospy.Time())
        print(t)
    except (tf2_ros.LookupException,
            tf2_ros.ConnectivityException,
            tf2_ros.ExtrapolationException) as e:
        pass
    rate.sleep()
