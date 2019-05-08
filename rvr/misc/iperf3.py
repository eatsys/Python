#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/3/11 16:43
# @Author  : Ethan
# @FileName: pdv.py

#import iperf3
#
#
#class Iperf:
#    def __init__(self, s_ip, c_ip):
#        self.s_ip = s_ip
#        self.c_ip = c_ip
#
#    def server(self):
#        server = iperf3.Server()
#        server.bind_address = c_ip
#        server.port = 6969
#        server.verbose = False
#        while True:
#            server.run()
#
#    def client(self):
#        client = iperf3.Client()
#        client.duration = 1
#        client.server_hostname = s_ip
#        client.port = 5201
#        client.protocol = 'udp'
#
#        print('Connecting to {0}:{1}'.format(client.server_hostname, client.port))
#        result = client.run()
#
#        if result.error:
#            print(result.error)
#        else:
#            print('')
#            print('Test completed:')
#            print('  started at         {0}'.format(result.time))
#            print('  bytes transmitted  {0}'.format(result.bytes))
#            print('  jitter (ms)        {0}'.format(result.jitter_ms))
#            print('  avg cpu load       {0}%\n'.format(result.local_cpu_total))
#
#            print('Average transmitted data in all sorts of networky formats:')
#            print('  bits per second      (bps)   {0}'.format(result.bps))
#            print('  Kilobits per second  (kbps)  {0}'.format(result.kbps))
#            print('  Megabits per second  (Mbps)  {0}'.format(result.Mbps))
#            print('  KiloBytes per second (kB/s)  {0}'.format(result.kB_s))
#            print('  MegaBytes per second (MB/s)  {0}'.format(result.MB_s))
#
#
import logging
from plumbum import local
from plumbum.commands.processes import CommandNotFound, ProcessExecutionError

class IperfError(Exception):
    """Raised when iperf execution fails"""

def run_iperf3_client(server_ip, **kwargs):
    """Run an iperf3 client and return JSON results"""
    iperf3_args = ['-U', '-c', server_ip]

    if kwargs.get('reverse', False):
        iperf3_args.append('-R')

    try:
        iperf3 = local['iperf3']
        print(iperf3(*iperf3_args))
        return iperf3(*iperf3_args)
    except CommandNotFound as err:
        logging.error("%s not found", err.program)
        raise IperfError(err)
    except ProcessExecutionError as err:
        logging.error("%s exited with %d", err.argv[0], err.retcode)
        raise IperfError(err)

if __name__ == '__main__':
    s_ip = '192.168.100.103'
    run_iperf3_client(s_ip)


