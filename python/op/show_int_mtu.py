from jnpr.junos import Device
from lxml import etree
import sys


def get_details(interfaces_xml):
    result = []
    allowed_interfaces = ['ge', 'xe', 'et', 'ae']
    
    for interface in interfaces_xml.iter('physical-interface'):
	name = interface.findtext('name').strip()
	mtu = interface.findtext('mtu').strip()
	speed = interface.findtext('speed').strip()

        drops_xpath = '//physical-interface[normalize-space(name)=$name]/output-error-list/output-drops'
        drops_result = interfaces_xml.xpath(drops_xpath, name=name)
        if len(drops_result) > 0:
            drops = drops_result[0].text.strip()
        else:
            drops = 'N/A'

        if any([True for interface in allowed_interfaces if name[:2] == interface]):
            result.append((name, mtu, speed, drops))
    return result

def main():
    with Device() as dev:
	interfaces_extensive = dev.rpc.get_interface_information(extensive=True)

    if type(interfaces_extensive) != etree._Element:
	print('Blad pobierania danych')
        print('Shoud be ETREE, received: {}'.format(type(interfaces_terse)))
	sys.exit()

    result = get_details(interfaces_extensive)

    print '{:11} {:6} {:12} {:6}'.format('Interface', 'MTU', 'Speed', 'Drops')
    for interface, mtu, speed, drops in result:
        print '{:11} {:6} {:12} {:6}'.format(interface, mtu, speed, drops)
    
if __name__ == '__main__':
    main()


