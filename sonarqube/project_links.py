#!/usr/bin/env python
# -*- coding:utf-8 -*-
from .config import *


class SonarQubeProject_Links(object):
    def __init__(self, sonarqube):
        self.sonarqube = sonarqube

    def create_project_links(self, projectKey, name, url):
        """
        Create a new project link.
        :param projectKey:
        :param name:
        :param url:
        :return:
        """
        params = {
            'projectKey': projectKey,
            'name': name,
            'url': url
        }
        self.sonarqube._make_call('post', API_PROJECT_LINKS_CREATE, **params)

    def delete_project_links(self, id):
        """
        Delete existing project link.
        :param id:
        :return:
        """
        params = {
            'id': id
        }
        self.sonarqube._make_call('post', API_PROJECT_LINKS_DELETE, **params)

    def search_project_links(self, projectKey):
        """
        List links of a project.
        :param projectKey:
        :return:
        """
        params = {
            'projectKey': projectKey
        }
        resp = self.sonarqube._make_call('get', API_PROJECT_LINKS_SEARCH, **params)
        data = resp.json()
        return data["links"]
