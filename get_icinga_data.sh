#!/bin/bash
set -x
curl http://$1:$2/_objects/services/_full > cache/services.json
curl http://$1:$2/_objects/hosts/_full > cache/hosts.json
curl http://$1:$2/_objects/hostgroups/_full > cache/hostgroups.json
