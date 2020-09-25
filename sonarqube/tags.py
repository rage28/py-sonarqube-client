#!/usr/bin/env python
# -*- coding:utf-8 -*-
from .config import *


class SonarQubeTags(object):
    def __init__(self, sonarqube):
        self.sonarqube = sonarqube

    def get_all_tags(self, size, filter):
        """
        Get all the tags on the server.

        :param size: Page size. Must be greater than 0 and less or equal than 100.
        :param filter: Limit search to tags that contain the supplied string.
        :return: list of tags.
        """
        params = {
            'ps': size,
            'q': filter
        }
        resp = self.sonarqube._make_call('get', API_TAGS_GET, **params)
        resp_json = resp.json()

        return resp_json['tags']

    def set_tags(self, project_key, tags):
        """
        Update a user's password.

        :param project_key: Project key.
        :param tags: Comma-separated list of tags.
        """
        params = {
            'project': project_key,
            'tags': tags
        }
        self.sonarqube._make_call('post', API_TAGS_PROJECT_SET, **params)