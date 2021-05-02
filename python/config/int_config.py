from jnpr.junos.utils.config import Config
from jnpr.junos import Device
from jinja2 import Template
import yaml
import os

def temp_path(vars):
	with Device() as dev:
		with Config(dev, mode='private') as cfg:
			cfg.load(template_path='template.j2', template_vars=vars, format='set')
			cfg.pdiff()
			cfg.rollback()
			

def temp_render(vars):
	with open('template.j2') as f:
		template = Template(f.read())

	with Device() as dev:
		with Config(dev, mode='private') as cfg:
			cfg.load(template=template, template_vars=vars, format='set')
			cfg.pdiff()
			cfg.rollback()

if __name__ == '__main__':
	os.chdir('/var/db/scripts/op')
	with open('vars.yml') as f:
		vars = yaml.load(f)
	#temp_path(vars)
	temp_render(vars)
