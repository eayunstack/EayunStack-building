%global sname oslo.messaging
%global milestone a5
%global dist_eayunstack .eayunstack

Name:       python-oslo-messaging
Version:    1.4.1
Release:    6%{?dist_eayunstack}
Summary:    OpenStack common messaging library

Group:      Development/Languages
License:    ASL 2.0
URL:        https://launchpad.net/oslo
Source0:    https://pypi.python.org/packages/source/o/%{sname}/%{sname}-1.4.1.tar.gz

Patch0001: 0001-update-requirements-to-pass-unittest.patch
Patch0002: 0002-Cleanup-listener-after-stopping-rpc-server.patch
Patch0003: 0003-Don-t-put-the-message-payload-into-warning-log.patch
Patch0004: 0004-Enable-user-authentication-in-the-AMQP-1.0-driver.patch
Patch0005: 0005-Notification-listener-pools.patch
Patch0006: 0006-rabbit-uses-kombu-instead-of-builtin-stuffs.patch
Patch0007: 0007-Create-a-new-connection-when-a-process-fork-has-been.patch
Patch0008: 0008-Fix-reconnect-race-condition-with-RabbitMQ-cluster.patch
Patch0009: 0009-Have-the-timeout-decrement-inside-the-wait-method.patch
Patch0010: 0010-Always-use-a-poll-timeout-in-the-executor.patch
Patch0011: 0011-Set-correctly-the-messaging-driver-to-use-in-tests.patch
Patch0012: 0012-Don-t-use-oslo.cfg-to-set-kombu-in-memory-driver.patch
Patch0013: 0013-Rabbit-iterconsume-must-honor-timeout.patch
Patch0014: 0014-Reintroduces-fake_rabbit-config-option.patch
Patch0015: 0015-rabbit-more-precise-iterconsume-timeout.patch
Patch0016: 0016-qpid-honor-iterconsume-timeout.patch
Patch0017: 0017-The-executor-doesn-t-need-to-set-the-timeout.patch
Patch0018: 0018-Fix-some-comments-in-a-backporting-review-session.patch
Patch0019: 0019-safe_log-Sanitize-Passwords-in-List-of-Dicts.patch
Patch0020: 0020-rabbit-fix-timeout-timer-when-duration-is-None.patch
Patch0021: 0021-Ensure-kombu-channels-are-closed.patch
Patch0022: 0022-Declare-DirectPublisher-exchanges-with-passive-True.patch
Patch0023: 0023-Fix-TypeError-caused-by-err_msg-formatting.patch
Patch0024: 0024-Refactor-the-replies-waiter-code.patch
Patch0025: 0025-Remove-unuseful-param-of-the-ConnectionContext.patch
Patch0026: 0026-rabbit-Fix-behavior-of-rabbit_use_ssl.patch
Patch0027: 0027-Speedup-the-rabbit-tests.patch
Patch0028: 0028-rabbit-heartbeat-implementation.patch
Patch0029: 0029-cleanup-connection-pool-return.patch
Patch0030: 0030-Reconnect-on-connection-lost-in-heartbeat-thread.patch
Patch0031: 0031-rabbit-redeclare-consumers-when-ack-requeue-fail.patch
Patch0032: 0032-Fix-list_opts-test-to-not-check-all-deps.patch
Patch0033: 0033-log-reconnection-event-after-reconnected.patch
Patch0034: 0034-check-the-connection-status-before-heartbeating.patch

BuildArch:  noarch
Requires:   python-setuptools
Requires:   python-iso8601
Requires:   python-oslo-config >= 1:1.2.1
Requires:   python-six >= 1.6
Requires:   python-stevedore
Requires:   PyYAML
Requires:   python-kombu
Requires:   python-qpid
Requires:   python-babel

# FIXME: this dependency will go away soon
Requires:   python-eventlet >= 0.13.0

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr
BuildRequires: python-d2to1

