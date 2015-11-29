import json
import utils
import time

def _get_timestamp():
  return int(time.time())

def find_hostgroups_by_pattern(args):
  matching_patterns = args['matching']

  invalid_patterns = []
  if 'not_matching' in args:
    invalid_patterns = args['not_matching']
  hostgroups = utils.get_nagios_data('hostgroups').keys()

  ignore_case = False
  if 'ignore_case' in args and args['ignore_case'] == 'true':
    ignore_case = True

  matched_hostgroups = []
  for pattern in matching_patterns:
    if ignore_case:
      matched_hostgroups.extend([str(h) for h in hostgroups if pattern in h.lower()])
    else:
      matched_hostgroups.extend([str(h) for h in hostgroups if pattern in h])

  invalid_hostgroups = []
  for pattern in invalid_patterns:
    if ignore_case:
      invalid_hostgroups.extend([str(h) for h in matched_hostgroups if pattern in h.lower()])
    else:
      invalid_hostgroups.extend([str(h) for h in matched_hostgroups if pattern in h])

  target_hostgroups = set(matched_hostgroups) - set(invalid_hostgroups)

  output = []
  for hostgroup in target_hostgroups:
    output.append({'timestamp': _get_timestamp(), 'hostgroup': hostgroup})
  return output
