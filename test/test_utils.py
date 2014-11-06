import unittest2

from reportbug import utils
import os.path
import platform
from nose.plugins.attrib import attr
import debianbts
import mock
import commands

class TestUtils(unittest2.TestCase):

    def test_modes_and_modelist(self):
        """Check MODES items and MODELIST are in sync"""

        self.assertItemsEqual(utils.MODES.keys(), utils.MODELIST)

class TestEmail(unittest2.TestCase):

    def test_check_email_addr(self):
        
        real_addr = 'reportbug-maint@lists.alioth.debian.org'

        self.assertTrue(utils.check_email_addr(real_addr))
        self.assertFalse(utils.check_email_addr('dummy'))
        self.assertFalse(utils.check_email_addr('nouser@nodomain'))
        self.assertFalse(utils.check_email_addr('.nouser@nodomain'))
        self.assertFalse(utils.check_email_addr('nouser.@nodomain'))
        self.assertFalse(utils.check_email_addr('nouser@.nodomain'))
        self.assertFalse(utils.check_email_addr('nouser@nodomain.'))
        self.assertFalse(utils.check_email_addr('too@many@at@signs'))

    def test_get_email_addr(self):

        email = 'Reportbug Maintainers <reportbug-maint@lists.alioth.debian.org>'
        name, email_addr = utils.get_email_addr(email)

        self.assertEqual(name, 'Reportbug Maintainers')
        self.assertEqual(email_addr, 'reportbug-maint@lists.alioth.debian.org')

    def test_get_email(self):

        name = 'Reportbug Maintainers'
        mail = 'reportbug-maint@lists.alioth.debian.org'

        n, m = utils.get_email(mail, name)

        self.assertEqual(name, n)
        self.assertEqual(mail, m)

    def test_get_user_id(self):

        name = 'Reportbug Maintainers'
        mail = 'reportbug-maint@lists.alioth.debian.org'
        addr = utils.get_user_id(mail, name)
        self.assertEqual(addr, "%s <%s>" % (name, mail))

        name = 'test'
        mail = 'faked'
        addr = utils.get_user_id(mail, name)
        self.assertIn(mail+'@', addr)

        mail = 'Reportbug Maintainers <reportbug-maint@lists.alioth.debian.org>'
        addr = utils.get_user_id(mail)
        self.assertEqual(mail, addr)

        mail = 'reportbug-maint@lists.alioth.debian.org'
        addr = utils.get_user_id(mail)
        self.assertIn(mail, addr)


    def test_find_rewritten(self):
        unittest2.skip("Is utils.find_rewritten actually useful to someone? deprecate it?")

