#!/usr/bin/env python

from jinja2 import Template
import yaml

with open('vars.yml') as f:
	vars = yaml.load(f)

with open('template.j2') as f:
	template = Template(f.read())
print template.render(vars)
