#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: tetration_scope

short_description: Add, remove, and update scopes

version_added: '2.9'

description:
- Enables management of Cisco Tetration scopes
- Enables creation, modification, deletion of scopes
- For updates of C(short_query) parameter requires calling for `tetration_scope_commit_query_changes` module after all shory query updates are done.

notes:
- If the ID is set, uses the C(short_name) field as if you were going to update the object
- If you pass in an ID that does not exist, the module will error out

options:
  description:
    description: User specified description of the scope
    type: string
  parent_app_scope_id:
    description:
    - ID of the parent scope
    - Required when C(scope_name) is set
    type: string
  policy_priority:
    description: Used to sort application priorities
    type: int
  scope_id:
    description:
    - Unique identifier for the scope
    type: string
  short_name:
    description:
    - User specified name of the scope
    type: string
  query_single:
    description:
    - Match Criteria associated with the scope
    - Supports only a single filter
    - Provides input validation
    - Mutually exclusive with [C(query_filter), C(query_nested)]
    type: dict
  query_multiple:
    description:
    - Simple filter associated with the scope
    - Supports a single list of filters with one logical operator
    - Provides input validation
    - Mutually exclusive with [C(query_single), C(query_nested)]
    type: dict
  query_raw:
    description:
    - Complex filter associated with the scope
    - Supports deeply nested filter structures
    - Provides only top level input validation
    - Mutually exclusive with [C(query_single), C(query_filter)]
    type: dict
  state:
    choices: [present, absent]
    description: Add, change, or remove scopes
    required: true
    type: string

extends_documentation_fragment: tetration_doc_common

notes:
- Requires the `requests` Python module.
- 'Required API Permission(s): app_policy_management or user_role_scope_management or sensor_management'

requirements:
- requests

author:
    - Brandon Beck (@techbeck03)
    - Joe Jacobs (@joej164)
'''

EXAMPLES = '''
# Add or Modify scope with a single filter
tetration_scope:
    short_name: Application
    parent_app_scope_id: abcd1234
    description: Scope for ACME example application
    query_single:
        type: subnet
        field: ip
        value: 172.16.0.0/12
    state: present
    provider:
      host: "https://tetration-cluster.company.com"
      api_key: 1234567890QWERTY
      api_secret: 1234567890QWERTY

# Add or Modify scope with multiple filters
tetration_scope:
    short_name: Application
    parent_app_scope_id: abcd1234
    description: Scope for ACME example application
    query_multiple:
      filter:
        - field: os
          type: contains
          value: linux
        - field: os
          type: contains
          value: windows
        - field: os
          type: contains
          value: mac
      type: or
    state: present
    provider:
      host: "https://tetration-cluster.company.com"
      api_key: 1234567890QWERTY
      api_secret: 1234567890QWERTY

# Add or Modify scope with multiple nested filters
tetration_scope:
    short_name: Application
    parent_app_scope_id: abcd1234
    description: Scope for ACME example application
    query_raw:
      filters:
        - field: os
          type: contains
          value: linux
        - field: os
          type: contains
          value: windows
        - filters:
            - field: host_tags_cvss3
              type: gt
              value: 8
            - field: host_tags_cvss2
              type: gt
              value: 8
          type: or
      type: or
    state: present
    provider:
      host: "https://tetration-cluster.company.com"
      api_key: 1234567890QWERTY
      api_secret: 1234567890QWERTY


# Delete scope
tetration_scope:
    short_name: Application
    parent_app_scope_id: abcd1234
    state: absent
    provider:
      host: "https://tetration-cluster.company.com"
      api_key: 1234567890QWERTY
      api_secret: 1234567890QWERTY
