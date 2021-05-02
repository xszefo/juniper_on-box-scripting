from jnpr.junos.utils.config import Config
from jnpr.junos import Device

def main():
	commands = '''
			set interfaces ge-0/0/0 description WAN
			set interfaces ge-0/0/1 description LAN1
			set interfaces ge-0/0/2 description LAN2
		   '''
	with Device() as dev:
		with Config(dev, mode='private') as cfg:
			cfg.load(commands, format="set")
			cfg.pdiff()
			cfg.rollback()
			




if __name__ == '__main__':
	main()
