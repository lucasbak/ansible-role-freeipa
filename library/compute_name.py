#!/usr/bin/python
# This is a custom Ansible module. To use its logic in another module,
# you can import this file as a regular Python module if it's in your PYTHONPATH,
# or copy the compute_username function to your other module.
# Example import if in the same directory:
# from compute_name import compute_username
from ansible.module_utils.basic import AnsibleModule

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
        givenname=dict(type='str', required=True),
        sn=dict(type='str', required=True)
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    givenname = module.params['givenname']
    sn = module.params['sn']

    username = compute_username(givenname, sn)

    module.exit_json(changed=False, username=username)

if __name__ == '__main__':
    main()