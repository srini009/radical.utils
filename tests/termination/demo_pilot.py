#!/usr/bin/env python3

import sys
import time
import radical.utils as ru


# ------------------------------------------------------------------------------
#
def main(n):
    '''
    once per second send a signal to the demo app server
    '''

    zmq_ep = ru.zmq.Client('demo_app')

    for i in range(n):
        print('.', end='', flush=True)
        reply = zmq_ep.request('boom')
        print('%3d: server replied: %s' % (i, reply))
        time.sleep(1)


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    n = int(sys.argv[1])
    main(n)


# ------------------------------------------------------------------------------

