import unittest2

from nose.plugins.attrib import attr
import mock
from reportbug import utils
from reportbug import debbugs

import urllib
import re

class TestDebianbts(unittest2.TestCase):

    def test_get_tags(self):

        # for each severity, for each mode
        self.assertItemsEqual(debbugs.get_tags('critical', utils.MODE_NOVICE).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'security', 'patch', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('grave', utils.MODE_NOVICE).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'security', 'patch', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('serious', utils.MODE_NOVICE).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'security', 'patch', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('important', utils.MODE_NOVICE).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'patch', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('does-not-build', utils.MODE_NOVICE).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'patch', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('normal', utils.MODE_NOVICE).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'patch', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('non-critical', utils.MODE_NOVICE).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'patch', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('minor', utils.MODE_NOVICE).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'patch', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('wishlist', utils.MODE_NOVICE).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'patch', 'newcomer'])

        self.assertItemsEqual(debbugs.get_tags('critical', utils.MODE_STANDARD).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'security', 'patch', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('grave', utils.MODE_STANDARD).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'security', 'patch', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('serious', utils.MODE_STANDARD).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'security', 'patch', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('important', utils.MODE_STANDARD).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'patch', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('does-not-build', utils.MODE_STANDARD).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'patch', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('normal', utils.MODE_STANDARD).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'patch', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('non-critical', utils.MODE_STANDARD).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'patch', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('minor', utils.MODE_STANDARD).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'patch', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('wishlist', utils.MODE_STANDARD).keys(), ['lfs', 'l10n', 'd-i', 'upstream', 'ipv6', 'patch', 'newcomer'])

        self.assertItemsEqual(debbugs.get_tags('critical', utils.MODE_ADVANCED).keys(), ['l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('grave', utils.MODE_ADVANCED).keys(), ['l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('serious', utils.MODE_ADVANCED).keys(), ['l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('important', utils.MODE_ADVANCED).keys(), ['l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('does-not-build', utils.MODE_ADVANCED).keys(), ['l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('normal', utils.MODE_ADVANCED).keys(), ['l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('non-critical', utils.MODE_ADVANCED).keys(), ['l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('minor', utils.MODE_ADVANCED).keys(), ['l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('wishlist', utils.MODE_ADVANCED).keys(), ['l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'newcomer'])

        self.assertItemsEqual(debbugs.get_tags('critical', utils.MODE_EXPERT).keys(), ['l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('grave', utils.MODE_EXPERT).keys(), ['l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('serious', utils.MODE_EXPERT).keys(), ['l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('important', utils.MODE_EXPERT).keys(), ['l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('does-not-build', utils.MODE_EXPERT).keys(), ['l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('normal', utils.MODE_EXPERT).keys(), ['l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('non-critical', utils.MODE_EXPERT).keys(), ['l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('minor', utils.MODE_EXPERT).keys(), ['l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'newcomer'])
        self.assertItemsEqual(debbugs.get_tags('wishlist', utils.MODE_EXPERT).keys(), ['l10n', 'd-i', 'ipv6', 'patch', 'lfs', 'upstream', 'security', 'newcomer'])


class TestInfofunc(unittest2.TestCase):

    def test_dpkg_infofunc(self):
        info = debbugs.dpkg_infofunc()
        arch = utils.get_arch()
        self.assertIn('Architecture:', info)
        self.assertIn(arch, info)
        self.assertIn('Architecture: ' + arch, info)
        self.assertTrue(info.endswith('\n\n'))

        # save original method
        __save1 = utils.get_arch
        __save2 = utils.get_multiarch

        utils.get_arch = mock.MagicMock(return_value = 'non-existing-arch')
        info = debbugs.dpkg_infofunc()
        self.assertIn('non-existing-arch', info)
        self.assertTrue(info.endswith('\n\n'))

        # test with get_arch() returning None
        utils.get_arch = mock.MagicMock(return_value = None)
        info = debbugs.dpkg_infofunc()
        self.assertIn('Architecture: ?', info)
        self.assertTrue(info.endswith('\n\n'))

        # test with a dummy m-a setup
        utils.get_multiarch = mock.MagicMock(return_value = 'multi-arch-ified')
        info = debbugs.dpkg_infofunc()
        self.assertIn('Foreign Architectures:', info)
        self.assertIn('multi-arch-ified', info)
        self.assertIn('Foreign Architectures: multi-arch-ified', info)

        utils.get_arch = __save1
        utils.get_multiarch = __save2
        del __save1
        del __save2

    def test_debian_infofunc(self):
        info = debbugs.debian_infofunc()
        self.assertIn('Architecture:', info)

    def test_ubuntu_infofunc(self):
        info = debbugs.ubuntu_infofunc()
        self.assertIn('Architecture:', info)

    def test_generic_infofunc(self):
        info = debbugs.generic_infofunc()
        self.assertIn('Architecture:', info)

class TestMiscFunctions(unittest2.TestCase):

    def test_yn_bool(self):
        self.assertEqual(debbugs.yn_bool(None), 'no')
        self.assertEqual(debbugs.yn_bool('no'), 'no')
        self.assertEqual(debbugs.yn_bool('yes'), 'yes')
        self.assertEqual(debbugs.yn_bool('dummy string'), 'yes')

    def test_convert_severity(self):

        # lists of bts systems, severity and the expected value in return
        sevs = [('debbugs', 'critical', 'critical'),
                ('debbugs', 'non-critical', 'normal'),
                (None, 'dummy', 'dummy'),
                ('gnats', 'important', 'serious'),
                ('gnats', 'dummy', 'dummy')]

        for type, severity, value in sevs:
            self.assertEqual(debbugs.convert_severity(severity, type), value)

    @attr('network') #marking the test as using network
    @unittest2.skip("Need to talk with dondelelcaro about make them sync")
    def test_pseudopackages_in_sync(self):

        dictparse = re.compile(r'([^\s]+)\s+(.+)',re.IGNORECASE)

        bdo_list = {}
        pseudo = urllib.urlopen('https://bugs.debian.org/pseudopackages/pseudo-packages.description')
        for l in pseudo:
            m = dictparse.search(l)
            bdo_list[m.group(1)] = m.group(2)

        self.maxDiff = None
        self.assertEqual(debbugs.debother, bdo_list)


class TestGetReports(unittest2.TestCase):

    @attr('network') #marking the test as using network
    def test_get_cgi_reports(self):

        data = debbugs.get_cgi_reports('reportbug', timeout=60)
        self.assertGreater(data[0], 0)


    @attr('network') #marking the test as using network
    def test_get_reports(self):

        data = debbugs.get_reports('reportbug', timeout=60)
        self.assertGreater(data[0], 0)

    @attr('network') #marking the test as using network
    def test_get_report(self):

        buginfo, bodies = debbugs.get_report(415801, 120)
        self.assertEqual(buginfo.bug_num, 415801)
        self.assertEqual(buginfo.subject,
                         'reportbug: add support for SOAP interface to BTS')

        # relative to bts#637994, report with messages without a header
        buginfo, bodies = debbugs.get_report(503300, 120)
        self.assertGreater(len(bodies), 0)

    @attr('network') #marking the test as using network
    def test_bts796759(self):

        # verify accessing WNPP happens correctly, now that BTS
        # access has to be done in batches
        data = debbugs.get_reports('wnpp', 120, source=True)
        self.assertGreater(data[0], 0)

class TestUrlFunctions(unittest2.TestCase):

    def test_cgi_report_url(self):

        self.assertEqual(debbugs.cgi_report_url('debian', 123),
                         'https://bugs.debian.org/cgi-bin/bugreport.cgi?' +
                             'bug=123&archived=False&mbox=no')
        self.assertIsNone(debbugs.cgi_report_url('default', 123))

    def test_cgi_package_url(self):

        self.assertEqual(debbugs.cgi_package_url('debian', 'reportbug'),
                         'https://bugs.debian.org/cgi-bin/pkgreport.cgi?' +
                             'archived=no&pkg=reportbug&repeatmerged=yes')
        self.assertEqual(debbugs.cgi_package_url
                         ('debian', 'reportbug', source=True),
                         'https://bugs.debian.org/cgi-bin/pkgreport.cgi?src=' +
                             'reportbug&archived=no&repeatmerged=yes')
        self.assertEqual(debbugs.cgi_package_url
                         ('debian', 'reportbug', version='5.0'),
                         'https://bugs.debian.org/cgi-bin/pkgreport.cgi?archi' +
                         'ved=no&version=5.0&pkg=reportbug&repeatmerged=yes')


    def test_get_package_url(self):

        self.assertEqual(debbugs.get_package_url('debian', 'reportbug'),
                         'https://bugs.debian.org/cgi-bin/pkgreport.cgi?archi' +
                         'ved=no&pkg=reportbug&repeatmerged=yes')

    def test_get_report_url(self):

        self.assertEqual(debbugs.get_report_url('debian', 123),
                         'https://bugs.debian.org/cgi-bin/bugreport.cgi?' +
                         'bug=123&archived=False&mbox=no')
