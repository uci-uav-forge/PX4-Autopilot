#!/usr/bin/env python2

from __future__ import division

PKG = 'px4'

import rospy
import glob
import json
import math
import os
from px4tools import ulog
import sys
from mavros import mavlink
from mavros_msgs.msg import Mavlink, Waypoint, WaypointReached
from sensor_msgs.msg import NavSatFix
from mavros_test_common import MavrosTestCommon
from pymavlink import mavutil
from six.moves import xrange
from threading import Thread



def current_global_position_callback(self, data):
    self.current_global_position = (data.latitude, data.longitude, data.altitude)


class LocationTest(MavrosTestCommon):
    """
    Run a mission
    """

    def setUp(self):
        super(self.__class__, self).setUp()

        self.mavlink_pub = rospy.Publisher('mavlink/to', Mavlink, queue_size=1)
        # mission_item_reached_sub will act as the object that reacts to Subscriber 'mavros/mission/reached'
        self.current_global_position = None
        self.current_global_position_sub = rospy.Subscriber(
            'mavros/global_position/global', NavSatFix,
            self.current_global_position_callback)

        # Wait for global position. Else, we run risk of running locally with extraneous coordinates
        # Is while(1) the best solution?
        while(1):
            if(self.current_global_position != None):
                break;

        rospy.loginfo(self.current_global_position)




if __name__ == '__main__':
    import rostest
    rospy.init_node('location_test_node', anonymous=True)

    name = "location_test"
    rostest.rosrun(PKG, name, LocationTest)
