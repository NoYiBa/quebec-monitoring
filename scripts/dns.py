#!/usr/bin/env python
# -*- coding: utf-8 -*-

DNS = {
    # Cogeco Cable (Trois-rivieres) 
    'cogeco.ca': ['205.151.69.200','205.151.68.200'],
    
    # Sympatico.ca (BELL)
    'sympatico.ca': ['198.235.216.110', '209.226.175.224', '206.47.244.90',
                  '206.47.244.53', '206.47.244.54', '198.235.216.1',
                  '198.235.216.2', '198.235.216.130', '198.235.216.131'],
    
    # Telus
    'telusquebec.com': ['142.169.1.16', '199.84.242.22'],
    
    # Videotron.CA 
    'videotron.ca': ['205.151.222.250', '205.151.222.251', '24.200.241.2',
                  '24.200.241.6', '24.200.241.10', '24.200.243.234',
                  '24.200.243.242', '24.200.243.250', '24.201.245.106',
                  '24.201.245.114'],
    
    # Videotron.NET
    'videotron.net': ['205.151.222.254', '205.151.222.253'],
    
    # Colbanet
    'colba.net': ['216.252.64.75', '216.252.64.76', '69.28.239.8',
                 '74.116.184.9', '69.28.239.9', '74.116.184.8'],

    # Cooptel
    'cooptel.qc.ca': ['216.144.115.241', '216.144.115.242'],

    # Fido
    'fido.ca': ['204.92.15.211', '204.92.15.212', '64.71.255.205', '64.71.255.253']
    }


prefix = (
"""
""")

template_host = (
"""
define host {
       use                      generic-host
       host_name                %(host)s
       address                  %(host)s
       alias                    %(host)s
       check_command            check_dummy!0!OK
}
""")

template_service = (
"""
define service {
       use                      generic-service
       host_name                %(host)s
       check_command            check_dig_service!%(ip)s!www.gouv.qc.ca
       display_name             %(host)s (%(ip)s)
       service_description      %(ip)s
       servicegroups            group-dns
       labels                   order_%(order)d
}
""")

postfix = (
"""
define host {
       use                            generic-host
       host_name                      DNS
       alias                          DNS
       check_command                  check_dummy!0!OK
}
define service {
       use                              generic-service
       host_name                        DNS
       service_description              DNS
       hostgroups                       group-dns
       check_command                    bp_rule!%(all_dns)s
       business_rule_output_template    $(x)$
       servicegroups                    group-dns
       labels                           order_0
       icon_image                       fa-gears
}
""")


def main():
    print prefix
    all_dns = []
    order = 1
    for host, ips in DNS.iteritems():
        print template_host % {'host': host}
        for ip in ips:
            print template_service % {'host': host, 'ip': ip, 'order': order}
            all_dns.append('%(host)s,%(ip)s' % {'host': host, 'ip': ip})
            order += 1
    print postfix % {'all_dns': '&'.join(all_dns)}
        

if __name__ == '__main__':
    main()
