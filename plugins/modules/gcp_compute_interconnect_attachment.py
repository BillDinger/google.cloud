#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Google
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# ----------------------------------------------------------------------------
#
#     ***     AUTO GENERATED CODE    ***    AUTO GENERATED CODE     ***
#
# ----------------------------------------------------------------------------
#
#     This file is automatically generated by Magic Modules and manual
#     changes will be clobbered when the file is regenerated.
#
#     Please read more about how to change this file at
#     https://www.github.com/GoogleCloudPlatform/magic-modules
#
# ----------------------------------------------------------------------------

from __future__ import absolute_import, division, print_function
__metaclass__ = type

################################################################################
# Documentation
################################################################################

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ["preview"],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: gcp_compute_interconnect_attachment
description:
- Represents an InterconnectAttachment (VLAN attachment) resource. For more information,
  see Creating VLAN Attachments.
short_description: Creates a GCP InterconnectAttachment
version_added: 2.8
author: Google Inc. (@googlecloudplatform)
requirements:
- python >= 2.6
- requests >= 2.18.4
- google-auth >= 1.3.0
options:
  state:
    description:
    - Whether the given object should exist in GCP
    choices:
    - present
    - absent
    default: present
  interconnect:
    description:
    - URL of the underlying Interconnect object that this attachment's traffic will
      traverse through.
    required: true
  description:
    description:
    - An optional description of this resource. .
    required: false
  router:
    description:
    - URL of the cloud router to be used for dynamic routing. This router must be
      in the same region as this InterconnectAttachment. The InterconnectAttachment
      will automatically connect the Interconnect to the network & region within which
      the Cloud Router is configured.
    - 'This field represents a link to a Router resource in GCP. It can be specified
      in two ways. You can add `register: name-of-resource` to a gcp_compute_router
      task and then set this router field to "{{ name-of-resource }}" Alternatively,
      you can set this router to a dictionary with the selfLink key where the value
      is the selfLink of your Router'
    required: true
  name:
    description:
    - Name of the resource. Provided by the client when the resource is created. The
      name must be 1-63 characters long, and comply with RFC1035. Specifically, the
      name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?`
      which means the first character must be a lowercase letter, and all following
      characters must be a dash, lowercase letter, or digit, except the last character,
      which cannot be a dash.
    required: true
  region:
    description:
    - Region where the regional interconnect attachment resides.
    required: true
extends_documentation_fragment: gcp
'''

EXAMPLES = '''
- name: create a interconnect attachment
  gcp_compute_interconnect_attachment:
      name: "test_object"
      region: us-central1
      project: "test_project"
      auth_kind: "serviceaccount"
      interconnect: https://googleapis.com/compute/v1/projects/test_project/global/interconnects/...
      router: https://googleapis.com/compute/v1/projects/test_project/regions/us-central1/routers/...
      service_account_file: "/tmp/auth.pem"
      state: present
  register: disk
'''

RETURN = '''
cloudRouterIpAddress:
  description:
  - IPv4 address + prefix length to be configured on Cloud Router Interface for this
    interconnect attachment.
  returned: success
  type: str
customerRouterIpAddress:
  description:
  - IPv4 address + prefix length to be configured on the customer router subinterface
    for this interconnect attachment.
  returned: success
  type: str
interconnect:
  description:
  - URL of the underlying Interconnect object that this attachment's traffic will
    traverse through.
  returned: success
  type: str
description:
  description:
  - An optional description of this resource. .
  returned: success
  type: str
privateInterconnectInfo:
  description:
  - Information specific to an InterconnectAttachment. This property is populated
    if the interconnect that this is attached to is of type DEDICATED.
  returned: success
  type: complex
  contains:
    tag8021q:
      description:
      - 802.1q encapsulation tag to be used for traffic between Google and the customer,
        going to and from this network and region.
      returned: success
      type: int
googleReferenceId:
  description:
  - Google reference ID, to be used when raising support tickets with Google or otherwise
    to debug backend connectivity issues.
  returned: success
  type: str
router:
  description:
  - URL of the cloud router to be used for dynamic routing. This router must be in
    the same region as this InterconnectAttachment. The InterconnectAttachment will
    automatically connect the Interconnect to the network & region within which the
    Cloud Router is configured.
  returned: success
  type: dict
creationTimestamp:
  description:
  - Creation timestamp in RFC3339 text format.
  returned: success
  type: str
id:
  description:
  - The unique identifier for the resource. This identifier is defined by the server.
  returned: success
  type: str
name:
  description:
  - Name of the resource. Provided by the client when the resource is created. The
    name must be 1-63 characters long, and comply with RFC1035. Specifically, the
    name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?`
    which means the first character must be a lowercase letter, and all following
    characters must be a dash, lowercase letter, or digit, except the last character,
    which cannot be a dash.
  returned: success
  type: str
region:
  description:
  - Region where the regional interconnect attachment resides.
  returned: success
  type: str
