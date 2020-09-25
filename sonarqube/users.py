#!/usr/bin/env python
# -*- coding:utf-8 -*-
from .config import *


class SonarQubeUser(object):
    def __init__(self, sonarqube):
        self.sonarqube = sonarqube
        self._data = None

    def poll(self):
        self._data = self.search_users()

    def iterkeys(self):
        for item in self:
            yield item['login']

    def keys(self):
        return list(self.iterkeys())

    def __len__(self):
        return len(self.keys())

    def __contains__(self, login_name):
        result = self.search_users(filter=login_name)
        logins = [item['login'] for item in result]
        return login_name in logins

    def __getitem__(self, index):
        return list(self)[index]

    def __iter__(self):
        self.poll()
        return self._data

    def search_users(self, filter=None):
        """
        Get a list of active users.

        :param filter:
        :return:
        """
        params = {}
        page_num = 1
        page_size = 1
        total = 2

        if filter is not None:
            params['q'] = filter

        while page_num * page_size < total:
            resp = self.sonarqube._make_call('get', API_USERS_SEARCH, **params)
            response = resp.json()

            page_num = response['paging']['pageIndex']
            page_size = response['paging']['pageSize']
            total = response['paging']['total']

            params['p'] = page_num + 1

            for user in response['users']:
                yield user

    def create_user(self, login, name, email, password=None, local='true', scm=None):
        """
        Create a user.

        :param login:
        :param name:
        :param email:
        :param password:
        :param local:
        :param scm:
        :return:
        """
        params = {
            'login': login,
            'name': name,
            'email': email,
            'local': local
        }
        if local == 'true' and password:
            params['password'] = password

        if scm:
            params['scmAccount'] = scm

        self.sonarqube._make_call('post', API_USERS_CREATE, **params)

    def update_user(self, login, name, email, scm=None):
        """
        Update a user.

        :param login:
        :param name:
        :param email:
        :param scm:
        :return:
        """
        params = {
            'login': login,
            'name': name,
            'email': email,
        }
        if scm:
            params['scmAccount'] = scm

        self.sonarqube._make_call('post', API_USERS_UPDATE, **params)

    def change_user_password(self, login, newPassword, previousPassword=None):
        """
        Update a user's password.
        :param login:
        :param newPassword:
        :param previousPassword:
        :return:
        """
        params = {
            'login': login,
            'password': newPassword
        }
        if previousPassword:
            params['previousPassword'] = previousPassword

        self.sonarqube._make_call('post', API_USERS_CHANGE_PASSWORD, **params)

    def deactivate_user(self, login):
        """
        Deactivate a user.

        :param login:
        :return:
        """
        params = {
            'login': login
        }
        self.sonarqube._make_call('post', API_USERS_DEACTIVATE, **params)

    def get_user_belong_to_groups(self, login):
        """
        Lists the groups a user belongs to.

        :param login:
        :return:
        """
        params = {
            'login': login
        }
        resp = self.sonarqube._make_call('get', API_USERS_GROUPS, **params)
        response = resp.json()
        groups_info = response['groups']
        groups = [g['name'] for g in groups_info]
        return groups
