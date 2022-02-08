#!/usr/bin/env python3

import sys
import time
import radical.utils as ru


# ------------------------------------------------------------------------------
#
class Session(object):
    '''
    This class represents the RCT software stack
    '''

    # --------------------------------------------------------------------------
    #
    def __init__(self):
        '''
        Create a ZMQ server to receive 'pilot state updates' (well, termination
        signals in this example).  Each such message will invoke
        `self.boom_handler()'
        '''

        zmq_ep = ru.zmq.Server(uid='demo_app')
        zmq_ep.register_request('boom', self.boom_handler)
        zmq_ep.start()
        ru.write_json('./demo_app.cfg', {'addr': zmq_ep.addr})


    # --------------------------------------------------------------------------
    #
    def boom_handler(self):
        '''
        This handler is invoked when we get a 'boom' message from
        `demo_pilot.py`.
        '''

        # NOTE: this handler is running in a subthread!

        print('\nmake app go boom!')

        # ----------------------------------------------------------------------
        # FIXME: code to trigger exception in the main thread goes here
        # ----------------------------------------------------------------------

        return 'bang bang'


# ------------------------------------------------------------------------------
#
def main(n):
    '''
    This is the application main thread.  It creates a `Session` and then just
    waits for exceptions to happen.

    Thread is *not* owned by RP, but is owned by the application programmer.  As
    such we cannot insert code to listen for signals, can't create `at_exit`
    handlers, can't install signal handlers etc - this is to be left alone!

    n: number of exceptions we expect to receive
    '''

    count = 0
    try:
        Session()

        while count < n:

            try:

                print('.', end='', flush=True)
                time.sleep(1)

            except Exception as e:
                print('ding dong: I got an exception here!  Wohoo!: %s' % e)
                count += 1

    except:
        pass

    finally:
        print('\nfound %d out of %d exceptions' % (count, n))


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    n = int(sys.argv[1])
    main(n)


# ------------------------------------------------------------------------------

