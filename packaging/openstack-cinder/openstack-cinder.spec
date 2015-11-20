%global release_name juno

%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

%global dist_eayunstack .eayunstack.1.0

Name:             openstack-cinder
Version:          2014.2.1
Release:          4%{?dist_eayunstack}
Summary:          OpenStack Volume service

License:          ASL 2.0
URL:              http://www.openstack.org/software/openstack-storage/
Source0:          http://launchpad.net/cinder/%{release_name}/%{version}/+download/cinder-%{version}.tar.gz

Source1:          cinder-dist.conf
Source2:          cinder.logrotate

Source10:         openstack-cinder-api.service
Source11:         openstack-cinder-scheduler.service
Source12:         openstack-cinder-volume.service
Source13:         openstack-cinder-backup.service
Source20:         cinder-sudoers

Patch0001: 0001-Remove-runtime-dep-on-python-pbr-python-d2to1.patch
Patch0002: 0002-Revert-Switch-over-to-oslosphinx.patch
Patch0003: 0003-Fix-eqlx-endless-loop-when-server-closes-the-connect.patch
Patch0004: 0004-Fix-the-eqlx-driver-to-retry-on-ssh-timeout.patch
Patch0005: 0005-Fixes-the-EQL-driver-CI-tests-AttributeError.patch
Patch0006: 0006-output-log-to-cinder-all-log-file.patch

BuildArch:        noarch
BuildRequires:    intltool
BuildRequires:    python-d2to1
BuildRequires:    python-oslo-sphinx
BuildRequires:    python-pbr
BuildRequires:    python-sphinx
BuildRequires:    python2-devel
BuildRequires:    python-setuptools
BuildRequires:    python-netaddr
BuildRequires:    systemd
BuildRequires:    git

Requires:         openstack-utils
Requires:         python-cinder = %{version}-%{release}

# as convenience
Requires:         python-cinderclient

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires(pre):    shadow-utils

Requires:         lvm2
Requires:         python-osprofiler
Requires:         python-rtslib

%description
OpenStack Volume (codename Cinder) provides services to manage and
access block storage volumes for use by Virtual Machine instances.


%package -n       python-cinder
Summary:          OpenStack Volume Python libraries
Group:            Applications/System

Requires:         sudo

Requires:         MySQL-python

Requires:         qemu-img
Requires:         sysfsutils

Requires:         python-paramiko

Requires:         python-qpid
Requires:         python-kombu
Requires:         python-amqplib

Requires:         python-eventlet
Requires:         python-greenlet
Requires:         python-iso8601
Requires:         python-netaddr
Requires:         python-lxml
Requires:         python-anyjson
Requires:         python-cheetah
Requires:         python-stevedore
Requires:         python-suds

Requires:         python-sqlalchemy
Requires:         python-migrate

Requires:         python-paste-deploy
Requires:         python-routes
Requires:         python-webob

Requires:         python-glanceclient >= 1:0
Requires:         python-swiftclient >= 1.2
Requires:         python-keystoneclient
Requires:         python-novaclient >= 1:2.15

Requires:         python-oslo-config >= 1:1.2.0
Requires:         python-oslo-db >= 1.0.0
Requires:         python-six >= 1.5.0

Requires:         python-babel
Requires:         python-lockfile

Requires:         python-oslo-rootwrap
Requires:         python-taskflow >= 0.4.0
Requires:         python-oslo-messaging >= 1.3.0-0.1.a9
Requires:         python-keystonemiddleware >= 1.0.0

Requires:         libcgroup-tools
Requires:         iscsi-initiator-utils

Requires:         python-osprofiler

%description -n   python-cinder
OpenStack Volume (codename Cinder) provides services to manage and
access block storage volumes for use by Virtual Machine instances.

This package contains the cinder Python library.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Volume
Group:            Documentation

Requires:         %{name} = %{version}-%{release}

BuildRequires:    graphviz