class TestPackages(unittest2.TestCase):

    def test_get_package_status(self):

        status = utils.get_package_status('non-existing-package')

        (pkgversion, pkgavail, depends, recommends, conffiles, maintainer,
         installed, origin, vendor, reportinfo, priority, desc, src_name,
         fulldesc, state, suggests, section) = status

        self.assertIsNone(pkgversion)
        self.assertIsNone(pkgavail)
        self.assertEqual(depends, ())
        self.assertEqual(recommends, ())
        self.assertEqual(conffiles, ())
        self.assertIsNone(maintainer)
        self.assertFalse(installed)
        self.assertIsNone(origin)
        self.assertEqual(vendor, '')
        self.assertIsNone(reportinfo)
        self.assertIsNone(priority)
        self.assertIsNone(desc)
        self.assertIsNone(src_name)
        self.assertEqual(fulldesc, '')
        self.assertEqual(state, '')
        self.assertEqual(suggests, ())
        self.assertIsNone(section)

        # Using an 'Essential: yes' package, what's better than 'dpkg'?
        status = utils.get_package_status('dpkg')

        (pkgversion, pkgavail, depends, recommends, conffiles, maintainer,
         installed, origin, vendor, reportinfo, priority, desc, src_name,
         fulldesc, state, suggests, section) = status

        self.assertIsNotNone(pkgversion)
        self.assertEqual(pkgavail, 'dpkg')
        # let's just check Depends is not null
        self.assertIsNotNone(depends)
        self.assertIsNotNone(maintainer)
        self.assertTrue(installed)
        self.assertEqual(origin, 'debian')
        self.assertEqual(priority, 'required')
        self.assertIsNotNone(desc)
        self.assertIsNotNone(fulldesc)
        self.assertEqual(state, 'installed')
        self.assertEqual(section, 'admin')

        # it exploits the 'statuscache', it's already called before
        # so it's now in the cache
        status = utils.get_package_status('dpkg')

        status = utils.get_package_status('reportbug', avail=True)

        (pkgversion, pkgavail, depends, recommends, conffiles, maintainer,
         installed, origin, vendor, reportinfo, priority, desc, src_name,
         fulldesc, state, suggests, section) = status

        self.assertIsNotNone(pkgversion)
        self.assertEqual(pkgavail, 'reportbug')
        # let's just check Depends is not null
        self.assertIsNotNone(depends)
        self.assertIsNotNone(maintainer)
        self.assertEqual(priority, 'standard')
        self.assertIsNotNone(desc)
        self.assertIsNotNone(fulldesc)

        status = utils.get_package_status('python-matplotlib')

        (pkgversion, pkgavail, depends, recommends, conffiles, maintainer,
         installed, origin, vendor, reportinfo, priority, desc, src_name,
         fulldesc, state, suggests, section) = status

        self.assertIsNotNone(recommends)


    def test_get_changed_config_files(self):

        status = utils.get_package_status('dpkg')

        (pkgversion, pkgavail, depends, recommends, conffiles, maintainer,
         installed, origin, vendor, reportinfo, priority, desc, src_name,
         fulldesc, state, suggests, section) = status

        confinfo, changed = utils.get_changed_config_files(conffiles)
        self.assertIsNotNone(confinfo)

    def test_find_package_for(self):
        result = utils.find_package_for('dpkg')
        self.assertNotEqual(result[1], {})

        filename = 'reportbug-bugfree'
        result = utils.find_package_for(filename, pathonly=True)
        self.assertEqual(result[0], filename)
        self.assertIsNone(result[1])

        result = utils.find_package_for('/usr/bin/reportbug')
        self.assertNotEqual(result[1], {})

        result = utils.find_package_for('/var/lib/dpkg/info/reportbug.md5sums')
        self.assertNotEqual(result[1], {})

        result = utils.find_package_for('/usr/bin/')
        self.assertNotEqual(result[1], {})

    def test_get_package_info(self):

        result = utils.get_package_info([])
        self.assertEqual(result, [])

        pkg = 'reportbug'
        result = utils.get_package_info([((pkg,), pkg)])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], pkg)

        # open package surely not available on my client systems
        #to cover line 568
        pkg = 'slapd'
        result = utils.get_package_info([((pkg,), pkg)])

        self.assertEqual(result[0][0], pkg)
        self.assertEqual(result[0][2], '<none>')

        result = utils.get_package_info([((pkg,), pkg)], skip_notfound=True)

        self.assertEqual(result, [])

        # package with a Provides
        #pkg = 'emacs'
        #result = utils.get_package_info([((pkg,), pkg)])

        #self.assertEqual(result[0][0], pkg)

    def test_packages_providing(self):
        pkg = 'editor'
        result = utils.packages_providing(pkg)

        self.assertGreater(len(result), 0)

    def test_get_avail_database(self):
        
        avail_db = utils.get_avail_database()
        entry = avail_db.next()
        self.assertIsNotNone(entry)

    def test_available_package_description(self):

        descr = utils.available_package_description('reportbug')
        self.assertEquals(descr, 'reports bugs in the Debian distribution')

        descr = utils.available_package_description('reportbug-bugfree')
        self.assertIsNone(descr)

class TestSourcePackages(unittest2.TestCase):

    #@unittest2.skip("Too slow")
    def test_get_source_name(self):
        binpkg = 'python-reportbug'
        src = utils.get_source_name(binpkg)
        self.assertEqual(src, 'reportbug')

        src = utils.get_source_name('reportbug-bugfree')
        self.assertIsNone(src)

    #@unittest2.skip("Too slow")
    def test_get_source_package(self):
        src = 'reportbug'
        binpkgs = utils.get_source_package(src)
        self.assertItemsEqual([bin[0] for bin in binpkgs], ['python-reportbug', 'reportbug'])

        bin = 'python-reportbug'
        binpkgs_frombin = utils.get_source_package(bin)
        self.assertEqual(binpkgs, binpkgs_frombin)

