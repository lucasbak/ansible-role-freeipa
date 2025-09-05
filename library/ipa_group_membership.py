#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import re

DOCUMENTATION = r'''
---
module: ipa_group_membership

short_description: Manage FreeIPA group membership from cluster_users and cluster_groups

options:
  cluster_groups:
    description: List of group names.
    required: true
    type: list
    elements: str
  cluster_users:
    description: List of user dicts with group membership.
    required: true
    type: list
    elements: dict
  ipa_host:
    description: IPA server hostname.
    required: true
    type: str
  ipa_user:
    description: IPA admin username.
    required: true
    type: str
  ipa_pass:
    description: IPA admin password.
    required: true
    type: str
  validate_certs:
    description: Validate SSL certificates.
    required: false
    type: bool
    default: true

author:
  - Your Name
'''

EXAMPLES = r'''
- name: Sync IPA group membership
  ipa_group_membership:
    cluster_groups:
      - bourbaki_admins
      - bourbaki_users
    cluster_users:
      - givenname: "Lucas"
        sn: "Bakalian"
        groups: ['bourbaki_admins','bourbaki_users']
        password: "mysupersecret"
        krbpasswordexpiration: 20500119235959
    ipa_host: ipa.example.com
    ipa_user: admin
    ipa_pass: topsecret
    validate_certs: false
'''

RETURN = r'''
changed:
  description: Whether any changes were made.
  type: bool
  returned: always
'''

def compute_username(givenname, sn):
    given_initial = givenname[0].lower()
    sn_parts = sn.strip().split()
    if len(sn_parts) == 1:
        return given_initial + sn_parts[0].lower()
    else:
        initials = ''.join([part[0].lower() for part in sn_parts[:-1]])
        last_part = sn_parts[-1].lower()
        return given_initial + initials + last_part

def main():
    module_args = dict(
        cluster_groups=dict(type='list', elements='str', required=True),
        cluster_users=dict(type='list', elements='dict', required=True),
        ipa_host=dict(type='str', required=True),
        ipa_user=dict(type='str', required=True),
        ipa_pass=dict(type='str', required=True, no_log=True),
        validate_certs=dict(type='bool', required=False, default=True),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    cluster_groups = module.params['cluster_groups']
    cluster_users = module.params['cluster_users']
    ipa_host = module.params['ipa_host']
    ipa_user = module.params['ipa_user']
    ipa_pass = module.params['ipa_pass']
    validate_certs = module.params['validate_certs']

    # Compute group membership
    group_members = {g: [] for g in cluster_groups}
    # Use local compute_name module to generate username
    for user in cluster_users:
        username = compute_username(user.get('givenname', ''), user.get('sn', ''))
        for group in user.get('groups', []):
            if group in group_members:
                group_members[group].append(username)

    # Build tasks for community.general.ipa_group
    results = []
    changed = False
    for group, users in group_members.items():
        # Use Ansible's module.run_command to call community.general.ipa_group
        # But here, just return the intended parameters for illustration
        results.append({
            'group': group,
            'users': users,
            'ipa_host': ipa_host,
            'ipa_user': ipa_user,
            'validate_certs': validate_certs,
        })
        # In a real module, you would use AnsibleModule's methods to call the ipa_group module

    module.exit_json(changed=changed, group_members=group_members, ipa_group_tasks=results)

if __name__ == '__main__':
    main()