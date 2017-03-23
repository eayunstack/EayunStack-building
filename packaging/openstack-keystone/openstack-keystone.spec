%global release_name juno
%global milestone rc2

%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

%global dist_eayunstack .eayunstack.dev

Name:           openstack-keystone
Version:        2014.2
Release:        2%{?dist_eayunstack}
Summary:        OpenStack Identity Service

License:        ASL 2.0
URL:            http://keystone.openstack.org/
Source0:        http://launchpad.net/keystone/%{release_name}/%{version}/+download/keystone-%{version}.tar.gz
Source1:        openstack-keystone.logrotate
Source2:        openstack-keystone.service
Source3:        openstack-keystone.sysctl
Source5:        openstack-keystone-sample-data
Source20:       keystone-dist.conf
Source21:       daemon_notify.sh
Source22:       openstack-keystone.init
Source23:       openstack-keystone.upstart


Patch0001: 0001-remove-runtime-dep-on-python-pbr.patch
Patch0002: 0002-sync-parameter-values-with-keystone-dist.conf.patch
Patch0003: 0003-output-log-to-keystone-all-log-file.patch

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-d2to1

Requires:       python-keystone = %{version}-%{release}
Requires:       python-keystoneclient >= 1:0.10.0

%if 0%{?rhel} == 6
Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig
Requires(preun):  initscripts
# for daemon_notify
Requires: /usr/bin/uuidgen
Requires: /bin/sleep
%else
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
%endif
Requires(pre):    shadow-utils