class TestSystemInformation(unittest2.TestCase):

    def test_get_cpu_cores(self):

        cores = utils.get_cpu_cores()
        self.assertGreaterEqual(cores, 1)


    def test_lsb_release_info(self):

        res = utils.lsb_release_info()
        self.assertIn('Debian', res)

    def test_get_running_kernel_pkg(self):

        package = utils.get_running_kernel_pkg()

        self.assertIn(platform.release(), package)

    def test_get_multiarch(self):

        orig = commands.getoutput

        commands.getoutput = mock.MagicMock(return_value = '')
        multiarch = utils.get_multiarch()
        self.assertEqual(multiarch, '')

        commands.getoutput = mock.MagicMock(return_value = 'i386')
        multiarch = utils.get_multiarch()
        self.assertEqual(multiarch, 'i386')

        commands.getoutput = mock.MagicMock(return_value = 'i386\namd64')
        multiarch = utils.get_multiarch()
        self.assertItemsEqual(multiarch.split(', '), ['i386', 'amd64'])

        commands.getoutput = orig

class TestMua(unittest2.TestCase):

    def test_mua_is_supported(self):

        for mua in ('mh', 'nmh', 'gnus', 'mutt', 'claws-mail'):
            self.assertTrue(utils.mua_is_supported(mua))

        self.assertFalse(utils.mua_is_supported('mua-of-my-dreams'))

    def test_mua_exists(self):

        for mua in ('mh', 'nmh', 'gnus', 'mutt', 'claws-mail'):
            if not utils.mua_exists(mua):
                self.fail("%s MUA program not available" % mua)

    def test_mua_name(self):

        for mua in ('mh', 'nmh', 'gnus', 'mutt', 'claws-mail'):
            self.assertIsInstance(utils.mua_name(mua), utils.Mua)

        self.assertEqual(utils.mua_name('mua-of-my-dreams'), 'mua-of-my-dreams')


