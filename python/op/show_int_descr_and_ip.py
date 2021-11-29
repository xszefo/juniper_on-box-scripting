#HelpDescription:Display description and IP information of the interfaces
from jnpr.junos import Device
from lxml import etree
import sys
import argparse

def get_data(interface):
    """
    Function to get a result of the commands: 
    - show interfaces terse
    - show interfaces description
    """
    with Device() as dev:
        if interface is not None:
            interfaces_terse = dev.rpc.get_interface_information(terse=True, interface_name=interface)
            interfaces_description = dev.rpc.get_interface_information(descriptions=True, interface_name=interface)
        else:
            interfaces_terse = dev.rpc.get_interface_information(terse=True)
            interfaces_description = dev.rpc.get_interface_information(descriptions=True)

    if type(interfaces_terse) != etree._Element or type(interfaces_description) != etree._Element:
        print('Blad pobierania danych')
        print('Terse - {}\nDescription - {}'.format(type(interfaces_terse), type(interfaces_description)))
        sys.exit()
    return interfaces_terse, interfaces_description

def get_details(interfaces_terse, interfaces_description):
    """
    Function to extract parameters from the XML result.
    """
    result = []

    for interface in interfaces_description.iter('physical-interface'):
        name = interface.findtext('name').strip()
        description = interface.findtext('description').strip()
        ip_xpath ='//physical-interface[normalize-space(name)=$name]/logical-interface/address-family/interface-address/ifa-local'
        ip_result = interfaces_terse.xpath(ip_xpath, name=name)
        ip = []
        if len(ip_result) > 0:
            for tmp_ip in ip_result:
                ip.append(tmp_ip.text.strip())
        result.append((name, description, ip))
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
    name_length, desc_length, ip_length = [max + 1 for max in max_length]

    print('{:{name_length}} {:{desc_length}} {:{ip_length}}'.format(
        'Name', 
        'Description', 
        'IP', 
        name_length=name_length, 
        desc_length=desc_length, 
        ip_length=ip_length))

    for name, description, ips in result:
        if len(ips) > 0:
            print('{:{name_length}} {:{desc_length}} {:{ip_length}}'.format(
                name, 
                description, 
                ips[0], 
                name_length=name_length, 
                desc_length=desc_length, 
                ip_length=ip_length))
            for ip in ips[1:]:
                print('{:{name_length}} {:{desc_length}} {:{ip_length}}'.format(
                '',
                '', 
                ip,
                name_length=name_length, 
                desc_length=desc_length, 
                ip_length=ip_length))
        else:
            print('{:{name_length}} {:{desc_length}}'.format(
                name, 
                description,
                name_length=name_length, 
                desc_length=desc_length))
    return True

arguments = {'interface': 'Name of interface to display'}

def main():
    parser = argparse.ArgumentParser(description='Script to get description and IP addresses of the interfaces.')
    for key in arguments:
        parser.add_argument(('-' + key), required=False, help=arguments[key])
    args = parser.parse_args()
    interface = args.interface

    interfaces_terse, interfaces_description = get_data(interface)
    result = get_details(interfaces_terse, interfaces_description)
    print_result(result)

if __name__ == '__main__':
    main()