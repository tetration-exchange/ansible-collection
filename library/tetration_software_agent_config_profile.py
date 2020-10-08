ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: tetration_software_agent_config_profile

short description: Enables creation, modification, deletion and query of software agent
  config profiles

version_added: '2.9'

description: Enables creation, modification, deletion and query of software agent
  config profiles

options:
    allow_broadcast:
        default: 'True'
        description: Whether or not broadcast traffic should be allowed
        type: bool
    allow_multicast:
        default: 'True'
        description: Whether or not broadcast traffic should be allowed
        type: bool
    auto_upgrade_opt_out:
        default: 'True'
        description: If True, agents are not auto-upgraded during upgrade of Tetration
          cluster
        type: bool
    cpu_quota_mode:
        choices: [0, 1, 2]
        default: 1
        description: 0=disabled 1=Adjusted 2=To
        type: int
    cpu_quota_pct:
        default: 3
        description: The amount of CPU quota to give to agent on the end host
        type: int
    data_plane_disabled:
        default: 'False'
        description: If true, agent stops reporting flows to Tetration
        type: bool
    enable_cache_sidechannel:
        default: 'False'
        description: Whether or not sidechannel detection is enabled
        type: bool
    enable_forensic:
        default: 'False'
        description: Whether or not forensics is enabled
        type: bool
    enable_meltdown:
        default: 'False'
        description: Whether or not meltdown detection is enabled
        type: bool
    enable_pid_lookup:
        default: 'False'
        description: Whether or not pid lookup for flow search is enabled
        type: bool
    enforcement_disabled:
        default: 'True'
        description: If True, enforcement is disabled
        type: bool
    name:
        description: User provided name of software agent profile
        required: true
        type: string
    preserve_existing_rules:
        default: 'False'
        description: If True, existing firewall rules are preserved
        type: bool
    root_app_scope_id:
        description: ID of root app scope for tenant to which an agent profile should
          be applied
        type: string
    state:
        choices: [present, absent, query]
        default: present
        description: Add, change, remove or query for agent config profiles
        required: true
        type: string
    tenant_name:
        description: Tenant name to which an agent config profile should be applied
        type: string

extends_documentation_fragment: tetration_doc_common

notes:
- Requires the `requests` Python module.

requirements:
- requests

author:
  - Brandon Beck (@techbeck03)
  - Joe Jacobs (@joej164)

'''

EXAMPLES = '''
# Add or Modify agent config profile
tetration_software_agent_config_profile:
    name: Enforcement Enabled
    tenant_name: ACME
    allow_broadcast: True
    allow_multicast: True
    auto_upgrade_opt_out: False
    cpu_quota_mode: 1
    cpu_quota_pct: 3
    data_plane_disabled: False
    enable_cache_sidechannel: False
    enable_forensic: True
    enable_meltdown: False
    enable_pid_lookup: True
    enforcement_disabled: False
    preserve_existing_rules: False
    state: present
    provider:
      host: "https://tetration-cluster.company.com"
      api_key: 1234567890QWERTY
      api_secret: 1234567890QWERTY

# Delete agent config profile
tetration_software_agent_config_profile:
    name: Enforcement Enabled
    tenant_name: ACME
    state: absent
    provider:
      host: "https://tetration-cluster.company.com"
      api_key: 1234567890QWERTY
      api_secret: 1234567890QWERTY

# Query agent config profile
tetration_software_agent_config_profile:
    name: Enforcement Enabled
    tenant_name: ACME
    state: query
    provider:
      host: "https://tetration-cluster.company.com"
      api_key: 1234567890QWERTY
      api_secret: 1234567890QWERTY
