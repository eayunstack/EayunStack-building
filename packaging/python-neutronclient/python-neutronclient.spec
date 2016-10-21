%global dist_eayunstack .eayunstack.1.0.1

Name:       python-neutronclient
Version:    2.3.9
Release:    4%{?dist_eayunstack}
Summary:    Python API and CLI for OpenStack Neutron

Group:      Development/Languages
License:    ASL 2.0
URL:        http://launchpad.net/python-neutronclient/
Source0:    https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

Patch0001: 0001-Remove-runtime-dependency-on-python-pbr.patch
Patch0002: 0002-Add-floating-ip-address-to-floatingip-create.patch
Patch0003: 0003-Add-external-fixed-ip-to-router-gateway-set.patch
Patch0004: 0004-Add-eayun_qos-support.patch
Patch0005: 0005-fix-the-firewall-rule-arg-split-error.patch
Patch0006: 0006-Add-Portmapping-support.patch
Patch0007: 0007-Add-pptp-vpn-credential-support.patch
Patch0008: 0008-neutron-CLI-Add-support-lbaas-add-remove-command.patch

BuildArch:  noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr
BuildRequires: python-d2to1

Requires: pyparsing
Requires: python-cliff >= 1.0
Requires: python-keystoneclient >= 0.9.0
Requires: python-prettytable >= 0.6
Requires: python-requests
Requires: python-setuptools
Requires: python-simplejson

%description
Client library and command line utility for interacting with Openstack
Neutron's API.

%prep
%setup -q -n %{name}-%{version}

%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1
%patch0007 -p1
%patch0008 -p1

# We provide version like this in order to remove runtime dep on pbr.
sed -i s/REDHATNEUTRONCLIENTVERSION/%{version}/ neutronclient/version.py

# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Install other needed files
install -p -D -m 644 tools/neutron.bash_completion \
    %{buildroot}%{_sysconfdir}/bash_completion.d/neutron.bash_completion

# Remove unused files
rm -rf %{buildroot}%{python_sitelib}/neutronclient/tests

%files
%doc LICENSE
%doc README.rst
%{_bindir}/neutron
%{python_sitelib}/neutronclient
%{python_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d

%changelog
* Fri Oct 21 2016 Xu Meihong <meihong.xu@eayun.com> 2.3.9-4.eayunstack.1.0.1
- add 0006-Add-Portmapping-support.patch
- add 0007-Add-pptp-vpn-credential-support.patch
- add 0008-neutron-CLI-Add-support-lbaas-add-remove-command.patch (redmine#7581)

* Thu May 21 2015 Xu Meihong <meihong.xu@eayun.com> 2.3.9-3.eayunstack.1.0
- add 0005-fix-the-firewall-rule-arg-split-error.patch (redmine#3720)

* Mon May 11 2015 Xu Meihong <meihong.xu@eayun.com> 2.3.9-2.eayunstack.1.0
- Fix redmine #3652
- Fix redmine #3677

* Mon Oct 13 2014 Jakub Ruzicka <jruzicka@redhat.com> 2.3.9-1
- Update to upstream 2.3.9

* Thu Aug 21 2014 Jakub Ruzicka <jruzicka@redhat.com> 2.3.6-2
- Fix listing security group rules

* Mon Aug 04 2014 Jakub Ruzicka <jruzicka@redhat.com> 2.3.6-1
- Update to upstream 2.3.6
- New requirements: python-requests, python-keystoneclient

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 25 2014 Jakub Ruzicka <jruzicka@redhat.com> 2.3.4-1
- Update to upstream 2.3.4

* Mon Jan 13 2014 Jakub Ruzicka <jruzicka@redhat.com> 2.3.3-1
- Update to upstream 2.3.3

* Fri Nov 01 2013 Jakub Ruzicka <jruzicka@redhat.com> - 2.3.1-2
- Don't obsolete python-quantumclient (#1025509)

* Tue Oct 08 2013 Jakub Ruzicka <jruzicka@redhat.com> - 2.3.1-1
- Update to upstream 2.3.1.

* Mon Sep 09 2013 Jakub Ruzicka <jruzicka@redhat.com> - 2.3.0-1
- Update to upstream 2.3.0.

* Wed Aug 28 2013 Jakub Ruzicka <jruzicka@redhat.com> - 2.2.6-2
- Remove all pbr deps in the patch instead of this spec file.

* Wed Aug 21 2013 Jakub Ruzicka <jruzicka@redhat.com> - 2.2.6-1
- Update to upstream 2.2.6.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Jakub Ruzicka <jruzicka@redhat.com> - 1:2.2.4-1
- Initial package based on python-quantumclient.
- Removed runtime dependency on python-pbr.
