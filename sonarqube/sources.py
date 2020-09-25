#!/usr/bin/env python
# -*- coding:utf-8 -*-
from .config import *


class SonarQubeSources(object):
    def __init__(self, sonarqube):
        self.sonarqube = sonarqube

    def get_sources_scm(self, file_key, from_line, to_line, commits_by_line='false'):
        """
        Get SCM information of source files. Require See Source Code permission on file's project
        :param file_key:
        :param from_line:
        :param to_line:
        :param commits_by_line:
        :return:
        """
        params = {
            'key': file_key,
            'from': from_line,
            'to': to_line,
            'commits_by_line': commits_by_line
        }
        resp = self.sonarqube._make_call('get', API_SOURCES_SCM, **params)
        return resp.json()['scm']

    def get_sources_show(self, file_key, from_line, to_line):
        params = {
            'key': file_key,
            'from': from_line,
            'to': to_line
        }
        resp = self.sonarqube._make_call('get', API_SOURCES_SHOW, **params)
        return resp.json()['sources']

    def get_sources_raw(self, file_key):
        params = {
            'key': file_key
        }
        resp = self.sonarqube._make_call('get', API_SOURCES_RAW, **params)
        return resp.text
