#!/usr/bin/python
# coding=utf-8

import diamond.collector
import re
import sys
import os
NAME = os.path.dirname(__file__)
OPSTOOLS = os.path.abspath(NAME)
sys.path.append(OPSTOOLS)

from getMessage import getMessage

class LogCollector(diamond.collector.Collector):
    def get_default_config_help(self):
        config_help = super(LogCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(LogCollector, self).get_default_config()
        config.update({
            'path':'LogCollector',
            'access_log_path':'www.xxx.com'
        })
        return config

    def collect(self):
        """
        Overrides the Collector.collect method
        """
        for k, v in getMessage().items():
            # Set Metric Name
            metric_name = k 
            # Set Metric Value
            metric_value = v

            # Publish Metric
            self.publish(metric_name, metric_value)
