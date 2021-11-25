0#HelpDescription:Display MTU, Speed and Drops of the interfaces
from jnpr.junos import Device
from lxml import etree
import sys

def get_clean_parameter(interface, parameter):
    """
    Helper function to get a parameter of a given interface, if none return blank string
    """
    try:
        return interface.findtext(parameter).strip()
    except AttributeError:
        return ''

def get_data():
    """
    Function to get a result of the command: show interfaces extensive
    """
    with Device() as dev:
	    interfaces_extensive = dev.rpc.get_interface_information(extensive=True)

    if type(interfaces_extensive) != etree._Element:
        print('Wrong data format')
        print('Should be ETREE, received: {}'.format(type(interfaces_extensive)))
        sys.exit()
    return interfaces_extensive

def get_details(interfaces_xml):
    """
    Function to extract parameters from the XML result.
    """
    result = []
    allowed_interfaces = ['ge', 'xe', 'et', 'ae']

    for interface in interfaces_xml.iter('physical-interface'):
        name = get_clean_parameter(interface, 'name')
        description = get_clean_parameter(interface, 'description')
        mtu = get_clean_parameter(interface, 'mtu')
        speed = get_clean_parameter(interface, 'speed')
        drops_xpath = '//physical-interface[normalize-space(name)=$name]/output-error-list/output-drops'
        drops_result = interfaces_xml.xpath(drops_xpath, name=name)
        if len(drops_result) > 0:
            drops = drops_result[0].text.strip()
        else:
            drops = 'N/A'
        if any([True for interface in allowed_interfaces if name[:2] == interface]):
            result.append((name, description, mtu, speed, drops))
    return result

def print_result(result):
    print('{:11} {:20} {:6} {:12} {:6}'.format('Interface', 'Description', 'MTU', 'Speed', 'Drops'))
    for interface, description, mtu, speed, drops in result:
        print('{:11} {:20} {:6} {:12} {:6}'.format(interface, description, mtu, speed, drops))
    return True

def main():
    interfaces_extensive = get_data()
    result = get_details(interfaces_extensive)
    print_result(result)
    
if __name__ == '__main__':
    main()


