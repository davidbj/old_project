#!/usr/bin/python

import sys
from os import path
NAME = path.dirname(__file__)
OPSTOOLS = path.abspath(NAME)
sys.path.append(OPSTOOLS)


from log import checkMessage
import diamond.collector
import time

class HttpdCodeCollector(diamond.collector.Collector):
    def collect(self):
        for k, v in checkMessage().items():
            metric_name = k
            metric_value = v
            self.publish(metric_name, metric_value)
