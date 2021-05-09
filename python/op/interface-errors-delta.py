from jnpr.junos import Device
from lxml import etree
import sys
import time

# Slownik porownywanych parametrow razem z ich sciezkami
PARAMETERS = {
	'input_drops': 'input-error-list/input-drops',
	'crc': 'ethernet-mac-statistics/input-crc-errors',
}

def get_parameter(xml, path):
	''' Funkcja zwraca wartosc prametru dla danej sciezki XML'''
	return xml.findtext(path).strip()

def get_data():
	result = {}
	physical_interfaces = ['ge', 'xe', 'et']

	with Device() as dev:
		interfaces_extensive = dev.rpc.get_interface_information(extensive=True)

	if type(interfaces_extensive) != etree._Element:
		print('Blad pobierania danych')
		print('Typ danych - {}'.format(type(interfaces_extensive)))
		sys.exit()

	for interface in interfaces_extensive.iter('physical-interface'):
		#name = interface.findtext('name').strip()
		name = get_parameter(interface, 'name')		

		# Weryfikacja czy w nazwie interfejsu jest ge/xe/et, co oznacza ze jest to interfejs fizyczny
		if any([True if phys_interface in name else False for phys_interface in physical_interfaces]): 
			temp_dict = result.setdefault(name, {})
			for parameter, path in PARAMETERS.items():
				temp_dict[parameter] = int(get_parameter(interface, path))

	return result

if __name__ == '__main__':
	print('Getting data...')
	before = get_data()

	#for i in range(0,5):
	#	print('Waiting 5 seconds - {}s'.format(i+1))
	#	time.sleep(1)

	print('Getting data...')
	after = get_data()
	
	print('{:10} {:15} {:10} {:10} {:10}'.format('Interface', 'Parameter', 'Before', 'After', 'Delta'))
	for interface in before:
		for parameter in PARAMETERS.keys():
			before_value = before[interface][parameter]
			after_value = after[interface][parameter]
			delta = after_value - before_value
			print('{:10} {:15} {:10} {:10} {:10}'.format(interface, parameter, before_value, after_value, delta))
		break