class TestBugreportBody(unittest2.TestCase):

    def test_get_dependency_info(self):

        pkg = 'reportbug'
        result = utils.get_dependency_info('reportbug', '')

        self.assertIn('no packages', result)

        result = utils.get_dependency_info('reportbug', [['dpkg']])
        self.assertIn('dpkg', result)

        # check for the provides stuff
        result = utils.get_dependency_info('reportbug', [['awk']])
        self.assertIn('awk', result)


    def test_bts657753(self):
        # check that non-existing deps gets a correct installation info
        # and not just the last one applied to anyone
        result = utils.get_dependency_info('reportbug',
                                           (('reportbug',), ('nonexisting',)))
        for line in result.split('\n'):
            if 'nonexisting' in line:
                self.assertFalse(line.startswith('ii'))

    def test_bts650659(self):
        # verify that the dependency list doesn't have tailing white spaces

        status = utils.get_package_status('reportbug')
        (pkgversion, pkgavail, depends, recommends, conffiles, maintainer,
         installed, origin, vendor, reportinfo, priority, desc, src_name,
         fulldesc, state, suggests, section) = status

        for l in [depends, recommends, suggests]:
            result = utils.get_dependency_info('reportbug', l)
            for line in result.split('\n'):
                self.assertEqual(line.rstrip(), line)

    def test_cleanup_msg(self):

        message = """Subject: unblock: reportbug/4.12.6
Package: release.debian.org
User: release.debian.org@packages.debian.org
Usertags: unblock
Severity: normal
Morph: cool
Continuation:
 header

Please unblock package reportbug

(explain the reason for the unblock here)

unblock reportbug/4.12.6

-- System Information:
Debian Release: squeeze/sid
  APT prefers unstable
  APT policy: (500, 'unstable'), (1, 'experimental')
Architecture: amd64 (x86_64)

Kernel: Linux 2.6.31-1-amd64 (SMP w/4 CPU cores)
Locale: LANG=en_US.UTF-8, LC_CTYPE=en_US.UTF-8 (charmap=UTF-8)
Shell: /bin/sh linked to /bin/bash"""
        header = [u'X-Debbugs-CC: reportbug@packages.qa.debian.org']
        pseudos = ['Morph: cool']
        rtype = 'debbugs'
        body, headers, pseudo = utils.cleanup_msg(message, header, pseudos,
                                                  rtype)

        # check body content
        self.assertIn('reportbug/4.12.6', body)
        self.assertIn('System Information', body)

        # check expected headers are there
        h = dict(headers)
        self.assertIn('Subject', h)
        self.assertIn('X-Debbugs-CC', h)

        # check expected pseudo headers are there
        p = dict([p.split(': ') for p in pseudo])
        self.assertIn('Package', p)
        self.assertIn('Severity', p)
        self.assertIn('User', p)
        self.assertIn('Usertags', p)
        self.assertIn('Morph', p)


    @attr('network') #marking the test as using network
    def test_generate_blank_report(self):

        report = utils.generate_blank_report('reportbug', '1.2.3', 'normal',
                                             '', '', '', type='debbugs')
        self.assertIsNotNone(report)
        self.assertIn('Package: reportbug', report)
        self.assertIn('Version: 1.2.3', report)
        self.assertIn('Severity: normal', report)

        report = utils.generate_blank_report('reportbug', '1.2.3', 'normal',
                                             '', '', '', type='debbugs',
                                             issource=True)
        self.assertIn('Source: reportbug', report)

        # test with exinfo (represents the bug number if this is a followup):
        # int, string, unconvertible (to int) datatype
        report = utils.generate_blank_report('reportbug', '1.2.3', 'normal',
                                             '', '', '', type='debbugs',
                                             exinfo=123456)
        self.assertIn('Followup-For: Bug #123456', report)

        bug = debianbts.get_status(123456)[0]
        report = utils.generate_blank_report('reportbug', '1.2.3', 'normal',
                                             '', '', '', type='debbugs',
                                             exinfo=bug)
        self.assertIn('Followup-For: Bug #123456', report)

        with self.assertRaises(TypeError):
            report = utils.generate_blank_report('reportbug', '1.2.3', 'normal',
                                                 '', '', '', type='debbugs',
                                                 exinfo={'123456': ''})

class TestConfig(unittest2.TestCase):

    # Use an "internal" file for testing
    def setUp(self):
        self._FILES = utils.FILES
        utils.FILES = [os.path.dirname(__file__) + '/data/reportbug.conf']

    def tearDown(self):
        utils.FILES = self._FILES

    def test_parse_config_files(self):

        desired_conf = {
            'bts': 'debian',
            'check_available': True,
            'check_uid': False,
            'debconf': False,
            'dontquery': False,
            'editor': u'emacs -nw',
            'email': u'reportbug-maint@lists.alioth.debian.org',
            'envelopefrom': u'reportbug-maint@lists.alioth.debian.org',
            'headers': ['X-Reportbug-Testsuite: this is the test suite'],
            'http_proxy': u'http://proxy.example.com:3128/',
            'interface': 'gtk2',
            'keyid': u'deadbeef',
            'max_attachment_size': 1024000,
            'mbox_reader_cmd': u'mutt -f %s',
            'mirrors': ['this_is_a_bts_mirror'],
            'mode': 'novice',
            'mta': u'/usr/sbin/sendmail',
            'nocc': False,
            'nocompress': False,
            'noconf': False,
            'offline': True,
            'paranoid': True,
            'query_src': False,
            'realname': u'Reportbug Maintainers',
            'replyto': u'We dont care <dev@null.org>',
            'sendto': 'submit',
            'severity': 'normal',
            'sign': 'gpg',
            'smtphost': u'reportbug.debian.org:587',
            'smtppasswd': u'James Bond',
            'smtptls': True,
            'smtpuser': u'Bond',
            'template': True,
            'verify': True}

        args = utils.parse_config_files()
        for conf in desired_conf:
            self.assertIn(conf, args)
            self.assertEqual(desired_conf[conf], args[conf])

        # mua returns an instance of utils.Mua, need to check differently
        self.assertIn('mua', args)
        self.assertIsInstance(args['mua'], utils.Mua)

    def test_bts579891(self):
        lex = utils.our_lex('realname "Paul \\"TBBle\\" Hampson"', posix=True)
        option = lex.get_token()
        self.assertEqual(option, 'realname')
        realname = lex.get_token()
        self.assertEqual(realname, 'Paul "TBBle" Hampson')


