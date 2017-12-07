%global release_name juno

%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

%global dist_eayunstack .eayunstack

Name:             openstack-cinder
Version:          2014.2.1
Release:          4.7%{?dist_eayunstack}
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
Patch0006: 0006-Volume-type-access-extension.patch
Patch0007: 0007-private-type-fix-db-scripts.patch
Patch0008: 0008-usd-is_uuid_like-from-oslo_utils.patch
Patch0009: 0009-fix-None-object-issue.patch
Patch0010: 0010-Choose-volume-type-belong-to-project.patch
Patch0011: 0011-Fix-the-unicode-encode-error-when-create-volume.patch
Patch0012: 0012-unittest-fix-test_migration_027.patch
Patch0013: 0013-Non-disruptive-backup.patch
Patch0014: 0014-Fix-cleanup_temp_volume_snapshots-for-missing-vol.patch
Patch0015: 0015-Handle-missing-temp-volume-and-snapshot-during-clean.patch
Patch0016: 0016-Fix-backup-init_host-volume-cleanup.patch
Patch0017: 0017-backup-init_host-cleanup-exception-handling.patch
Patch0018: 0018-cinder-list-fails-with-name-sort-key.patch
Patch0019: 0019-restore-volume-status-in-create_backup-when-backup-s.patch
Patch0020: 0020-take-care-of-non-disruptive-backup-when-detaching-a-.patch
Patch0021: 0021-only-allow-force-create-snapshot-when-volume-is-usab.patch
Patch0022: 0022-Get-the-consumer-in-a-correct-way-for-retyping-with-.patch
Patch0023: 0023-Use-project-id-from-volume-when-retyping-volumes.patch
Patch0024: 0024-Convert-mox-to-mock-tests-compute-test_nova.py.patch
Patch0025: 0025-Cleanly-override-config-in-tests.patch
Patch0026: 0026-Add-a-privileged-user-for-OpenStack-services.patch
Patch0027: 0027-Pass-region-name-to-Nova-client.patch
Patch0028: 0028-Add-ability-to-override-OpenStack-privileged-user-au.patch
Patch0029: 0029-Support-front-end-qos-updates-in-volume-retype.patch
Patch0030: 0030-Correctly-open-rbd-image-in-ceph-backup-driver.patch
Patch0031: 0031-Uncouple-scheduler-stats-from-volume-creation.patch
Patch0032: 0032-Rbd-update-volume-stats-in-wrong-way.patch
Patch0033: 0033-rbd-Change-capacity-calculation-from-integer-to-floa.patch
Patch0034: 0034-fix-cinder-ceph-backup-driver-padding-error.patch
Patch0035: 0035-Fix-always-false-condition-in-glance-wrapper.patch
Patch0036: 0036-Fix-properties-extracting-from-image-with-glance-api.patch
Patch0037: 0037-Fix-glance-image-create-fail-with-glance-api-v1.patch
Patch0038: 0038-Upload-backup-volume-to-image.patch
Patch0039: 0039-Add-deactivate-step-to-extend_lv.patch
Patch0040: 0040-Cinder-volume-revert-to-snapshot.patch
Patch0041: 0041-Cinder-volume-support-reverting-to-any-snapshot.patch
Patch0042: 0042-Cinder-volume-revert-to-snapshot-with-Ceph.patch
Patch0043: 0043-Resize-rbd-to-match-expected-volume-size-when.patch
Patch0044: 0044-Rbd-driver-support-reverting-to-any-snapshot.patch
Patch0045: 0045-Fix-code-style-errors-introduced-by-non-disruptive-b.patch
Patch0046: 0046-Keep-consistency-of-referring-db-backup-object.patch
Patch0047: 0047-Add-restore_volume_id-in-backup.patch
Patch0048: 0048-Correctly-reset-volume-status-while-cinder-backup-re.patch
Patch0049: 0049-Move-retype-quota-checks-to-API.patch
Patch0050: 0050-Retyping-volume-got-error-under-max-vol-limit.patch
Patch0051: 0051-Send-the-notifications-to-the-Ceilometer-for-backup-.patch
Patch0052: 0052-Add-notification-for-uploading-backup-to-Glance.patch
Patch0053: 0053-Fix-rbd-driver-revert_to_snapshot-resize-error.patch
Patch0054: 0054-Clean-up-backup-clone-snapshot-in-exception-handling.patch

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
%setup -q -n cinder-%{version}