'''

RETURN = '''
---
object:
  contains:
    child_app_scope_ids:
      description: "An array of child scope ids"
      returned: when C(state) is present
      sample: '[]'
      type: list
    description:
      description: User specified description of the scope
      returned: when C(state) is present
      sample: Scope for ACME example application
      type: string
    dirty:
      description: Indicates a child or parent query has been updated and that the
        changes need to be committed
      returned: when C(state) is present
      sample: 'false'
      type: bool
    dirty_short_query:
      description: Non-null if the query for this scope has been updated but not yet
        committed
      returned: when C(state) is present
      sample: 'null'
      type: dict
    id:
      description: Unique identifier for the scope
      returned: when C(state) is present
      sample: 5c93da83497d4f33d7145960
      type: int
    name:
      description: Fully qualified name of the scope. This is a fully qualified name,
        i.e. it has name of parent scopes (if applicable) all the way to the root
        scope
      returned: when C(state) is present
      sample: ACME:Example:Application
      type: string
    parent_app_scope_id:
      description: ID of the parent scope
      returned: when C(state) is present
      sample: 596d5215497d4f3eaef1fd04
      type: string
    policy_priority:
      description: Used to sort application priorities
      returned: when C(state) is present
      sample: 2
      type: int
    query:
      description: Filter (or match criteria) associated with the scope in conjunction
        with the filters of the parent scopes (all the way to the root scope)
      returned: when C(state) is present
      sample: JSON Filter (full)
      type: dict
    root_app_scope_id:
      description: ID of the root scope this scope belongs to
      returned: when C(state) is present
      sample: 596d3d2f497d4f35380b68ef
      type: string
    short_name:
      description: User specified name of the scope
      returned: when C(state) is present
      sample: Application
      type: string
    query_single:
      description: Filter (or match criteria) associated with the scope
      returned: when C(state) is present
      sample: JSON Filter (short)
      type: dict
    updated_at:
      description: Date this scope was last updated (Unix Epoch)
      returned: when C(state) is present
      sample: 1500402190
      type: int
    vrf_id:
      description: ID of the VRF to which scope belongs to
      returned: when C(state) is present
      sample: 1
      type: int
  description: the changed or modified object(s)
  returned: always
  type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.tetration_constants import TETRATION_API_SCOPES