%description
The Oslo project intends to produce a python library containing
infrastructure code shared by OpenStack projects. The APIs provided
by the project should be high quality, stable, consistent and generally
useful.

The Oslo messaging API supports RPC and notifications over a number of
different messaging transports.

%package doc
Summary:    Documentation for OpenStack common messaging library
Group:      Documentation

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx

# Needed for autoindex which imports the code
BuildRequires: python-iso8601
BuildRequires: python-oslo-config
BuildRequires: python-six
BuildRequires: python-stevedore
BuildRequires: PyYAML
BuildRequires: python-babel

%description doc
Documentation for the oslo.messaging library.

%prep
%setup -q -n %{sname}-%{version}

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

# Remove bundled egg-info
rm -rf %{sname}.egg-info
# let RPM handle deps
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt

# make doc build compatible with python-oslo-sphinx RPM
sed -i 's/oslosphinx/oslo.sphinx/' doc/source/conf.py

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/tests

export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html -d build/doctrees   source build/html
popd
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo

%check

%files
%doc README.rst LICENSE
%{python_sitelib}/oslo
%{python_sitelib}/*.egg-info
%{python_sitelib}/*-nspkg.pth
%{_bindir}/oslo-messaging-zmq-receiver

%files doc
%doc doc/build/html LICENSE

%changelog
* Tue Mar 08 2016 apporc <appleorchard2000@gmail.com> - 1.4.1-6.eayunstack.1.1
- 0034-check-the-connection-status-before-heartbeating.patch

* Wed Jan 06 2016 apporc <appleorchard2000@gmail.com> - 1.4.1-5.eayunstack.1.1
- delete patch 0001-Enable-user-authentication-in-the-AMQP-1.0-driver.patch
- delete patch 0002-Create-a-new-connection-when-a-process-fork-has-been.patch
- delete patch 0003-Fix-typo-in-reconnect-exception-handler.patch
- delete patch 0004-Fix-_poll_connection-not-timeout-issue-1-2.patch
- delete patch 0005-update-requirements-to-pass-unittest.patch
- delete patch 0006-Fix-_poll_connection-not-timeout-issue-2-2.patch
- delete patch 0007-Fix-possible-usage-of-undefined-variable.patch
- delete patch 0008-rabbit-redeclare-consumers-when-ack-requeue-fail.patch
- delete patch 0009-Fix-list_opts-test-to-not-check-all-deps.patch
- add patch 0001-update-requirements-to-pass-unittest.patch
- add patch 0002-Cleanup-listener-after-stopping-rpc-server.patch
- add patch 0003-Don-t-put-the-message-payload-into-warning-log.patch
- add patch 0004-Enable-user-authentication-in-the-AMQP-1.0-driver.patch
- add patch 0005-Notification-listener-pools.patch
- add patch 0006-rabbit-uses-kombu-instead-of-builtin-stuffs.patch
- add patch 0007-Create-a-new-connection-when-a-process-fork-has-been.patch
- add patch 0008-Fix-reconnect-race-condition-with-RabbitMQ-cluster.patch
- add patch 0009-Have-the-timeout-decrement-inside-the-wait-method.patch
- add patch 0010-Always-use-a-poll-timeout-in-the-executor.patch
- add patch 0011-Set-correctly-the-messaging-driver-to-use-in-tests.patch
- add patch 0012-Don-t-use-oslo.cfg-to-set-kombu-in-memory-driver.patch
- add patch 0013-Rabbit-iterconsume-must-honor-timeout.patch
- add patch 0014-Reintroduces-fake_rabbit-config-option.patch
- add patch 0015-rabbit-more-precise-iterconsume-timeout.patch
- add patch 0016-qpid-honor-iterconsume-timeout.patch
- add patch 0017-The-executor-doesn-t-need-to-set-the-timeout.patch
- add patch 0018-Fix-some-comments-in-a-backporting-review-session.patch
- add patch 0019-safe_log-Sanitize-Passwords-in-List-of-Dicts.patch
- add patch 0020-rabbit-fix-timeout-timer-when-duration-is-None.patch
- add patch 0021-Ensure-kombu-channels-are-closed.patch
- add patch 0022-Declare-DirectPublisher-exchanges-with-passive-True.patch
- add patch 0023-Fix-TypeError-caused-by-err_msg-formatting.patch
- add patch 0024-Refactor-the-replies-waiter-code.patch
- add patch 0025-Remove-unuseful-param-of-the-ConnectionContext.patch
- add patch 0026-rabbit-Fix-behavior-of-rabbit_use_ssl.patch
- add patch 0027-Speedup-the-rabbit-tests.patch
- add patch 0028-rabbit-heartbeat-implementation.patch
- add patch 0029-cleanup-connection-pool-return.patch
- add patch 0030-Reconnect-on-connection-lost-in-heartbeat-thread.patch
- add patch 0031-rabbit-redeclare-consumers-when-ack-requeue-fail.patch
- add patch 0032-Fix-list_opts-test-to-not-check-all-deps.patch
- add patch 0033-log-reconnection-event-after-reconnected.patch

* Fri Dec 11 2015 apporc <appleorchard2000@gmail.com> - 1.4.1-4.eayunstack.1.0.1
- 0004-Fix-_poll_connection-not-timeout-issue-1-2.patch
- 0005-update-requirements-to-pass-unittest.patch
- 0006-Fix-_poll_connection-not-timeout-issue-2-2.patch
- 0007-Fix-possible-usage-of-undefined-variable.patch
- 0008-rabbit-redeclare-consumers-when-ack-requeue-fail.patch
- 0009-Fix-list_opts-test-to-not-check-all-deps.patch

* Thu Jan 08 2015 Alan Pevec <apevec@redhat.com> - 1.4.1-3
- Fix reconnect exception handler (Dan Smith) rhbz#1175685

* Tue Dec 02 2014 Alan Pevec <apevec@redhat.com> - 1.4.1-2
- AMQP 1.0 driver fixes (Ken Giusti) LP#1392868 LP#1385445

* Sun Sep 21 2014 Alan Pevec <apevec@redhat.com> - 1.4.0.0-4
- Final release 1.4.0

* Wed Sep 17 2014 Alan Pevec <apevec@redhat.com> - 1.4.0.0-3.a5
- Latest upstream

* Wed Jul 09 2014 Pádraig Brady <pbrady@redhat.com> - 1.4.0.0-1
- Latest upstream

* Tue Jun 10 2014 Pádraig Brady <pbrady@redhat.com> - 1.3.0.2-4
- Fix message routing with newer QPID #1103800

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 06 2014 Pádraig Brady <pbrady@redhat.com> - 1.3.0.2-2
- Update python-six dependency to >= 1.6 to support Icehouse

* Thu Apr 24 2014 Pádraig Brady <pbrady@redhat.com> - 1.3.0.2-1
- Update to icehouse stable release
- Add dependency on newer python-eventlet

* Fri Apr 11 2014 Pádraig Brady <pbrady@redhat.com> - 1.3.0-0.2.a9
- Add dependencies on python-kombu, python-qpid, and PyYAML

* Tue Mar 18 2014 Pádraig Brady <pbrady@redhat.com> - 1.3.0-0.1.a9
- Latest upstream

* Tue Feb 11 2014 Pádraig Brady <pbrady@redhat.com> - 1.3.0-0.1.a7
- Update to 1.3.0a7.

* Thu Jan  2 2014 Pádraig Brady <pbrady@redhat.com> - 1.3.0-0.1.a2
- Update to 1.3.0a2.

* Tue Sep  3 2013 Mark McLoughlin <markmc@redhat.com> - 1.2.0-0.1.a11
- Update to a11 development snapshot.

* Mon Aug 12 2013 Mark McLoughlin <markmc@redhat.com> - 1.2.0-0.1.a2
- Initial package.