'''

################################################################################
# Imports
################################################################################

from ansible.module_utils.gcp_utils import navigate_hash, GcpSession, GcpModule, GcpRequest, remove_nones_from_dict, replace_resource_dict
import json
import re
import time

################################################################################
# Main
################################################################################


def main():
    """Main function"""

    module = GcpModule(
        argument_spec=dict(
            state=dict(default='present', choices=['present', 'absent'], type='str'),
            interconnect=dict(required=True, type='str'),
            description=dict(type='str'),
            router=dict(required=True, type='dict'),
            name=dict(required=True, type='str'),
            region=dict(required=True, type='str')
        )
    )

    if not module.params['scopes']:
        module.params['scopes'] = ['https://www.googleapis.com/auth/compute']

    state = module.params['state']
    kind = 'compute#interconnectAttachment'

    fetch = fetch_resource(module, self_link(module), kind)
    changed = False

    if fetch:
        if state == 'present':
            if is_different(module, fetch):
                update(module, self_link(module), kind)
                fetch = fetch_resource(module, self_link(module), kind)
                changed = True
        else:
            delete(module, self_link(module), kind)
            fetch = {}
            changed = True
    else:
        if state == 'present':
            fetch = create(module, collection(module), kind)
            changed = True
        else:
            fetch = {}

    fetch.update({'changed': changed})

    module.exit_json(**fetch)


def create(module, link, kind):
    auth = GcpSession(module, 'compute')
    return wait_for_operation(module, auth.post(link, resource_to_request(module)))


def update(module, link, kind):
    module.fail_json(msg="InterconnectAttachment cannot be edited")


def delete(module, link, kind):
    auth = GcpSession(module, 'compute')
    return wait_for_operation(module, auth.delete(link))


def resource_to_request(module):
    request = {
        u'kind': 'compute#interconnectAttachment',
        u'interconnect': module.params.get('interconnect'),
        u'description': module.params.get('description'),
        u'router': replace_resource_dict(module.params.get(u'router', {}), 'selfLink'),
        u'name': module.params.get('name')
    }
    return_vals = {}
    for k, v in request.items():
        if v is not None:
            return_vals[k] = v

    return return_vals


def fetch_resource(module, link, kind, allow_not_found=True):
    auth = GcpSession(module, 'compute')
    return return_if_object(module, auth.get(link), kind, allow_not_found)


def self_link(module):
    return "https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/interconnectAttachments/{name}".format(**module.params)


def collection(module):
    return "https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/interconnectAttachments".format(**module.params)


def return_if_object(module, response, kind, allow_not_found=False):
    # If not found, return nothing.
    if allow_not_found and response.status_code == 404:
        return None

    # If no content, return nothing.
    if response.status_code == 204:
        return None

    try:
        module.raise_for_status(response)
        result = response.json()
    except getattr(json.decoder, 'JSONDecodeError', ValueError) as inst:
        module.fail_json(msg="Invalid JSON response with error: %s" % inst)

    if navigate_hash(result, ['error', 'errors']):
        module.fail_json(msg=navigate_hash(result, ['error', 'errors']))

    return result


def is_different(module, response):
    request = resource_to_request(module)
    response = response_to_hash(module, response)

    # Remove all output-only from response.
    response_vals = {}
    for k, v in response.items():
        if k in request:
            response_vals[k] = v

    request_vals = {}
    for k, v in request.items():
        if k in response:
            request_vals[k] = v

    return GcpRequest(request_vals) != GcpRequest(response_vals)


# Remove unnecessary properties from the response.
# This is for doing comparisons with Ansible's current parameters.
def response_to_hash(module, response):
    return {
        u'cloudRouterIpAddress': response.get(u'cloudRouterIpAddress'),
        u'customerRouterIpAddress': response.get(u'customerRouterIpAddress'),
        u'interconnect': response.get(u'interconnect'),
        u'description': response.get(u'description'),
        u'privateInterconnectInfo': InterconnectAttachmentPrivateinterconnectinfo(response.get(u'privateInterconnectInfo', {}), module).from_response(),
        u'googleReferenceId': response.get(u'googleReferenceId'),
        u'router': response.get(u'router'),
        u'creationTimestamp': response.get(u'creationTimestamp'),
        u'id': response.get(u'id'),
        u'name': response.get(u'name')
    }


def region_selflink(name, params):
    if name is None:
        return
    url = r"https://www.googleapis.com/compute/v1/projects/.*/regions/[a-z1-9\-]*"
    if not re.match(url, name):
        name = "https://www.googleapis.com/compute/v1/projects/{project}/regions/%s".format(**params) % name
    return name


def async_op_url(module, extra_data=None):
    if extra_data is None:
        extra_data = {}
    url = "https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/operations/{op_id}"
    combined = extra_data.copy()
    combined.update(module.params)
    return url.format(**combined)


def wait_for_operation(module, response):
    op_result = return_if_object(module, response, 'compute#operation')
    if op_result is None:
        return {}
    status = navigate_hash(op_result, ['status'])
    wait_done = wait_for_completion(status, op_result, module)
    return fetch_resource(module, navigate_hash(wait_done, ['targetLink']), 'compute#interconnectAttachment')


def wait_for_completion(status, op_result, module):
    op_id = navigate_hash(op_result, ['name'])
    op_uri = async_op_url(module, {'op_id': op_id})
    while status != 'DONE':
        raise_if_errors(op_result, ['error', 'errors'], 'message')
        time.sleep(1.0)
        op_result = fetch_resource(module, op_uri, 'compute#operation')
        status = navigate_hash(op_result, ['status'])
    return op_result


def raise_if_errors(response, err_path, module):
    errors = navigate_hash(response, err_path)
    if errors is not None:
        module.fail_json(msg=errors)


class InterconnectAttachmentPrivateinterconnectinfo(object):
    def __init__(self, request, module):
        self.module = module
        if request:
            self.request = request
        else:
            self.request = {}

    def to_request(self):
        return remove_nones_from_dict({
            u'tag8021q': self.request.get('tag8021q')
        })

    def from_response(self):
        return remove_nones_from_dict({
            u'tag8021q': self.request.get(u'tag8021q')
        })


if __name__ == '__main__':
    main()