from ansible.module_utils.tetration_constants import TETRATION_PROVIDER_SPEC
from ansible.module_utils.tetration import TetrationApiModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    single_filter = dict(
        field=dict(type='str', required=True),
        type=dict(type='str', required=True),
        value=dict(type='str', required=True)
    )

    query_filter_structure = dict(
        filters=dict(type='list', elements='dict', options=single_filter, required=True),
        type=dict(type='str', required=True)
    )

    nested_query_filter_structure = dict(
        filters=dict(type='list', elements='dict', required=True),
        type=dict(type='str', required=True)
    )

    module_args = dict(
        scope_id=dict(type='str', required=False),
        short_name=dict(type='str', required=False),
        description=dict(type='str', required=False),
        query_multiple=dict(type='dict', options=query_filter_structure, required=False),
        query_raw=dict(type='dict', options=nested_query_filter_structure, required=False),
        query_single=dict(type='dict', options=single_filter, reqired=False),
        parent_app_scope_id=dict(type='str', required=False),
        policy_priority=dict(type='int', required=False),
        state=dict(choices=['present', 'absent'], required=True),
        provider=dict(type='dict', options=TETRATION_PROVIDER_SPEC)
    )

    # Create the objects that will be returned
    result = {
        "object": None,
        "changed": False
    }
    result_obj = dict(
        child_app_scope_ids=[],
        description=None,
        dirty=None,
        dirty_short_query=None,
        id=None,
        name=None,
        parent_app_scope_id=None,
        policy_priority=None,
        query=None,
        root_app_scope_id=None,
        short_name=None,
        short_query=None,
        updated_at=None,
        vrf_id=None
    )

    # Creating the Ansible Module
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_one_of=[
            ['scope_id', 'short_name'],
        ],
        mutually_exclusive=[
            ['query_multiple', 'query_raw', 'query_single']
        ],
        required_by={
            'short_name': ['parent_app_scope_id']
        },
    )

    # Get current state of the object
    tet_module = TetrationApiModule(module)
    all_scopes_response = tet_module.run_method('GET', TETRATION_API_SCOPES)

    all_scopes_lookup = {(s['short_name'], s['parent_app_scope_id']): s['id'] for s in all_scopes_response}
    unique_scope_name = module.params['short_name'], module.params['parent_app_scope_id']

    # Verify the passed in data is valid
    if module.params['scope_id'] and module.params['scope_id'] not in all_scopes_lookup.values():
        error_message = "`scope_id` passed into the module does not exist."
        module.fail_json(msg=error_message, searched_scope=module.params['scope_id'])

    if module.params['parent_app_scope_id'] and module.params['parent_app_scope_id'] not in all_scopes_lookup.values():
        error_message = "`parent_app_scope_id` passed into the module does not exist."
        module.fail_json(msg=error_message)

    # Since the query parameter data all goes into one field eventually, just extract it into
    # A value here for use later on in the module
    query_parameters = ['query_multiple', 'query_raw', 'query_single']
    extracted_query_filter = {}
    for query in query_parameters:
        if module.params[query]:
            extracted_query_filter = module.params[query]

    # Implment changes as defined in the module
    if module.params['state'] == 'present':
        if module.params['scope_id'] or unique_scope_name in all_scopes_lookup.keys():
            # Object exists, doing an update
            if module.params['scope_id']:
                scope_id_to_update = module.params['scope_id']
            else:
                scope_id_to_update = all_scopes_lookup[unique_scope_name]

            route = f"{TETRATION_API_SCOPES}/{scope_id_to_update}"
            response = tet_module.run_method('GET', route)

            req_payload = {
                'short_name': None,
                'short_query': {},
                'description': None,
                'parent_app_scope_id': None,
                'policy_priority': None
            }

            payload_keys = [k for k in req_payload.keys()]
            for key in payload_keys:
                if module.params.get(key) is not None and module.params[key] != response[key]:
                    req_payload[key] = module.params[key]
                elif key == 'short_query':
                    if extracted_query_filter and extracted_query_filter != response['short_query']:
                        req_payload[key] = extracted_query_filter
                    else:
                        req_payload.pop(key)
                else:
                    req_payload.pop(key)

            # Updating the Update Object
            if req_payload:
                update_response = tet_module.run_method('PUT', route, req_payload=req_payload)
                result['changed'] = True
                result_obj = update_response
            else:
                result_obj = response

        elif unique_scope_name not in all_scopes_lookup.keys():
            # Creating a new object
            if not extracted_query_filter:
                error_message = (
                    'In order to create a new `scope` you must also add a query parameter.'
                )
                module.fail_json(msg=error_message)

            req_payload = {
                'short_name': module.params['short_name'],
                'short_query': extracted_query_filter,
                'description': module.params['description'],
                'parent_app_scope_id': module.params['parent_app_scope_id'],
                'policy_priority': module.params['policy_priority']
            }
            response = tet_module.run_method('POST', TETRATION_API_SCOPES, req_payload=req_payload)
            result_obj = response
            result['changed'] = True
        else:
            error_message = "An unknown error occured"
            module.fail_json(msg=error_message)
    elif module.params['state'] == 'absent':
        if module.params['scope_id'] or unique_scope_name in all_scopes_lookup.keys():
            # User exists, doing an update
            if module.params['scope_id']:
                scope_id_to_delete = module.params['scope_id']
            else:
                scope_id_to_delete = all_scopes_lookup[unique_scope_name]

            route = f"{TETRATION_API_SCOPES}/{scope_id_to_delete}"
            response = tet_module.run_method('DELETE', route)

            if response.get('details'):
                error_message = "There are objects using this scope.  Review the `details` tag for more details."
                module.fail_json(msg=error_message, details=response['details'])
            else:
                result['changed'] = True
                result_obj = response

    result['object'] = result_obj
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
