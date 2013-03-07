import sys
import serial
import argparse
import server2
import time

global debug
debug = False

def main():
    args = parse_args()

    # Initialize some stuff...
    if args.serialport:
        print("Opening serial port: %s" % args.serialport)
        serial_out = serial_in =  serial.Serial(args.serialport, 9600)
    else:
        print("No serial port.  Supply one with the -s port option")
        sys.exit()

    if args.verbose:
        debug = True
    else:
        debug = False

    idx = 0
    while True:
        msg = receive(serial_in)
        if len(msg.split(" ")) == 4: #Don't process junk data
            lines = server2.handle_client(msg)
            send(serial_out, str(len(lines)))
            for v in lines:
                send(serial_out, str(v))
def send(serial_port, message):
    """
    Sends a message back to the client device.
    """
    full_message = ''.join((message, "\n"))

    (debug and
        print("server:" + full_message + ":") )

    reencoded = bytes(full_message, encoding='ascii')
    serial_port.write(reencoded)


def receive(serial_port, timeout=None):
    """
    Listen for a message. Attempt to timeout after a certain number of
    milliseconds.
    """
    raw_message = serial_port.readline()

    debug and print("client:", raw_message, ":")

    message = raw_message.decode('ascii')

    return message.rstrip("\n\r")



def parse_args():
    """
    Parses arguments for this program.
    Returns an object with the following members:
        args.
             serialport -- str
             verbose    -- bool
             graphname  -- str
    """

    parser = argparse.ArgumentParser(
        description='Assignment 1: Map directions.',
        epilog = 'If SERIALPORT is not specified, stdin/stdout are used.')
    parser.add_argument('-s', '--serial',
                        help='path to serial port',
                        dest='serialport',
                        default=None)
    parser.add_argument('-v', dest='verbose',
                        help='verbose',
                        action='store_true')
    parser.add_argument('-g', '--graph',
                        help='path to graph (DEFAULT = " edmonton-roads-2.0.1.txt")',
                        dest='graphname',
                        default=' edmonton-roads-2.0.1.txt')

    return parser.parse_args()

if __name__ == '__main__':
    main()
