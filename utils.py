import json
import os

def load_json_file(json_file):
  return json.load(open(json_file))

def reload_nagios_data(api_type):
  pass

def get_nagios_data(data_type, reload=False):
  json_file = os.path.join(data_type + '.json')
  if not os.path.exists(json_file):
    print 'ERROR: %s does not exist' % json_file
  return load_json_file(json_file)
