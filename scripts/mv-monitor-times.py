# Search-replaces monitor time windows.
#
# python mv-monitor-times.py <accessId> <accessKey> <oldWindow> <newWindow>

import sys

from sumologic import SumoLogic

args = sys.argv
sumo = SumoLogic(args[1], args[2])
oldWindow = args[3]
newWindow = args[4]

ds = sumo.dashboards()
