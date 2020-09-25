#!/usr/bin/env python
# -*- coding:utf-8 -*-
from .config import *


class SonarQubePermissions(object):
    def __init__(self, sonarqube):
        self.sonarqube = sonarqube

    def project_permissions_add_group(self, project_key, group_name, permissions):
        """
        Add permission to a group.

        :param project_key: Project key
        :param group_name: Group name or 'anyone' (case insensitive)
        :param permissions: Permission. Possible values for project permissions admin, codeviewer, issueadmin,
                            securityhotspotadmin, scan, user
        """
        params = {
            'groupName': group_name,
            'projectKey': project_key
        }
        if isinstance(permissions, list):
            for perm in permissions:
                params['permission'] = perm
                self.sonarqube._make_call('post', API_PERMISSIONS_ADD_GROUP, **params)
        elif isinstance(permissions, str):
            params['permission'] = permissions
            self.sonarqube._make_call('post', API_PERMISSIONS_ADD_GROUP, **params)

    def project_permissions_remove_group(self, project_key, group_name, permissions):
        """
        Remove a permission from a group.

        :param project_key:
        :param group_name:
        :param permissions:
        :return:
        """
        params = {
            'groupName': group_name,
            'projectKey': project_key
        }
        if isinstance(permissions, list):
            for perm in permissions:
                params['permission'] = perm
                self.sonarqube._make_call('post', API_PERMISSIONS_REMOVE_GROUP, **params)
        elif isinstance(permissions, str):
            params['permission'] = permissions
            self.sonarqube._make_call('post', API_PERMISSIONS_REMOVE_GROUP, **params)

    def project_permissions_get_users(self, project_key, organization='default-organization', permission='scan',
                                      filter=None):
        """
        Get all the users in a given project with the specified permission

        :param project_key:
        :param organization:
        :param permission:
        :param filter
        :return:
        """
        params = {
            'projectKey': project_key
        }
        page_num = 1
        page_size = 1
        total = 2

        if permission is not None:
            params['permission'] = permission

        if organization is not None:
            params['organization'] = organization

        if filter is not None:
            params['q'] = filter

        while page_num * page_size < total:
            resp = self.sonarqube._make_call('get', API_PERMISSIONS_GET_USERS, **params)
            response = resp.json()

            page_num = response['paging']['pageIndex']
            page_size = response['paging']['pageSize']
            total = response['paging']['total']

            params['p'] = page_num + 1

            for user in response['users']:
                yield user

    def project_permissions_add_user(self, project_key, login, permissions):
        """
        Add permission to a user.

        :param project_key:
        :param login:
        :param permissions:
        :return:
        """
        params = {
            'login': login,
            'projectKey': project_key
        }
        if isinstance(permissions, list):
            for perm in permissions:
                params['permission'] = perm
                self.sonarqube._make_call('post', API_PERMISSIONS_ADD_USER, **params)
        elif isinstance(permissions, str):
            params['permission'] = permissions
            self.sonarqube._make_call('post', API_PERMISSIONS_ADD_USER, **params)

    def project_permissions_remove_user(self, project_key, login, permissions):
        """
        Remove permission from a user.

        :param project_key:
        :param login:
        :param permissions:
        :return:
        """
        params = {
            'login': login,
            'projectKey': project_key
        }
        if isinstance(permissions, list):
            for perm in permissions:
                params['permission'] = perm
                self.sonarqube._make_call('post', API_PERMISSIONS_REMOVE_USER, **params)
        elif isinstance(permissions, str):
            params['permission'] = permissions
            self.sonarqube._make_call('post', API_PERMISSIONS_REMOVE_USER, **params)

    def apply_template_to_project(self, project_key, template_id):
        """
        Apply a permission template to one project.

        :param project_key:
        :param template_id:
        :return:
        """
        params = {
            'projectKey': project_key,
            'templateId': template_id
        }
        self.sonarqube._make_call('post', API_PERMISSIONS_APPLY_TEMPLATE, **params)