'''

RETURN = '''
---
object:
  contains:
    allow_broadcast:
      description: Whether or not broadcast traffic should be allowed
      returned: when C(state) is present or query
      sample: 'True'
      type: bool
    allow_multicast:
      description: Whether or not broadcast traffic should be allowed
      returned: when C(state) is present or query
      sample: 'True'
      type: bool
    auto_upgrade_opt_out:
      description: If True, agents are not auto-upgraded during upgrade of Tetration
        cluster
      returned: when C(state) is present or query
      sample: 'False'
      type: bool
    cpu_quota_mode:
      description: 0=disabled 1=Adjusted 2=Top
      returned: when C(state) is present or query
      sample: 1
      type: bool
    cpu_quota_pct:
      description: The amount of CPU quota to give to agent on the end host (pct)
      returned: when C(state) is present or query
      sample: 3
      type: int
    cpu_quota_us:
      description: The amount of CPU quota to give to agent on the end host (us)
      returned: when C(state) is present or query
      sample: 30000
      type: int
    data_plane_disabled:
      description: If true, agent stops reporting flows to Tetration
      returned: when C(state) is present or query
      sample: 'False'
      type: bool
    enable_cache_sidechannel:
      description: Whether or not sidechannel detection is enabled
      returned: when C(state) is present or query
      sample: 'False'
      type: bool
    enable_forensic:
      description: Whether or not forensics is enabled
      returned: when C(state) is present or query
      sample: 'True'
      type: bool
    enable_meltdown:
      description: Whether or not meltdown detection is enabled
      returned: when C(state) is present or query
      sample: 'False'
      type: bool
    enable_pid_lookup:
      description: Whether or not pid lookup for flow search is enabled
      returned: when C(state) is present or query
      sample: 'True'
      type: bool
    enforcement_disabled:
      description: If True, enforcement is disabled
      returned: when C(state) is present or query
      sample: 'False'
      type: bool
    id:
      description: Unique identifier for the agent config intent
      returned: when C(state) is present or query
      sample: 2000
      type: int
    name:
      description: User provided name for config intent
      returned: when C(state) is present or query
      sample: Enforcement Enabled
      type: string
    preserve_existing_rules:
      description: If True, existing firewall rules are preserved
      returned: when C(state) is present or query
      sample: 'False'
      type: bool
  description: the changed or modified object(s)
  returned: always
  type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.tetration import TetrationApiModule
from ansible.module_utils.tetration_constants import TETRATION_API_SCOPES
from ansible.module_utils.tetration_constants import TETRATION_API_AGENT_CONFIG_PROFILES
from ansible.module_utils.tetration_constants import TETRATION_PROVIDER_SPEC


def validate_ranges(params_to_validate, all_params, low_value, high_value):
    invalid_pct_params = []
    for param in params_to_validate:
        if all_params[param] is not None and all_params[param] not in range(low_value, high_value + 1):
            invalid_pct_params.append(param)

    return invalid_pct_params