%description
Keystone is a Python implementation of the OpenStack
(http://www.openstack.org) identity service API.

This package contains the Keystone daemon.

%package -n       python-keystone
Summary:          Keystone Python libraries
Group:            Applications/System

Requires:       python-eventlet
Requires:       python-ldap
Requires:       python-ldappool
Requires:       python-memcached
Requires:       python-migrate >= 0.9.1
Requires:       python-paste-deploy >= 1.5.0
Requires:       python-routes >= 1.12
Requires:       python-sqlalchemy >= 0.8.4
Requires:       python-webob >= 1.2.3
Requires:       python-passlib
Requires:       MySQL-python
Requires:       PyPAM
Requires:       python-iso8601
Requires:       python-oslo-config >= 1:1.4.0.0
Requires:       openssl
Requires:       python-netaddr
Requires:       python-six >= 1.4.1
Requires:       python-babel
Requires:       python-oauthlib
Requires:       python-dogpile-cache >= 0.5.3
Requires:       python-jsonschema
Requires:       python-oslo-messaging >= 1.4.0.0
Requires:       python-pycadf >= 0.6.0
Requires:       python-posix_ipc
Requires:       python-keystonemiddleware
Requires:       python-oslo-db
Requires:       python-oslo-i18n
Requires:       python-oslo-utils

%description -n   python-keystone
Keystone is a Python implementation of the OpenStack
(http://www.openstack.org) identity service API.

This package contains the Keystone Python library.

%if 0%{?with_doc}
%package doc
Summary:        Documentation for OpenStack Identity Service
Group:          Documentation

BuildRequires:  python-sphinx >= 1.1.2
BuildRequires:  python-oslo-sphinx
# for API autodoc
BuildRequires:  python-keystonemiddleware
BuildRequires:  python-ldappool


%description doc
Keystone is a Python implementation of the OpenStack
(http://www.openstack.org) identity service API.

This package contains documentation for Keystone.
%endif

%prep
%setup -q -n keystone-%{version}

%patch0001 -p1
%patch0002 -p1
%patch0003 -p1

find . \( -name .gitignore -o -name .placeholder \) -delete
find keystone -name \*.py -exec sed -i '/\/usr\/bin\/env python/d' {} \;
# Remove bundled egg-info
rm -rf keystone.egg-info
# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt
# Remove dependency on pbr and set version as per rpm
sed -i s/REDHATKEYSTONEVERSION/%{version}/ bin/keystone-all keystone/cli.py

# make doc build compatible with python-oslo-sphinx RPM
sed -i 's/oslosphinx/oslo.sphinx/' doc/source/conf.py

%build
cp etc/keystone.conf.sample etc/keystone.conf
# distribution defaults are located in keystone-dist.conf

%{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root %{buildroot}

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/keystone/tests

install -d -m 755 %{buildroot}%{_sysconfdir}/keystone
install -p -D -m 640 etc/keystone.conf %{buildroot}%{_sysconfdir}/keystone/keystone.conf
install -p -D -m 644 etc/keystone-paste.ini %{buildroot}%{_datadir}/keystone/keystone-dist-paste.ini
install -p -D -m 644 %{SOURCE20} %{buildroot}%{_datadir}/keystone/keystone-dist.conf
install -p -D -m 644 etc/policy.v3cloudsample.json %{buildroot}%{_datadir}/keystone/policy.v3cloudsample.json
install -p -D -m 640 etc/logging.conf.sample %{buildroot}%{_sysconfdir}/keystone/logging.conf
install -p -D -m 640 etc/default_catalog.templates %{buildroot}%{_sysconfdir}/keystone/default_catalog.templates
install -p -D -m 640 etc/policy.json %{buildroot}%{_sysconfdir}/keystone/policy.json
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-keystone
%if 0%{?rhel} == 6
# Install service readiness wrapper
install -p -D -m 755 %{SOURCE21} %{buildroot}%{_datadir}/keystone/daemon_notify.sh
install -p -D -m 755 %{SOURCE22} %{buildroot}%{_initrddir}/openstack-keystone
install -p -D -m 644 %{SOURCE23} %{buildroot}%{_datadir}/keystone/%{name}.upstart
%else
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/openstack-keystone.service
%endif
install -d -m 755 %{buildroot}%{_prefix}/lib/sysctl.d
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_prefix}/lib/sysctl.d/openstack-keystone.conf
# Install sample data script.
install -p -D -m 755 tools/sample_data.sh %{buildroot}%{_datadir}/keystone/sample_data.sh
install -p -D -m 755 %{SOURCE5} %{buildroot}%{_bindir}/openstack-keystone-sample-data
# Install sample HTTPD integration files
install -p -D -m 644 httpd/keystone.py  %{buildroot}%{_datadir}/keystone/keystone.wsgi
install -p -D -m 644 httpd/wsgi-keystone.conf  %{buildroot}%{_datadir}/keystone/

install -d -m 755 %{buildroot}%{_sharedstatedir}/keystone
install -d -m 755 %{buildroot}%{_localstatedir}/log/keystone
%if 0%{?rhel} == 6
install -d -m 755 %{buildroot}%{_localstatedir}/run/keystone
%endif

# docs generation requires everything to be installed first
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
make html
make man
mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 build/man/*.1 %{buildroot}%{_mandir}/man1/
popd
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo

%pre
# 163:163 for keystone (openstack-keystone) - rhbz#752842
getent group keystone >/dev/null || groupadd -r --gid 163 keystone
getent passwd keystone >/dev/null || \
useradd --uid 163 -r -g keystone -d %{_sharedstatedir}/keystone -s /sbin/nologin \
-c "OpenStack Keystone Daemons" keystone
exit 0

%post
%if 0%{?rhel} == 6
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add openstack-keystone
fi
%else
%systemd_post openstack-keystone.service
%endif

%preun
%if 0%{?rhel} == 6
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /sbin/service openstack-keystone stop >/dev/null 2>&1
    /sbin/chkconfig --del openstack-keystone
fi
%else
%systemd_preun openstack-keystone.service
%endif

%postun
%if 0%{?rhel} == 6
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /sbin/service openstack-keystone condrestart >/dev/null 2>&1 || :
fi
%else
%systemd_postun_with_restart openstack-keystone.service
%endif

%files
%doc LICENSE
%doc README.rst
%{_mandir}/man1/keystone*.1.gz
%{_bindir}/keystone-all
%{_bindir}/keystone-manage
%{_bindir}/openstack-keystone-sample-data
%dir %{_datadir}/keystone
%attr(0644, root, keystone) %{_datadir}/keystone/keystone-dist.conf
%attr(0644, root, keystone) %{_datadir}/keystone/keystone-dist-paste.ini
%attr(0644, root, keystone) %{_datadir}/keystone/policy.v3cloudsample.json
%attr(0755, root, root) %{_datadir}/keystone/sample_data.sh
%attr(0644, root, keystone) %{_datadir}/keystone/keystone.wsgi
%attr(0644, root, keystone) %{_datadir}/keystone/wsgi-keystone.conf
%if 0%{?rhel} == 6
%attr(0755, root, root) %{_datadir}/keystone/daemon_notify.sh
%{_datadir}/keystone/%{name}.upstart
%{_initrddir}/openstack-keystone
%else
%{_unitdir}/openstack-keystone.service
%endif
%dir %attr(0750, root, keystone) %{_sysconfdir}/keystone
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/keystone.conf
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/logging.conf
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/default_catalog.templates
%config(noreplace) %attr(0640, keystone, keystone) %{_sysconfdir}/keystone/policy.json
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-keystone
%dir %attr(-, keystone, keystone) %{_sharedstatedir}/keystone
%dir %attr(0750, keystone, keystone) %{_localstatedir}/log/keystone
%if 0%{?rhel} == 6
%dir %attr(-, keystone, keystone) %{_localstatedir}/run/keystone
%endif
%{_prefix}/lib/sysctl.d/openstack-keystone.conf


%files -n python-keystone
%defattr(-,root,root,-)
%doc LICENSE
%{python_sitelib}/keystone
%{python_sitelib}/keystone-%{version}-*.egg-info

%if 0%{?with_doc}
%files doc
%doc LICENSE doc/build/html
%endif

%changelog
* Fri Nov 20 2015 Ma Zhe <zhe.ma@eayun.com> 2014.2-2.eayunstack.1.1
- add 0003-output-log-to-keystone-all-log-file.patch

* Thu Oct 16 2014 Alan Pevec <apevec@redhat.com> 2014.2-1
- Juno release

* Wed Jul 09 2014 Alan Pevec <apevec@redhat.com> 2014.1.1-4
- Keystone V2 trusts privilege escalation through user supplied project id
  CVE-2014-3520

* Wed Jun 25 2014 Alan Pevec <apevec@redhat.com> 2014.1.1-3
- exclude default port 35357 from the ephemeral port range

* Fri Jun 13 2014 Alan Pevec <apevec@redhat.com> 2014.1.1-2
- privilege escalation through trust chained delegation CVE-2014-3476

* Fri Jun 06 2014 Alan Pevec <apevec@redhat.com> 2014.1.1-1
- updated to stable icehouse 2014.1.1 release
- Keystone user and group id mismatch CVE-2014-0204

* Thu Apr 17 2014 Alan Pevec <apevec@redhat.com> 2014.1-2
- Icehouse release

* Fri Apr 11 2014 Alan Pevec <apevec@redhat.com> 2014.1-0.9.rc2
- icehouse rc2

* Sun Mar 09 2014 Alan Pevec <apevec@redhat.com> 2014.1-0.5.b3
- use oslo systemd module for service notification

* Fri Mar 07 2014 Alan Pevec <apevec@redhat.com> 2014.1-0.4.b3
- icehouse-3 milestone

* Fri Jan 24 2014 Alan Pevec <apevec@redhat.com> 2014.1-0.3.b2
- icehouse-2 milestone

* Mon Jan 06 2014 Pádraig Brady <pbrady@redhat.com> - 2014.1-0.2.b1
- Set python-six min version to ensure updated

* Thu Dec 12 2013 Alan Pevec <apevec@redhat.com> 2014.1-0.1.b1
- icehouse-1 milestone

* Wed Oct 30 2013 Alan Pevec <apevec@redhat.com> 2013.2-2
- unintentional role granting with Keystone LDAP backend CVE-2013-4477

* Thu Oct 17 2013 Alan Pevec <apevec@redhat.com> - 2013.2-1
- Update to havana final

* Mon Oct 07 2013 Alan Pevec <apevec@redhat.com> - 2013.2-0.14.rc1
- rename HTTPD integration to keystone.wsgi

* Wed Oct 02 2013 Adam Young <ayoung@redhat> - 2013.2-0.11.rc1
- HTTPD integration files

* Wed Oct 02 2013 Alan Pevec <apevec@redhat.com> - 2013.2-0.10.rc1
- Havana release candidate

* Mon Sep 09 2013 Alan Pevec <apevec@redhat.com> - 2013.2-0.9.b3
- havana-3 milestone
- drop pbr run-time dependency
- set distribution defaults in keystone-dist.conf

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2013.2-0.5.b2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 pbrady@redhat.com 2013.2-0.4.b2
- havana-2 milestone

* Mon Jun 24 2013 apevec@redhat.com 2013.2-0.3.b1
- restrict /var/log/keystone/ rhbz#956814

* Sat Jun 22 2013 apevec@redhat.com 2013.2-0.2.b1
- Force simple Bind for authentication CVE-2013-2157

* Fri Jun 07 2013 Alan Pevec <apevec@redhat.com> 2013.2-0.1.h1
- havana-1 milestone

* Fri May 10 2013 Alan Pevec <apevec@redhat.com> 2013.1.1-1
- updated to stable grizzly 2013.1.1 release CVE-2013-2006 CVE-2013-2059

* Thu Apr 04 2013 Alan Pevec <apevec@redhat.com> 2013.1-1
- Update to grizzly final

* Wed Apr 03 2013 Alan Pevec <apevec@redhat.com> 2013.1-0.10.rc3
- grizzly rc3

* Fri Mar 29 2013 Alan Pevec <apevec@redhat.com> 2013.1-0.9.rc2
- grizzly rc2

* Wed Mar 20 2013 Pádraig Brady <pbrady@redhat.com> 2013.1-0.8.g3
- fix a grizzly issue with int/str config mismatch

* Mon Mar 11 2013 Alan Pevec <apevec@redhat.com> 2013.1-0.7.g3
- openssl is required for PKI tokens rhbz#918757

* Mon Mar 11 2013 Alan Pevec <apevec@redhat.com> 2013.1-0.6.g3
- remove python-sqlalchemy restriction

* Sun Feb 24 2013 Alan Pevec <apevec@redhat.com> 2013.1-0.5.g3
- update dependencies

* Sat Feb 23 2013 Alan Pevec <apevec@redhat.com> 2013.1-0.4.g3
- grizzly-3 milestone

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2013.1-0.3.g2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 11 2013 Alan Pevec <apevec@redhat.com> 2013.1-0.2.g2
- grizzly-2 milestone

* Thu Nov 22 2012 Alan Pevec <apevec@redhat.com> 2013.1-0.1.g1
- grizzly-1 milestone

* Fri Nov 16 2012 Alan Pevec <apevec@redhat.com> 2012.2-5
- fix /etc/keystone directory permission CVE-2012-5483 (rhbz#873447)

* Mon Nov 12 2012 Alan Pevec <apevec@redhat.com> 2012.2-4
- readd iso8601 dependency (from openstack-common timeutils)

* Fri Nov 09 2012 Alan Pevec <apevec@redhat.com> 2012.2-3
- remove auth-token subpackage (rhbz#868357)

* Thu Nov 08 2012 Alan Pevec <apevec@redhat.com> 2012.2-2
- Fix default port for identity.internalURL in sample script

* Thu Sep 27 2012 Alan Pevec <apevec@redhat.com> 2012.2-1
- Update to folsom final

* Wed Sep 26 2012 Alan Pevec <apevec@redhat.com> 2012.2-0.9.rc2
- folsom rc2

* Fri Sep 21 2012 Alan Pevec <apevec@redhat.com> 2012.2-0.8.rc1
- fix systemd notification (rhbz#858188)

* Fri Sep 14 2012 Alan Pevec <apevec@redhat.com> 2012.2-0.7.rc1
- folsom rc1 (CVE-2012-4413)

* Thu Aug 30 2012 Alan Pevec <apevec@redhat.com> 2012.2-0.6.f3
- Require authz to update user's tenant (CVE-2012-3542)

* Wed Aug 29 2012 Alan Pevec <apevec@redhat.com> 2012.2-0.5.f3
- allow middleware configuration from app config

* Mon Aug 20 2012 Alan Pevec <apevec@redhat.com> 2012.2-0.4.f3
- folsom-3 milestone

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012.2-0.3.f2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 06 2012 Alan Pevec <apevec@redhat.com> 2012.2-0.2.f2
- folsom-2 milestone (CVE-2012-3426)

* Fri May 25 2012 Alan Pevec <apevec@redhat.com> 2012.2-0.1.f1
- folsom-1 milestone

* Thu May 24 2012 Alan Pevec <apevec@redhat.com> 2012.1-3
- python-keystone-auth-token subpackage (rhbz#824034)
- use reserved user id for keystone (rhbz#752842)

* Mon May 21 2012 Alan Pevec <apevec@redhat.com> 2012.1-2
- Sync up with Essex stable branch
- Remove dependencies no loner needed by Essex

* Thu Apr 05 2012 Alan Pevec <apevec@redhat.com> 2012.1-1
- Essex release

* Wed Apr 04 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.13.rc2
- essex rc2

* Sat Mar 24 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.12.rc1
- update to final essex rc1

* Wed Mar 21 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.11.rc1
- essex rc1

* Thu Mar 08 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.10.e4
- change default catalog backend to sql rhbz#800704
- update sample-data script
- add missing keystoneclient dependency

* Thu Mar 01 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.9.e4
- essex-4 milestone

* Sat Feb 25 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.8.e4
- change default database to mysql

* Tue Feb 21 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.7.e4
- switch all backends to sql

* Mon Feb 20 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.6.e4
- add missing default_catalog.templates

* Mon Feb 20 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.5.e4
- pre essex-4 snapshot, for keystone rebase

* Mon Feb 13 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.4.e3
- fix deps rhbz#787072
- keystone is not hashing passwords lp#924391
- Fix "KeyError: 'service-header-mappings'" lp#925872

* Wed Feb  8 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 2012.1-0.3.e3
- Remove the dep on python-sqlite2 as that's being retired in F17 and keystone
  will work with the sqlite3 module from the stdlib

* Thu Jan 26 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.2.e3
- separate library to python-keystone
- avoid conflict with python-keystoneclient

* Thu Jan 26 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.1.e3
- essex-3 milestone

* Wed Jan 18 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.e2
- essex-2 milestone

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2011.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 24 2011 Alan Pevec <apevec@redhat.com> 2011.3.1-2
- include LICENSE, update package description from README.md

* Mon Nov 21 2011 Alan Pevec <apevec@redhat.com> 2011.3.1-1
- Update to 2011.3.1 stable/diablo release

* Fri Nov 11 2011 Alan Pevec <apevec@redhat.com> 2011.3-2
- Update to the latest stable/diablo snapshot

* Mon Oct 24 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-1
- Update version to diablo final

* Wed Oct 19 2011 Matt Domsch <Matt_Domsch@dell.com> - 1.0-0.4.d4.1213
- add Requires: python-passlib

* Mon Oct 3 2011 Matt Domsch <Matt_Domsch@dell.com> - 1.0-0.2.d4.1213
- update to diablo release.
- BR systemd-units for _unitdir

* Fri Sep  2 2011 Mark McLoughlin <markmc@redhat.com> - 1.0-0.2.d4.1078
- Use upstream snapshot tarball
- No need to define python_sitelib anymore
- BR python2-devel
- Remove BRs only needed for unit tests
- No need to clean buildroot in install anymore
- Use slightly more canonical site for URL tag
- Prettify the requires tags
- Cherry-pick tools.tracer patch from upstream
- Add config file
- Add keystone user and group
- Ensure log file is in /var/log/keystone
- Ensure the sqlite db is in /var/lib/keystone
- Add logrotate support
- Add system units

* Thu Sep  1 2011 Matt Domsch <Matt_Domsch@dell.com> - 1.0-0.1.20110901git396f0bfd%{?dist}
- initial packaging
