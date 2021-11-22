#HelpDescription:Display description and IP information of the interfaces
from jnpr.junos import Device
from lxml import etree
import sys
import argparse

def get_data(interface):
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
    print('{:15} {:20} {:15}'.format('Name', 'Description', 'IP'))
    for name, description, ips in result:
        if len(ips) > 0:
            print('{:15} {:20} {:15}'.format(name, description, ips[0]))
            for ip in ips[1:]:
                print('{:15} {:20} {:15}'.format('','', ip))
        else:
            print('{:15} {:20}'.format(name, description))
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