class TestControl(unittest2.TestCase):

    def test_parse_bug_control_file(self):

        ctrl_file = os.path.dirname(__file__) + '/data/control'

        submitas, submitto, reportwith, supplemental = \
            utils.parse_bug_control_file(ctrl_file)

        self.assertEquals(submitas, 'reportbug2')
        self.assertEquals(submitto, 'reportbug-maint@lists.alioth.debian.org')
        self.assertIn('python', reportwith)
        self.assertIn('perl', reportwith)
        self.assertIn('python', supplemental)
        self.assertIn('perl', supplemental)

class TestPaths(unittest2.TestCase):

    def test_search_path_for(self):

        p = 'not-existing'
        res = utils.search_path_for(p)
        self.assertIsNone(res)

        p = '/tmp'
        res = utils.search_path_for(p)
        self.assertEquals(p, res)

        p = 'dpkg'
        res = utils.search_path_for(p)
        self.assertEquals(res, '/usr/bin/dpkg')

class TestEditor(unittest2.TestCase):

    def test_which_editor(self):

        res = utils.which_editor()
        self.assertIsNotNone(res)

        e = 'reportbug-editor'
        res = utils.which_editor(e)
        self.assertEquals(e, res)
        
class TestSearch(unittest2.TestCase):

    def test_search_pipe(self):

        f = 'reportbug'

        dlocate = True
        pipe, dloc = utils.search_pipe(f, dlocate)
        res = pipe.readlines()
        pipe.close()

        self.assertEquals(dloc, dlocate)
        self.assertGreater(len(res), 0)

        dlocate = False
        pipe, dloc = utils.search_pipe(f, dlocate)
        res = pipe.readlines()
        pipe.close()

        self.assertEquals(dloc, dlocate)
        self.assertGreater(len(res), 0)

class TestDpkg(unittest2.TestCase):

    def test_query_dpkg_for(self):

        p = 'reportbug'
        dlocate = True
        res = utils.query_dpkg_for(p, dlocate)

        self.assertEquals(res[0], p)
        self.assertGreater(len(res[1].keys()), 0)

        dlocate = False
        res = utils.query_dpkg_for(p, dlocate)

        self.assertEquals(res[0], p)
        self.assertGreater(len(res[1].keys()), 0)

        # to trigger 'Try again without dlocate if no packages found'
        p = 'blablabla'
        dlocate = True
        res = utils.query_dpkg_for(p, dlocate)

        self.assertEquals(res[0], p)
        self.assertEquals(res[1], {})

class TestMisc(unittest2.TestCase):

    def test_first_run(self):

        isfirstrun = utils.first_run()
        self.assertIsNotNone(isfirstrun)

    def test_exec_and_parse_bugscript(self):

        handler = os.path.dirname(__file__) + '/../share/handle_bugscript'
        bugscript_file = os.path.dirname(__file__) + '/data/bugscript'

        (rc, h, ph, t, a) = utils.exec_and_parse_bugscript(handler, bugscript_file)

        self.assertIn('python', t)
        self.assertIn('debian', t)
        self.assertIn('From: morph@dummy.int', h)
        self.assertIn('User: morph@debian.org', ph)
        self.assertIn('/etc/fstab', a)

    def test_check_package_name(self):
        self.assertTrue(utils.check_package_name('reportbug'))
        self.assertTrue(utils.check_package_name('ab'))
        self.assertFalse(utils.check_package_name('a'))
        self.assertFalse(utils.check_package_name('.a'))
        self.assertFalse(utils.check_package_name('dfffff       '))
        self.assertFalse(utils.check_package_name('reportbug_reportbug'))
        self.assertTrue(utils.check_package_name('reportbug+love-war.com'))
        self.assertTrue(utils.check_package_name('reportbug2001'))
        self.assertFalse(utils.check_package_name('UPPERCASE'))
        self.assertFalse(utils.check_package_name('((()))'))
