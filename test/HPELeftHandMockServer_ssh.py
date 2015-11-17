# (c) Copyright 2015 Hewlett Packard Enterprise Development LP
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
""" Test SSH server."""

import argparse
import logging
import os
import shlex
import socket
import sys
import threading

import paramiko


paramiko.util.log_to_file('paramiko_server.log')


class CliParseException(Exception):
    pass


class CliArgumentParser(argparse.ArgumentParser):

    def error(self, message):
        usage = super(CliArgumentParser, self).format_help()
        full_message = "%s\r\n%s" % (message, usage)
        raise CliParseException(full_message)

    def parse_args(self, *args):
        return super(CliArgumentParser, self).parse_args(args[1:])


class Cli(object):

    def __init__(self):
        self.log_name = 'paramiko.LeftHandCLI'
        self.logger = paramiko.util.get_logger(self.log_name)

        self.fpgs = {}
        self.vfss = {}

    def do_cli_other(self, *args):
        msg = 'FAIL! Mock SSH CLI does not know how to "%s".' % ' '.join(args)
        self.logger.log(logging.ERROR, msg)
        return msg

    def do_cli_exit(self, *args):
        self.logger.log(logging.INFO, "quiting... g'bye")
        return ''

    def do_cli_quit(self, *args):
        self.logger.log(logging.INFO, "quiting... g'bye")
        return ''

    def process_command(self, cmd):
        self.logger.log(logging.INFO, cmd)
        if cmd is None:
            print("returnNone")
            return ''
        args = shlex.split(cmd)
        if args:
            method = getattr(self, 'do_cli_' + args[0], self.do_cli_other)
            try:
                return method(*args)
            except Exception as cmd_exception:
                return str(cmd_exception)
        else:
            return ''


class ParamikoServer(paramiko.ServerInterface):

    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        return paramiko.OPEN_SUCCEEDED

    def check_auth_none(self, username):
        return paramiko.AUTH_SUCCESSFUL

    def check_auth_password(self, username, password):
        return paramiko.AUTH_SUCCESSFUL

    def check_auth_publickey(self, username, key):
        return paramiko.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username):
        return 'password,publickey,none'

    def check_channel_shell_request(self, c):
        self.event.set()
        return True

    def check_channel_pty_request(self, c, term, width, height, pixelwidth,
                                  pixelheight, modes):
        return True


if __name__ == "__main__":

    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 2200

    key_file = os.path.expanduser('~/.ssh/id_rsa')
    host_key = paramiko.RSAKey(filename=key_file)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', int(port)))
    s.listen(60)
    print("Listening for SSH client connections...")
    connection, address = s.accept()
    transport = None
    channel = None
    try:
        transport = paramiko.Transport(connection)
        transport.load_server_moduli()
        transport.add_server_key(host_key)
        server = ParamikoServer()
        transport.start_server(server=server)

        cliProcessor = Cli()

        while True:
            channel = transport.accept(60)
            if channel is None:
                print("Failed to get SSH channel.")
                sys.exit(1)

            print("Connected")
            server.event.wait(10)

            if not server.event.isSet():
                print("No shell set")
                sys.exit(1)

            fio = channel.makefile('rU')
            commands = []
            command = None
            while not (command == 'exit' or command == 'quit'):
                command = fio.readline().strip('\r\n')
                commands.append(command)

            to_send = '\r\n'.join(commands)
            channel.send(to_send)

            output = ['']
            prompt = "FAKE-LeftHand-CLI cli% "
            for cmd in commands:
                output.append('%s%s' % (prompt, cmd))
                result = cliProcessor.process_command(cmd)
                if result is not None:
                    output.append(result)
            output_to_send = '\r\n'.join(output)
            channel.send(output_to_send)
            channel.close()
            print("Disconnected")

    finally:
        if channel:
            channel.close()
        if transport:
            try:
                transport.close()
                print("transport closed")
            except Exception as e:
                print("transport close exception %s" % e)
                pass
