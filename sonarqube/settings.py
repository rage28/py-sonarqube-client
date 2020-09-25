#!/usr/bin/env python
# -*- coding:utf-8 -*-
from .config import *


class SonarQubeSettings(object):
    def __init__(self, sonarqube):
        self.sonarqube = sonarqube

    def update_setting_value(self, component, key, value):
        params = {
            'component': component,
            'key': key,
            'value': value
        }
        self.sonarqube._make_call('post', API_SETTINGS_SET, **params)

    def list_settings_values(self, component, keys=None):
        params = {
            'component': component,
            'keys': keys
        }

        resp = self.sonarqube._make_call('get', API_SETTINGS_VALUES, **params)
        return resp.json()['settings']