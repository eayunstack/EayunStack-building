%global dist_eayunstack .eayunstack

Name:             python-novaclient
Epoch:            1
Version:          2.20.0
Release:          2%{?dist_eayunstack}
Summary:          Python API and CLI for OpenStack Nova

Group:            Development/Languages
License:          ASL 2.0
URL:              http://pypi.python.org/pypi/%{name}
Source0:          http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

Patch0001: 0001-Remove-runtime-dependency-on-python-pbr.patch
Patch0002: 0002-Use-oslo.sphinx-instead-of-oslosphinx.patch
Patch0003: 0003-Add-support-of-update-Cinder-volume-QoS-Specs.patch

BuildArch:        noarch
BuildRequires:    python-setuptools
BuildRequires:    python2-devel
BuildRequires:    python-d2to1
BuildRequires:    python-pbr

Requires:         python-argparse
Requires:         python-iso8601
Requires:         python-oslo-utils
Requires:         python-prettytable
Requires:         python-requests
Requires:         python-simplejson
Requires:         python-six
Requires:         python-babel
Requires:         python-keystoneclient
Requires:         python-keyring
Requires:         python-setuptools

%description
This is a client for the OpenStack Nova API. There's a Python API (the
novaclient module), and a command-line script (nova). Each implements 100% of
the OpenStack Nova API.

%package doc
Summary:          Documentation for OpenStack Nova API Client
Group:            Documentation

BuildRequires:    python-sphinx
BuildRequires:    python-oslo-sphinx

%description      doc
This is a client for the OpenStack Nova API. There's a Python API (the
novaclient module), and a command-line script (nova). Each implements 100% of
the OpenStack Nova API.

This package contains auto-generated documentation.

%prep
%setup -q

%patch0001 -p1
%patch0002 -p1
%patch0003 -p1

# We provide version like this in order to remove runtime dep on pbr.
sed -i s/REDHATNOVACLIENTVERSION/%{version}/ novaclient/__init__.py

# Remove bundled egg-info
rm -rf python_novaclient.egg-info

# Let RPM handle the requirements
rm -f {,test-}requirements.txt

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -pm 644 tools/nova.bash_completion \
    %{buildroot}%{_sysconfdir}/bash_completion.d/nova

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/novaclient/tests
export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html
sphinx-build -b man doc/source man

install -p -D -m 644 man/nova.1 %{buildroot}%{_mandir}/man1/nova.1

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

%files
%doc README.rst
%doc LICENSE
%{_bindir}/nova
%{python_sitelib}/novaclient
%{python_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d
%{_mandir}/man1/nova.1.gz

%files doc
%doc html

%changelog
* Wed Mar 29 2017 Zhao Chao <chao.zhao@eayun.com> 1:2.20.0-2
- add 0003-Add-support-of-update-Cinder-volume-QoS-Specs.patch

* Fri Oct 03 2014 Jakub Ruzicka <jruzicka@redhat.com> 1:2.20.0-1
- Update to upstream 2.20.0
- New Requires: python-oslo-utils, python-keystoneclient

* Wed Aug 13 2014 Jakub Ruzicka <jruzicka@redhat.com> 1:2.18.1-1
- Update to upstream 2.18.1
- New Requires: python-oslo-sphinx
- Use oslo.sphinx instead of oslosphinx

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.17.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Jakub Ruzicka <jruzicka@redhat.com> 1:2.17.0-2
- Selective backports (server groups and more)
- Nova CLI for server groups (rhbz#1101014)
- Enable delete multiple server groups in one request
- Fix session handling in novaclient
- Fix authentication bug when booting an server in V3
- Avoid AttributeError in servers.Server.__repr__

* Tue Mar 25 2014 Jakub Ruzicka <jruzicka@redhat.com> 1:2.17.0-1
- Update to upstream 2.17.0

* Wed Feb 26 2014 Jakub Ruzicka <jruzicka@redhat.com> 2.16.0-2
- Update to upstream 2.16.0

* Thu Sep 19 2013 Jakub Ruzicka <jruzicka@redhat.com> 
- Update to upstream 2.15.0
- Add python-babel dependency
- Nuke pbr deps handling in patch instead of this spec file

* Wed Aug 07 2013 Jakub Ruzicka <jruzicka@redhat.com> - 1:2.14.1-1
- Update to upstream version 2.14.1.
- New build requires: python-d2to1, python-pbr
- New require: python-six
- Remove runtime dependency on python-pbr.
- Include new manpage.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 03 2013 Jakub Ruzicka <jruzicka@redhat.com> 2.13.0-1
- Update to upstream version 2.13.0. (#921769)
- Update requires from tools/pip-requires.
- versioninfo is gone from tarball, generate it.

* Fri Mar 08 2013 Alan Pevec <apevec@redhat.com> 2.11.1-2
- Add dependency on python-requests and python-keyring (#919337)

* Thu Mar 07 2013 Alan Pevec <apevec@redhat.com> 2.11.1-1
- Update to latest upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 21 2012 Alan Pevec <apevec@redhat.com> 2.10.0-2
- Include bash_completion file (#872544) (Alvaro Lopez Ortega)
- Add dependency on python-iso8601 (#881515)

* Mon Dec 03 2012 Alan Pevec <apevec@redhat.com> 2.10.0-1
- Update to latest upstream release

* Thu Sep 27 2012 Pádraig Brady <P@draigBrady.com> 1:2.9.0-1
- Update to latest upstream release (aligned with Folsom)

* Tue Sep 25 2012 Pádraig Brady <P@draigBrady.com> 1:2.8.0.26-2
- Update to latest upstream release

* Wed Aug 22 2012 Pádraig Brady <P@draigBrady.com> 2012.2-0.3.f1
- Add dependency on python-setuptools (#849477)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012.2-0.2.f1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Pádraig Brady <P@draigBrady.com> 2012.2-0.1.f1
- Update to folsom-1 release

* Sun Apr  8 2012 Pádraig Brady <P@draigBrady.com> 2012.1-1
- Update to essex release
- Include LICENSE (#732695)

* Thu Mar 22 2012 Pádraig Brady <P@draigBrady.com> 2012.1-0.4.rc1
- Avoid a horizon issue trying to write to /var/www (#801202)

* Wed Mar 21 2012 Pádraig Brady <P@draigBrady.com> 2012.1-0.3.rc1
- Update to essex-rc1

* Tue Mar 06 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.2.e4
- Update to essex-4

* Fri Jan 27 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-0.1.e3
- Update to essex milestone 3

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-0.5.89bzr
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 24 2011 Mark McLoughlin <markmc@redhat.com> - 2.6.1-0.4.89bzr
- Update to latest upstream snapshot
- Don't use %%setup -n (#732694)

* Mon Aug 22 2011 Mark McLoughlin <markmc@redhat.com> - 2.6.1-0.3.83bzr
- Remove python-devel BR
- Remove the openstack-novaclient sub-package

* Fri Aug 19 2011 Mark McLoughlin <markmc@redhat.com> - 2.6.1-0.2.83bzr
- Remove argparse from egg requires.txt; no egg info for argparse available

* Wed Aug 17 2011 Mark McLoughlin <markmc@redhat.com> - 2.6.1-0.1.83bz
- Update to latest upstream

* Wed Aug 10 2011 Mark McLoughlin <markmc@redhat.com> - 2.6.1-0.1.74bzr
- Update to latest upstream

* Mon Aug  8 2011 Mark McLoughlin <markmc@redhat.com> - 2.5.1-1
- Initial package from Alexander Sakhnov <asakhnov@mirantis.com>
  with cleanups by Mark McLoughlin
