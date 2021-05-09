from jnpr.junos import Device
from lxml import etree
import sys

if __name__ == '__main__':
	with Device() as dev:
		interfaces_terse = dev.rpc.get_interface_information(terse=True)
		interfaces_description = dev.rpc.get_interface_information(descriptions=True)

	if type(interfaces_terse) != etree._Element or type(interfaces_description) != etree._Element:
		print('Blad pobierania danych')
		print('Terse - {}\nDescription - {}'.format(type(interfaces_terse), type(interfaces_description)))
		sys.exit()

	for interface in interfaces_description.iter('physical-interface'):
		name = interface.findtext('name').strip()
		description = interface.findtext('description').strip()
		ip_xpath ='//physical-interface[normalize-space(name)=$name]/logical-interface/address-family/interface-address/ifa-local'
		ip_result = interfaces_terse.xpath(ip_xpath, name=name)
		if ip_result:
			for ip in ip_result:
				ip = ip.text.strip()
				print '{} {} {}'.format(name, description, ip)
		else:	
			print '{} {}'.format(name, description)
