#!/usr/bin/env python2.7
# encoding: utf-8
'''
tracer.py

Created by Karl Dubost on 2014-09-10.
Copyright (c) 2014 Grange. All rights reserved.
see LICENSE.TXT
'''
import sys
import threading


def show_guts(f):
    sentinel = object()
    gutsdata = threading.local()
    gutsdata.captured_locals = None
    gutsdata.tracing = False

    def trace_locals(frame, event, arg):
        if event.startswith('c_'):  # C code traces, no new hook
            return
        if event == 'call':  # start tracing only the first call
            if gutsdata.tracing:
                return None
            gutsdata.tracing = True
            return trace_locals
        if event == 'line':  # continue tracing
            return trace_locals

        # event is either exception or return, capture locals, end tracing
        gutsdata.captured_locals = frame.f_locals.copy()
        return None

    def wrapper(*args, **kw):
        # preserve existing tracer, start our trace
        old_trace = sys.gettrace()
        sys.settrace(trace_locals)

        retval = sentinel
        try:
            retval = f(*args, **kw)
        finally:
            # reinstate existing tracer, report, clean up
            sys.settrace(old_trace)
            print('-' * 80)
            for key, val in gutsdata.captured_locals.items():
                print('{}: {!r}'.format(key, val))
            if retval is not sentinel:
                print('Returned: {!r}'.format(retval))
            print('-' * 80)
            gutsdata.captured_locals = None
            gutsdata.tracing = False

        return retval
    return wrapper
