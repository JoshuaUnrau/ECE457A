from __future__ import print_function

import sys
import rospy
from beginner_tutorials.srv import *

def setPoseClient(x, y):
	rospy.wait_for_service('/turtlesim/updateTargetPose')
	try:
		add_two_ints = rospy.ServiceProxy('/turtlesim/updateTargetPose', AddTwoInts)
		resp1 = add_two_ints(x, y)
		return resp1
	except rospy.ServiceException as e:
		print("Service call failed: %s"%e)

def usage():
	return "%s [x y]"%sys.argv[0]

if __name__ == "__main__":
	if len(sys.argv) == 3:
		x = int(sys.argv[1])
		y = int(sys.argv[2])
	else:
		print(usage())
		sys.exit(1)
	print("Requesting set pose (%s, %s)"%(x, y))
	print("%s + %s = %s"%(x, y, setPoseClient(x, y)))