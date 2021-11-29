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

def get_clean_parameter_with_xpath(query, interface_xml, interface_name):
    """
    Helper function to get a parameter based on XPATH query, if none return Non Available - N/A
    """
    xpath_result = interface_xml.xpath(query, name=interface_name)
    if len(xpath_result) > 0:
        return xpath_result[0].text.strip()
    return 'N/A'

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
        drops = get_clean_parameter_with_xpath('output-error-list/output-drops', interface, name)
        crc = get_clean_parameter_with_xpath('ethernet-mac-statistics/input-crc-errors', interface, name)

        if any([True for interface in allowed_interfaces if name[:2] == interface]):
            result.append((name, description, mtu, speed, drops, crc))
    return result

def print_result(result):
    """ 
    Wyliczenie najdluzszego wyniku z kazdej kolumny
    1. Na poczatku tworze liste 0 i jej dlugosc jest rowna liczbie kolumn.
    2. Dla kazdego interfejsu (res) wyciagam jego wszystkie parametry razem z indexami
    3. Jezeli dlugosc parametru dla danego indeksu jest wieksza niz maksymalna dlugosc dla tego indeksu, to wstawiam ja do listy
    4. Tworze zmienne _length dla kadzego parametru, do kazdej z nich dodaje 1 aby rozsunac od siebie wyniki
    """
    max_length = [0] * len(result[0])
    for res in result:
        for index, value in enumerate(res):
            if len(value) > max_length[index]:
                max_length[index] = len(value)
    int_length, desc_length, mtu_length, speed_length, drops_length, crc_length = [max + 1 for max in max_length]

    print('{:{int_length}} {:{desc_length}} {:{mtu_length}} {:{speed_length}} {:{drops_length}} {:{crc_length}}'.format(
        'Interface', 
        'Description', 
        'MTU', 
        'Speed', 
        'Drops', 
        'CRC', 
        int_length=int_length, 
        desc_length=desc_length,
        mtu_length=mtu_length, 
        speed_length=speed_length, 
        drops_length=drops_length, 
        crc_length=crc_length))

    for interface, description, mtu, speed, drops, crc in result:
        print('{:{int_length}} {:{desc_length}} {:{mtu_length}} {:{speed_length}} {:{drops_length}} {:{crc_length}}'.format(
            interface, 
            description, 
            mtu, 
            speed, 
            drops,
            crc,
            int_length=int_length, 
            desc_length=desc_length,
            mtu_length=mtu_length, 
            speed_length=speed_length, 
            drops_length=drops_length, 
            crc_length=crc_length))
    return True

def main():
    interfaces_extensive = get_data()
    result = get_details(interfaces_extensive)
    print_result(result)
        
if __name__ == '__main__':
    main()