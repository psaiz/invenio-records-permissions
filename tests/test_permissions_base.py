# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
# Copyright (C) 2019 Northwestern University.
#
# Invenio-Records-Permissions is free software; you can redistribute it
# and/or modify it under the terms of the MIT License; see LICENSE file for
# more details.

from elasticsearch_dsl import Q
from invenio_access.permissions import any_user

from invenio_records_permissions.generators import AnyUser, Deny
from invenio_records_permissions.policies import BasePermissionPolicy


class TestPermissionPolicy(BasePermissionPolicy):
    can_create = [AnyUser()]
    can_list = [AnyUser()]
    can_read = [AnyUser()]
    can_foo_bar = [AnyUser()]


def test_base_permission_policy(app):
    policy = BasePermissionPolicy

    for action in ['list', 'read', 'update', 'delete', 'random']:
        generators = policy(action=action).generators

        assert len(generators) == 0


def test_custom_permission_policy(app):
    policy = TestPermissionPolicy

    assert isinstance(policy(action='create').generators[0], AnyUser)
    assert isinstance(policy(action='list').generators[0], AnyUser)
    assert isinstance(policy(action='read').generators[0], AnyUser)
    assert isinstance(policy(action='foo_bar').generators[0], AnyUser)
    assert len(policy(action='update').generators) == 0
    assert len(policy(action='delete').generators) == 0
    assert len(policy(action='random').generators) == 0


def test_base_permission(superuser_role_need):
    create_perm = TestPermissionPolicy(action='create')
    list_perm = TestPermissionPolicy(action='list')
    read_perm = TestPermissionPolicy(action='read')
    update_perm = TestPermissionPolicy(action='update')
    delete_perm = TestPermissionPolicy(action='delete')
    foo_bar_perm = TestPermissionPolicy(action='foo_bar')

    assert create_perm.needs == {superuser_role_need, any_user}
    assert create_perm.excludes == set()

    assert list_perm.needs == {superuser_role_need, any_user}
    assert list_perm.excludes == set()

    assert read_perm.needs == {superuser_role_need, any_user}
    assert read_perm.excludes == set()
    assert read_perm.query_filters == [Q('match_all')]

    assert update_perm.needs == {superuser_role_need}
    # TODO: Reinstate {any_user} when default Deny() implemented. See #10
    assert update_perm.excludes == set()

    assert delete_perm.needs == {superuser_role_need}
    # TODO: Reinstate {any_user} when default Deny() implemented. See #10
    assert delete_perm.excludes == set()

    assert foo_bar_perm.needs == {superuser_role_need, any_user}
    assert foo_bar_perm.excludes == set()