def main():
    ''' Main entry point for module execution
    '''
    #
    # Module specific spec
    module_args = dict(
        name=dict(type='str', required=False),
        id=dict(type='str', required=False),
        app_scope_id=dict(type='str', required=False),
        app_scope_name=dict(type='str', required=False),
        allow_broadcast=dict(type='bool', required=False),
        allow_link_local=dict(type='bool', required=False),
        allow_multicast=dict(type='bool', required=False),
        auto_upgrade_opt_out=dict(type='bool', required=False),
        cpu_quota_mode=dict(type='int', required=False, choices=[0, 1, 2]),
        cpu_quota_pct=dict(type='int', required=False),
        cpu_quota_us=dict(type='int', required=False),
        data_plane_disabled=dict(type='bool', required=False),
        enable_dns=dict(type='bool', required=False),
        enable_forensics=dict(type='bool', required=False),
        enable_meltdown=dict(type='bool', required=False),
        enable_pid_lookup=dict(type='bool', required=False),
        enforcement_cpu_quota_mode=dict(type='int', required=False, choices=[0, 1, 2]),
        enforcement_cpu_quota_pct=dict(type='int', required=False),
        enforcement_cpu_quota_us=dict(type='int', required=False),
        enforcement_disabled=dict(type='bool', required=False, default=True),
        enforcement_max_rss_limit=dict(type='int', required=False),
        enforcement_max_rss_limit_mb=dict(type='int', required=False),
        forensics_cpu_quota_mode=dict(type='int', required=False, choices=[0, 1, 2]),
        forensics_cpu_quota_pct=dict(type='int', required=False),
        forensics_cpu_quota_us=dict(type='int', required=False),
        forensics_mem_quota_bytes=dict(type='int', required=False),
        forensics_mem_quota_mb=dict(type='int', required=False),
        max_rss_limit=dict(type='int', required=False),
        max_rss_limit_mb=dict(type='int', required=False),
        preserve_existing_rules=dict(type='bool', required=False),
        state=dict(choices=['present', 'absent', 'query']),
        provider=dict(type='dict', options=TETRATION_PROVIDER_SPEC)
    )

    # Building custom error handling to display custom error messages

    # Combine specs and include provider parameter
    module = AnsibleModule(
        argument_spec=module_args,
        required_one_of=[
            ['app_scope_id', 'app_scope_name'],
            ['name', 'id']
        ],
        mutually_exclusive=[
            ['app_scope_id', 'app_scope_name'],
            ['name', 'id'],
            ['cpu_quota_pct', 'cpu_quota_us'],
            ['enforcement_cpu_quota_pct', 'enforcement_cpu_quota_us'],
            ['forensics_cpu_quota_pct', 'forensics_cpu_quota_us'],
            ['enforcement_max_rss_limit', 'enforcement_max_rss_limit_mb'],
            ['forensics_mem_quota_bytes', 'forensics_mem_quota_mb'],
            ['max_rss_limit', 'max_rss_limit_mb'],
        ]
    )

    if module.params['name'] == 'Default':
        module.fail_json(msg='Cannot modify the default agent profile')

    # Verify the following modules have valid inputs between 1 and 100% inclusive
    percent_params = ['cpu_quota_pct', 'enforcement_cpu_quota_pct', 'forensics_cpu_quota_pct']
    invalid_percent_params = validate_ranges(percent_params, module.params, low_value=1, high_value=100)
    if invalid_percent_params:
        module.fail_json(msg=f'The following params need to be between 1 and 100 inclusive: {invalid_percent_params}')

    # Verify the following modules have valid inputs between 10,000 and 1,000,000 inclusive
    us_params = ['cpu_quota_us', 'enforcement_cpu_quota_us', 'forensics_cpu_quota_us']
    invalid_us_params = validate_ranges(us_params, module.params, low_value=10000, high_value=100000)
    if invalid_us_params:
        module.fail_json(msg=f'The following params need to be between 10,000 and 1,000,000 inclusive: {invalid_us_params}')

    # Verify the following modules have valid inputs between 128 and 2048 inclusive
    mb_params = ['enforcement_max_rss_limit_mb', 'forensics_mem_quota_mb']
    invalid_mb_params = validate_ranges(mb_params, module.params, low_value=128, high_value=2048)
    if invalid_mb_params:
        module.fail_json(msg=f'The following params need to be between 128 and 2048 inclusive: {invalid_mb_params}')

    # Verify the following modules have valid inputs between 200 and 2048 inclusive
    vis_mb_params = ['max_rss_limit_mb']
    invalid_vis_mb_params = validate_ranges(vis_mb_params, module.params, low_value=200, high_value=2048)
    if invalid_vis_mb_params:
        module.fail_json(msg=f'The following params need to be between 200 and 2048 inclusive: {invalid_vis_mb_params}')

    # Verify the following modules have valid inputs between 134,217,728 and 2,147,483,649 inclusive
    bytes_params = ['enforcement_max_rss_limit', 'forensics_mem_quota_bytes']
    invalid_bytes_params = validate_ranges(bytes_params, module.params, low_value=134217728, high_value=2147483649)
    if invalid_bytes_params:
        module.fail_json(
            msg=f'The following params need to be between 134,217,728 and 2,147,483,649 inclusive: {invalid_bytes_params}')

    # Verify the following modules have valid inputs between 209,715,200 and 2,147,483,649 inclusive
    vis_bytes_params = ['max_rss_limit']
    invalid_vis_bytes_params = validate_ranges(vis_bytes_params, module.params, low_value=209715200, high_value=2147483649)
    if invalid_vis_bytes_params:
        module.fail_json(
            msg=f'The following params need to be between 209,715,200 and 2,147,483,649 inclusive: {invalid_vis_bytes_params}')

    tet_module = TetrationApiModule(module)
    # These are all elements we put in our return JSON object for clarity
    result = {
        'changed': False,
        'object': {},
    }

    # state = module.params['state']
    # check_mode = module.check_mode
    # name = module.params['name']
    # app_scope_id = module.params['root_app_scope_id']
    # app_scope_name = module.params['tenant_name']
    # allow_broadcast = module.params['allow_broadcast']
    # allow_multicast = module.params['allow_multicast']
    # auto_upgrade_opt_out = module.params['auto_upgrade_opt_out']
    # cpu_quota_mode = module.params['cpu_quota_mode']
    # cpu_quota_pct = module.params['cpu_quota_pct']
    # data_plane_disabled = module.params['data_plane_disabled']
    # enable_cache_sidechannel = module.params['enable_cache_sidechannel']
    # enable_forensics = module.params['enable_forensics']
    # enable_meltdown = module.params['enable_meltdown']
    # enable_pid_lookup = module.params['enable_pid_lookup']
    # enforcement_disabled = module.params['enforcement_disabled']
    # preserve_existing_rules = module.params['preserve_existing_rules']
    # existing_app_scope = None
    # existing_config_profile = None
    # agent_options = [
    #     'allow_broadcast',
    #     'allow_multicast',
    #     'auto_upgrade_opt_out',
    #     'cpu_quota_mode',
    #     'cpu_quota_pct',
    #     'data_plane_disabled',
    #     'enable_cache_sidechannel',
    #     'enable_forensics',
    #     'enable_meltdown',
    #     'enable_pid_lookup',
    #     'enforcement_disabled',
    #     'preserve_existing_rules'
    # ]
    # agent_update_remove_keys = [
    #     'preserve_existing_rules'
    # ]

    # =========================================================================
    # Get current state of the object
    app_scopes = tet_module.run_method('GET', TETRATION_API_SCOPES)
    app_scope_dict = {s['name']: s['id'] for s in app_scopes}

    existing_app_scope_id = None
    if module.params['app_scope_id'] in app_scope_dict.values():
        existing_app_scope_id = module.params['app_scope_id']
    else:
        scope_name = module.params['app_scope_name']
        existing_app_scope_id = app_scope_dict.get(scope_name)

    if not existing_app_scope_id:
        if module.params['app_scope_id']:
            module.fail_json(msg=f"Unable to find existing app scope id: {module.params['app_scope_id']}")
        else:
            module.fail_json(msg=f"Unable to find existing app scope named: {module.params['app_scope_name']}")

    existing_profiles = tet_module.run_method('GET', TETRATION_API_AGENT_CONFIG_PROFILES)

    existing_profile = None

    for profile in existing_profiles:
        if module.params['name'] == profile['name']:
            existing_profile = profile
        elif module.params['id'] == profile['id']:
            existing_profile = profile

    module.exit_json(**result)

    # ---------------------------------
    # STATE == 'present'
    # ---------------------------------
    if module.params['state'] == 'present':
        new_object = {
            'name': module.params['name'],
            'app_scope_id': existing_app_scope_id,
            'allow_broadcast': module.params['allow_broadcast'],
            'allow_link_local': module.params['allow_link_local'],
            'allow_multicast': module.params['allow_multicast'],
            'auto_upgrade_opt_out': module.params['auto_upgrade_opt_out'],
            'cpu_quota_mode': module.params['cpu_quota_mode'],
            'cpu_quota_pct': module.params['cpu_quota_pct'],
            'cpu_quota_us': module.params['cpu_quota_us'],
            'data_plane_disabled': module.params['data_plane_disabled'],
            'enable_dns': module.params['enable_dns'],
            'enable_forensics': module.params['enable_forensics'],
            'enable_meltdown': module.params['enable_meltdown'],
            'enable_pid_lookup': module.params['enable_pid_lookup'],
            'enforcement_cpu_quota_mode': module.params['enforcement_cpu_quota_mode'],
            'enforcement_cpu_quota_pct': module.params['enforcement_cpu_quota_pct'],
            'enforcement_cpu_quota_us': module.params['enforcement_cpu_quota_us'],
            'enforcement_disabled': module.params['enforcement_disabled'],
            'enforcement_max_rss_limit': module.params['enforcement_max_rss_limit'],
            'enforcement_max_rss_limit_mb': module.params['enforcement_max_rss_limit_mb'],
            'forensics_cpu_quota_mode': module.params['forensics_cpu_quota_mode'],
            'forensics_cpu_quota_pct': module.params['forensics_cpu_quota_pct'],
            'forensics_cpu_quota_us': module.params['forensics_cpu_quota_us'],
            'forensics_mem_quota_bytes': module.params['forensics_mem_quota_bytes'],
            'forensics_mem_quota_mb': module.params['forensics_mem_quota_mb'],
            'max_rss_limit': module.params['max_rss_limit'],
            'max_rss_limit_mb': module.params['max_rss_limit_mb'],
            'preserve_existing_rules': module.params['preserve_existing_rules'],
        }

        obj_keys_to_remove = []
        for k, v in new_object.items():
            if v is None:
                obj_keys_to_remove.append(k)

        for key in obj_keys_to_remove:
            new_object.pop(key)

        result['to_update'] = new_object
        module.exit_json(**result)

        for option in agent_options:
            new_object[option] = module.params.get(option)
        if not existing_config_profile:
            if not check_mode:
                result['object'] = tet_module.run_method(
                    method_name='post',
                    target=TETRATION_API_AGENT_CONFIG_PROFILES,
                    req_payload=new_object
                )
            else:
                result['object'] = new_object
            result['changed'] = True
        else:
            for option in agent_update_remove_keys:
                del new_object[option]
            result['changed'] = tet_module.filter_object(new_object, existing_config_profile, check_only=True)
            if not check_mode:
                result['object'] = tet_module.run_method(
                    method_name='put',
                    target='%s/%s' % (TETRATION_API_AGENT_CONFIG_PROFILES, existing_config_profile['id']),
                    req_payload=new_object
                )
            else:
                result['object'] = new_object

    # ---------------------------------
    # STATE == 'absent'
    # ---------------------------------
    elif module.params['state'] in 'absent':
        if existing_config_profile:
            if not check_mode:
                tet_module.run_method(
                    method_name='delete',
                    target='%s/%s' % (TETRATION_API_AGENT_CONFIG_PROFILES, existing_config_profile['id'])
                )
            result['changed'] = True
    # ---------------------------------
    # STATE == 'query'
    # ---------------------------------
    else:
        result['object'] = existing_config_profile

    module.exit_json(**result)


if __name__ == '__main__':
    main()