%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1
%patch0007 -p1
%patch0008 -p1
%patch0009 -p1
%patch0010 -p1
%patch0011 -p1
%patch0012 -p1
%patch0013 -p1
%patch0014 -p1
%patch0015 -p1
%patch0016 -p1
%patch0017 -p1
%patch0018 -p1
%patch0019 -p1
%patch0020 -p1
%patch0021 -p1
%patch0022 -p1
%patch0023 -p1
%patch0024 -p1
%patch0025 -p1
%patch0026 -p1
%patch0027 -p1
%patch0028 -p1
%patch0029 -p1
%patch0030 -p1
%patch0031 -p1
%patch0032 -p1
%patch0033 -p1
%patch0034 -p1
%patch0035 -p1
%patch0036 -p1
%patch0037 -p1
%patch0038 -p1
%patch0039 -p1
%patch0040 -p1
%patch0041 -p1
%patch0042 -p1
%patch0043 -p1
%patch0044 -p1
%patch0045 -p1
%patch0046 -p1
%patch0047 -p1
%patch0048 -p1
%patch0049 -p1
%patch0050 -p1
%patch0051 -p1
%patch0052 -p1
%patch0053 -p1
%patch0054 -p1

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
* Thu Dec 7 2017 Zhao Chao <chao.zhao@eayun.com> - 2014.2.1-4.7.eayunstack
- add patches 0034-0038, from github pull request #20 (redmine #10587)
- add patches 0039-0043, from github pull request #21 (redmine #10661)
- add patches 0044, from github pull request #22 (redmine #10661, fix Patch 0037)
- add Patches 0045-0048, from github pull request #23 (redmine #9978)
- add Patches 0049-0050, from github pull request #24 (redmine #10289)
- add Patches 0051-0052, from github pull request #25 (redmine #10111)
- add Patche 0053, from github pull request #26 (redmine #11083)
- add Patch 0054, from github pull request #27 (redmine #11278)

* Wed Jun 7 2017 Zhao Chao <chao.zhao@eayun.com> - 2014.2.1-4.6.eayunstack
- add Patch0031: 0031-Uncouple-scheduler-stats-from-volume-creation.patch (pr#19, redmine#9914)
- add Patch0032: 0032-Rbd-update-volume-stats-in-wrong-way.patch
- add Patch0033: 0033-rbd-Change-capacity-calculation-from-integer-to-floa.patch

* Tue May 23 2017 Zhao Chao <chao.zhao@eayun.com> - 2014.2.1-4.5.eayunstack
- add Patch0022: 0022-Get-the-consumer-in-a-correct-way-for-retyping-with-.patch
- add Patch0023: 0023-Use-project-id-from-volume-when-retyping-volumes.patch
- add Patch0024: 0024-Convert-mox-to-mock-tests-compute-test_nova.py.patch
- add Patch0025: 0025-Cleanly-override-config-in-tests.patch
- add Patch0026: 0026-Add-a-privileged-user-for-OpenStack-services.patch
- add Patch0027: 0027-Pass-region-name-to-Nova-client.patch
- add Patch0028: 0028-Add-ability-to-override-OpenStack-privileged-user-au.patch
- add Patch0029: 0029-Support-front-end-qos-updates-in-volume-retype.patch
- add Patch0030: 0030-Correctly-open-rbd-image-in-ceph-backup-driver.patch

* Wed Nov 30 2016 Zhao Chao <chao.zhao@eayun.com> - 2014.2.1-4.4.eayunstack.1.0.1
- add Patch0021: 0021-only-allow-force-create-snapshot-when-volume-is-usab.patch

* Mon Nov 14 2016 Zhao Chao <chao.zhao@eayun.com> - 2014.2.1-4.3.eayunstack.1.0.1
- add Patch0018: 0018-cinder-list-fails-with-name-sort-key.patch
- add Patch0019: 0019-restore-volume-status-in-create_backup-when-backup-s.patch
- add Patch0020: 0020-take-care-of-non-disruptive-backup-when-detaching-a-.patch

* Mon May 16 2016 Zhao Chao <chao.zhao@eayun.com> - 2014.2.1-4.2.eayunstack.1.0.1
- add Patch0012: 0012-unittest-fix-test_migration_027.patch
- add Patch0013: 0013-Non-disruptive-backup.patch
- add Patch0014: 0014-Fix-cleanup_temp_volume_snapshots-for-missing-vol.patch
- add Patch0015: 0015-Handle-missing-temp-volume-and-snapshot-during-clean.patch
- add Patch0016: 0016-Fix-backup-init_host-volume-cleanup.patch
- add Patch0017: 0017-backup-init_host-cleanup-exception-handling.patch

* Thu Apr 28 2016 Zhao Chao <chao.zhao@eayun.com> - 2014.2.1-4.1.eayunstack.1.0.1
- add Patch0011: 0011-Fix-the-unicode-encode-error-when-create-volume.patch

* Fri Dec 11 2015 Dunrong Huang <dunrong.huang@eayun.com> - 2014.2.1-4.eayunstack.1.0.1
- add Patch0006: 0006-Volume-type-access-extension.patch
- add Patch0007: 0007-private-type-fix-db-scripts.patch
- add Patch0008: 0008-usd-is_uuid_like-from-oslo_utils.patch
- add Patch0009: 0009-fix-None-object-issue.patch
- add Patch0010: 0010-Choose-volume-type-belong-to-project.patch

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
