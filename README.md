# icinga-external-cmds-generator

Query icinga1.x/nagios for data and generate bulk external commands

### Why

TODO: Link to a new blog post on http://saurabh-hirani.github.io/

### Pre-requisites

* Familiarity with [external commands](http://docs.icinga.org/latest/en/extcommands2.html)
* [Nagira](https://github.com/dmytro/nagira) running on your monitoring server
* Go through some command templates provided in **templates/** and add new
  command templates if needed.

### Examples

1. Cache the icinga data locally:
```
$ ./get_icinga_data.sh $NAGIRA_HOST $NAGIRA_PORT
```
The above command does the following:
  - Generates hosts, services and hostgroups data from nagira and dumps their json in the **cache/** dir.

2. Generate a shell-script which will disable service checks on all hosts belonging
to a hostgroup which matches **stage** but not **stage-local**
```
$ python external_cmd_script_generator.py \
  --external-cmd disable_hostgroup_host_checks \
  --tmpl-vars-generator find_hostgroups_by_pattern \
  --func-args '{"matching": ["stage""], "not_matching": ["stage-local"], "ignore_case": "true"}'
  --output-file output/disable_hostgroup_host_checks-stage.sh
```
The above command does the following:
  - Searches for "disable_hostgorup_host_checks.tmpl in templates/
  - Needs to patch it - calls tmpl_vars_generators.find_hostgroup_by_pattern by passing in --func-args
  - Dumps the patched output in output/disable_hostgroup_host_checks-stage.sh

You can add a new template, write the appropriate function in **tmpl_vars_generators.py**
and get the desired output script.
