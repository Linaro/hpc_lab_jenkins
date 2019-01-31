#!/usr/bin/env python3

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: test_result_parser

short_description: This module parses test output with regexes
and puts the results into a Junit/Xunit XML files.

version_added: "2.4"

description:
    - "This module parses test output with regexes and puts the
       results into a Junit/Xunit XML files."

options:
    test_output_path:
        description:
            - Path to the file containing the test's output.
        required: true
    test_threshold:
        description:
            - Value that will determine the test result (via the
            failed method).
        required: true
    junit_write_path:
        description:
            - Path to the parsed JUnit/Xunit file will be
            written.
        required: false
    tag:
        description:
            - Tag on the filename.
        required: false
'''

EXAMPLES = '''
# Pass in a message
- name: Parse test output in playbook_dir
  test_result_parser:
    json_or_xml: 'xml'
    test_output_path: "{{ playbook_dir }}/log-{{ test.name }}-{{ results_tag }}.txt"
    test_threshold: "{{ test.threshold }}"
    junit_write_path: "{{ workspace }}/results"
    tag: '55'
'''

RETURN = '''
junit_write_path:
    description: Path to the outputted xml/json results
    type: str
'''
import os
import re

from ansible.module_utils.test_result_parser.parser import TestParser
from ansible.module_utils.basic import AnsibleModule
from ansible.errors import AnsibleError

def run_module():
    module_args = dict(
        test_output_path=dict(type='str', required=True),
        test_threshold=dict(type='str', required=True),
        junit_write_path=dict(type='str', required=False, default='./'),
        tag=dict(type='str', required=False, default='')
    )

    result = dict(
        changed=False,
        original_message='Nothing done by the test parser',
        message='Nothing done by the test parser'
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        return result

    result['original_message'] = repr(module.params)

    try:
        test_parser = TestParser()
        test_parser.parse(module.params['test_output_path'],
                          module.params['test_threshold'],
                          module.params['junit_write_path'],
                          module.params['tag'])
        result['message'] = 'Test parsed succesfully : result saved here, %s' % module_args['junit_write_path']
        result['changed'] = True
        module.exit_json(**result)
    except AnsibleError as err:
        result['message'] = 'Ansible Error raised'
        result['changed'] = False
        module.fail_json(msg=repr(err), **result)
    except Exception as err:
        result['message'] = 'Failed to parse test'
        result['changed'] = False
        module.fail_json(msg=repr(err), **result)

def main():
    run_module()

if __name__ == '__main__':
    main()