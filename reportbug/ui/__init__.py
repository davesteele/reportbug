#!/usr/bin/python -S
# -*- python -*-
# reportbug - Report a bug in the Debian distribution.
#   Written by Chris Lawrence <lawrencc@debian.org>
#   Copyright (C) 1999-2008 Chris Lawrence
#
# This program is freely distributable per the following license:
#
##  Permission to use, copy, modify, and distribute this software and its
##  documentation for any purpose and without fee is hereby granted,
##  provided that the above copyright notice appears in all copies and that
##  both that copyright notice and this permission notice appear in
##  supporting documentation.
##
##  I DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING ALL
##  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL I
##  BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY
##  DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
##  WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
##  ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
##  SOFTWARE.
#
# $Id: reportbug.py,v 1.35.2.24 2008-04-18 05:38:28 lawrencc Exp $


__all__ = ['text_ui', 'urwid_ui', 'newt_ui', 'gtk2_ui']

UIS = {'text': 'A text-oriented console user interface',
       'urwid': 'A menu-based console user interface',
       'newt': 'A newt user interface',
       'gtk2': 'A graphical (GTK+) user interface'}

AVAILABLE_UIS = []

for uis in UIS.keys():
    try:
        # let's try to import the ui...
        ui_module = __import__('reportbug.ui', fromlist=[uis+'_ui'])
        # ... and check if it's really imported
        ui = getattr(ui_module, uis+'_ui')
        # then we can finally add it to AVAILABLE_UIS
        AVAILABLE_UIS.append(uis)
    except:
        # we can't import uis, so just skip it
        pass