# Required to build module documents
BuildRequires:    python-eventlet
BuildRequires:    python-routes
BuildRequires:    python-sqlalchemy
BuildRequires:    python-webob
# while not strictly required, quiets the build down when building docs.
BuildRequires:    python-migrate, python-iso8601

%description      doc
OpenStack Volume (codename Cinder) provides services to manage and
access block storage volumes for use by Virtual Machine instances.

This package contains documentation files for cinder.
%endif

%prep
%autosetup -n cinder-%{version} -S git

find . \( -name .gitignore -o -name .placeholder \) -delete

find cinder -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

sed -i 's/%{version}.%{milestone}/%{version}/' PKG-INFO

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

# We add REDHATCINDERVERSION/RELEASE with the pbr removal patch
sed -i s/REDHATCINDERVERSION/%{version}/ cinder/version.py
sed -i s/REDHATCINDERRELEASE/%{release}/ cinder/version.py

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# docs generation requires everything to be installed first
export PYTHONPATH="$( pwd ):$PYTHONPATH"

pushd doc

%if 0%{?with_doc}
SPHINX_DEBUG=1 sphinx-build -b html source build/html
# Fix hidden-file-or-dir warnings
rm -fr build/html/.doctrees build/html/.buildinfo
%endif

# Create dir link to avoid a sphinx-build exception
mkdir -p build/man/.doctrees/
ln -s .  build/man/.doctrees/man
SPHINX_DEBUG=1 sphinx-build -b man -c source source/man build/man
mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 build/man/*.1 %{buildroot}%{_mandir}/man1/

popd

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/cinder
install -d -m 755 %{buildroot}%{_sharedstatedir}/cinder/tmp
install -d -m 755 %{buildroot}%{_localstatedir}/log/cinder

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/cinder
install -p -D -m 640 %{SOURCE1} %{buildroot}%{_datadir}/cinder/cinder-dist.conf
install -p -D -m 640 etc/cinder/cinder.conf.sample %{buildroot}%{_sysconfdir}/cinder/cinder.conf
install -d -m 755 %{buildroot}%{_sysconfdir}/cinder/volumes
install -p -D -m 640 etc/cinder/rootwrap.conf %{buildroot}%{_sysconfdir}/cinder/rootwrap.conf
install -p -D -m 640 etc/cinder/api-paste.ini %{buildroot}%{_sysconfdir}/cinder/api-paste.ini
install -p -D -m 640 etc/cinder/policy.json %{buildroot}%{_sysconfdir}/cinder/policy.json

# Install initscripts for services
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_unitdir}/openstack-cinder-api.service
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/openstack-cinder-scheduler.service
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/openstack-cinder-volume.service
install -p -D -m 644 %{SOURCE13} %{buildroot}%{_unitdir}/openstack-cinder-backup.service

# Install sudoers
install -p -D -m 440 %{SOURCE20} %{buildroot}%{_sysconfdir}/sudoers.d/cinder

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-cinder

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/cinder

# Install rootwrap files in /usr/share/cinder/rootwrap
mkdir -p %{buildroot}%{_datarootdir}/cinder/rootwrap/
install -p -D -m 644 etc/cinder/rootwrap.d/* %{buildroot}%{_datarootdir}/cinder/rootwrap/

# Remove unneeded in production stuff
rm -f %{buildroot}%{_bindir}/cinder-debug
rm -fr %{buildroot}%{python_sitelib}/cinder/tests/
rm -fr %{buildroot}%{python_sitelib}/run_tests.*
rm -f %{buildroot}/usr/share/doc/cinder/README*

%pre
getent group cinder >/dev/null || groupadd -r cinder --gid 165
if ! getent passwd cinder >/dev/null; then
  useradd -u 165 -r -g cinder -G cinder,nobody -d %{_sharedstatedir}/cinder -s /sbin/nologin -c "OpenStack Cinder Daemons" cinder
fi
exit 0

%post
%systemd_post openstack-cinder-volume
%systemd_post openstack-cinder-api
%systemd_post openstack-cinder-scheduler
%systemd_post openstack-cinder-backup

%preun
%systemd_preun openstack-cinder-volume
%systemd_preun openstack-cinder-api
%systemd_preun openstack-cinder-scheduler
%systemd_preun openstack-cinder-backup

%postun
%systemd_postun_with_restart openstack-cinder-volume
%systemd_postun_with_restart openstack-cinder-api
%systemd_postun_with_restart openstack-cinder-scheduler
%systemd_postun_with_restart openstack-cinder-backup

%files
%dir %{_sysconfdir}/cinder
%config(noreplace) %attr(-, root, cinder) %{_sysconfdir}/cinder/cinder.conf
%config(noreplace) %attr(-, root, cinder) %{_sysconfdir}/cinder/api-paste.ini
%config(noreplace) %attr(-, root, cinder) %{_sysconfdir}/cinder/rootwrap.conf
%config(noreplace) %attr(-, root, cinder) %{_sysconfdir}/cinder/policy.json
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-cinder
%config(noreplace) %{_sysconfdir}/sudoers.d/cinder
%attr(-, root, cinder) %{_datadir}/cinder/cinder-dist.conf

%dir %attr(0750, cinder, root) %{_localstatedir}/log/cinder
%dir %attr(0755, cinder, root) %{_localstatedir}/run/cinder
%dir %attr(0755, cinder, root) %{_sysconfdir}/cinder/volumes

%{_bindir}/cinder-*
%{_unitdir}/*.service
%{_datarootdir}/cinder
%{_mandir}/man1/cinder*.1.gz

%defattr(-, cinder, cinder, -)
%dir %{_sharedstatedir}/cinder
%dir %{_sharedstatedir}/cinder/tmp

%files -n python-cinder
%{?!_licensedir: %global license %%doc}
%license LICENSE
%{python2_sitelib}/cinder
%{python2_sitelib}/cinder-%{version}*.egg-info

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%endif

%changelog
* Fri Nov 20 2015 Ma Zhe <zhe.ma@eayun.com> - 2014.2.1-4.eayunstack.1.0
- add 0006-output-log-to-cinder-all-log-file.patch

* Thu May 07 2015 Dunrong Huang <dunrong.huang@eayun.com> - 2014.2.1-3.eayunstack.1.0
- add 0003-Fix-eqlx-endless-loop-when-server-closes-the-connect.patch
- add 0004-Fix-the-eqlx-driver-to-retry-on-ssh-timeout.patch
- add 0005-Fixes-the-EQL-driver-CI-tests-AttributeError.patch

* Sat Jan 17 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 2014.2.1-2
- Fix requirements (RHBZ #1174760 #1175368 #1179060)

* Fri Dec 05 2014 Haikel Guemar <hguemar@fedoraproject.org> 2014.2.1-1
- Update to upstream 2014.2.1

* Thu Dec 04 2014 Eric Harney <eharney@redhat.com> - 2014.2-3
- Depend on python-oslo-db

* Wed Nov 26 2014 Haïkel guémar <hguemar@redhat.com> - 2014.2-2
- Drop now useless tgtd configuration (RHBZ #1157619)

* Fri Oct 17 2014 Haïkel Guémar <hguemar@fedoraproject.org> 2014.2-1
- Update to upstream 2014.2
- Spec cleanups

* Wed Oct 15 2014 Haïkel Guémar <hguemar@fedoraproject.org> 2014.2-0.6.rc3
- Update to upstream 2014.2.rc3

* Mon Oct 13 2014 Haikel Guemar <hguemar@fedoraproject.org> 2014.2-0.5.rc2
- Update to upstream 2014.2.rc2

* Thu Oct 09 2014 hguemar <hguemar@senbonzakura> - 2014.2-0.4.rc1
- Fix spec typos

* Wed Oct 08 2014 Haikel Guemar <hguemar@fedoraproject.org> 2014.2-0.3.rc1
- Update to upstream 2014.2.rc1

* Fri Sep 12 2014 Eric Harney <eharney@redhat.com> - 2014.2-0.2.b3
- Update to Juno milestone 3

* Thu Jul 31 2014 Eric Harney <eharney@redhat.com> - 2014.2-0.1.b2
- Update to Juno milestone 2

* Wed Jun 11 2014 Eric Harney <eharney@redhat.com> - 2014.1.1-2
- Add dependency on iscsi-initiator-utils

* Mon Jun 09 2014 Eric Harney <eharney@redhat.com> - 2014.1.1-1
- Update to Icehouse stable release 1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2014.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 29 2014 Alan Pevec <apevec@redhat.com> - 2014.1-3
- drop crudini build dependency

* Mon Apr 21 2014 Eric Harney <eharney@redhat.com> - 2014.1-2
- Remove qpid settings from cinder-dist.conf

* Thu Apr 17 2014 Eric Harney <eharney@redhat.com> - 2014.1-1
- Update to 2014.1 (Icehouse)

* Tue Apr 15 2014 Eric Harney <eharney@redhat.com> - 2014.1-0.10.rc3
- Add python-oslo-messaging requirement
- Add GlusterFS delete patch
- Add systemd patches (not used yet)

* Tue Apr 15 2014 Eric Harney <eharney@redhat.com> - 2014.1-0.9.rc3
- Update to Icehouse RC3

* Mon Apr 07 2014 Eric Harney <eharney@redhat.com> - 2014.1-0.8.rc2
- Update to Icehouse RC2
- Icehouse requires newer version of python-six

* Thu Mar 27 2014 Eric Harney <eharney@redhat.com> - 2014.1-0.7.rc1
- Update to Icehouse RC1

* Tue Mar 25 2014 Pádraig Brady <pbrady@redhat.com> - 2014.1-0.6.b3
- Depend on python-rtslib and targetcli rather than scsi-target-utils

* Fri Mar 21 2014 Pádraig Brady <pbrady@redhat.com> - 2014.1-0.5.b3
- Use lioadm iSCSI helper rather than tgtadm

* Sun Mar 16 2014 Eric Harney <eharney@redhat.com> - 2014.1-0.4.b3
- Update to Icehouse milestone 3
- Add deps on python-oslo-rootwrap, python-taskflow

* Mon Jan 27 2014 Eric Harney <eharney@redhat.com> - 2014.1-0.3.b2
- Update to Icehouse milestone 2

* Mon Jan 06 2014 Pádraig Brady <pbrady@redhat.com> - 2014.1-0.2.b1
- Set python-six min version to ensure updated

* Thu Dec 19 2013 Eric Harney <eharney@redhat.com> - 2014.1-0.1.b1
- Update to Icehouse milestone 1

* Mon Oct 28 2013 Eric Harney <eharney@redhat.com> - 2013.2-2
- Fix GlusterFS volume driver clone operations

* Thu Oct 17 2013 Eric Harney <eharney@redhat.com> - 2013.2-1
- Update to 2013.2 (Havana)
- Restart/remove cinder-backup service during upgrade/uninstallation

* Wed Oct 16 2013 Eric Harney <eharney@redhat.com> - 2013.2-0.13.rc3
- Update to Havana RC3

* Fri Oct 11 2013 Eric Harney <eharney@redhat.com> - 2013.2-0.12.rc2
- Update to Havana RC2

* Tue Oct 08 2013 Eric Harney <eharney@redhat.com> - 2013.2-0.11.rc1
- Update to Havana RC1
- Fix python-novaclient req epoch

* Mon Sep 23 2013 Eric Harney <eharney@redhat.com> - 2013.2-0.10.b3
- Depend on python-novaclient 2.15

* Wed Sep 18 2013 Eric Harney <eharney@redhat.com> - 2013.2-0.9.b3
- Add cinder-dist.conf
- Tighten permissions on /var/log/cinder

* Mon Sep 9 2013 Eric Harney <eharney@redhat.com> - 2013.2-0.8.b3
- Update to Havana milestone 3
- Add dependency on python-novaclient

* Thu Aug 29 2013 Pádraig Brady <pbrady@redhat.com> - 2013.2-0.7.b2
- Add dependency on sysfsutils to support the fiber channel driver

* Mon Aug 26 2013 Eric Harney <eharney@redhat.com> - 2013.2-0.6.b2
- Add cinder-backup service init script

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2013.2-0.5.b2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Pádraig Brady <pbrady@redhat.com> - 2013.2-0.4.b2
- Add dependency on python-suds to support the netapp driver
- Add dependency on python-keystoneclient for auth token middleware
- Add dependency on qemu-img for volume creation from Glance images

* Sun Jul 21 2013 Pádraig Brady <pbrady@redhat.com> - 2013.2-0.3.b2
- Update to Havana milestone 2

* Thu Jun 13 2013 Eric Harney <eharney@redhat.com> - 2013.2-0.2.b1
- Update to Havana milestone 1

* Mon May 13 2013 Eric Harney <eharney@redhat.com> - 2013.1.1-1
- Update to Grizzly stable release 1, 2013.1.1

* Mon Apr 08 2013 Eric Harney <eharney@redhat.com> - 2013.1-2
- Backport fix for GlusterFS driver get_volume_stats

* Thu Apr 04 2013 Eric Harney <eharney@redhat.com> - 2013.1-1
- Update to Grizzly final release

* Tue Apr  2 2013 Pádraig Brady <pbrady@redhat.com> - 2013.1-0.6.rc3
- Adjust to support sqlalchemy-0.8.0

* Wed Mar 27 2013 Eric Harney <eharney@redhat.com> - 2013.1-0.5.rc3
- Update to Grizzly RC3 release

* Mon Mar 25 2013 Eric Harney <eharney@redhat.com> - 2013.1-0.5.rc2
- Update to Grizzly RC2 release

* Mon Mar 18 2013 Eric Harney <eharney@redhat.com> - 2013.1-0.5.rc1
- Update to Grizzly RC1 release

* Tue Mar 05 2013 Pádraig Brady <P@draigBrady.com> - 2013.1-0.4.g3
- Add dependency on python-stevedore

* Mon Feb 25 2013 Eric Harney <eharney@redhat.com> - 2013.1-0.3.g3
- Fix build issues with G-3 update

* Mon Feb 25 2013 Eric Harney <eharney@redhat.com> - 2013.1-0.2.g3
- Update to Grizzly milestone 3

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2013.1-0.2.g2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 10 2013 Eric Harney <eharney@redhat.com> - 2013.1-0.1.g2
- Update to Grizzly milestone 2

* Thu Nov 29 2012 Eric Harney <eharney@redhat.com> - 2013.1-0.1.g1
- Update to Grizzly milestone 1

* Wed Nov 14 2012 Eric Harney <eharney@redhat.com> - 2012.2-2
- Remove unused dependency on python-daemon

* Thu Sep 27 2012 Pádraig Brady <P@draigBrady.com> - 2012.2-1
- Update to Folsom final

* Fri Sep 21 2012 Pádraig Brady <P@draigBrady.com> - 2012.2-0.5.rc1
- Update to Folsom RC1

* Fri Sep 21 2012 Pádraig Brady <P@draigBrady.com> - 2012.2-0.4.f3
- Fix to ensure that tgt configuration is honored

* Mon Sep 17 2012 Pádraig Brady <P@draigBrady.com> - 2012.2-0.3.f3
- Move user config out of /etc/cinder/api-paste.ini
- Require python-cinderclient

* Mon Sep  3 2012 Pádraig Brady <P@draigBrady.com> - 2012.2-0.2.f3
- Initial release
