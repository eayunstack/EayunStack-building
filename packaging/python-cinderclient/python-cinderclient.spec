%global dist_eayunstack .eayunstack.1.1

Name:             python-cinderclient
Version:          1.1.1
Release:          4%{?dist_eayunstack}
Summary:          Python API and CLI for OpenStack Cinder

Group:            Development/Languages
License:          ASL 2.0
URL:              http://github.com/openstack/python-cinderclient
Source0:          http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

Patch0001: 0001-Remove-runtime-dependency-on-python-pbr.patch
Patch0002: 0002-Stop-pbr-from-installing-requirements-during-build.patch
Patch0003: 0003-Fix-search_opts-error-with-backup-delete-command.patch
Patch0004: 0004-Add-support-for-os-volume-type-access-extension.patch
Patch0005: 0005-cinderclient-accepts-arguments-after-metadata-withou.patch
Patch0006: 0006-Add-volume-multi-attach-support.patch

BuildArch:        noarch

BuildRequires:    python2-devel
BuildRequires:    python-setuptools
BuildRequires:    python-pbr
BuildRequires:    python-d2to1

Requires:         python-babel
Requires:         python-prettytable
Requires:         python-requests
Requires:         python-setuptools
Requires:         python-simplejson
Requires:         python-six

%description
Client library (cinderclient python module) and command line utility
(cinder) for interacting with OpenStack Cinder (Block Storage) API.


%package doc
Summary:          Documentation for OpenStack Nova API Client
Group:            Documentation

BuildRequires:    python-sphinx
BuildRequires:    python-oslo-sphinx

%description      doc
Client library (cinderclient python module) and command line utility
(cinder) for interacting with OpenStack Cinder (Block Storage) API.

This package contains auto-generated documentation.


%prep
%setup -q

%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1

# We provide version like this in order to remove runtime dep on pbr.
sed -i s/REDHATCINDERCLIENTVERSION/%{version}/ cinderclient/__init__.py

# Remove bundled egg-info
rm -rf python_cinderclient.egg-info

# Let RPM handle the requirements
rm -f {,test-}requirements.txt

sed -i 's/oslosphinx/oslo.sphinx/' doc/source/conf.py

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

install -p -D -m 644 tools/cinder.bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/cinder.bash_completion

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/cinderclient/tests

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html
sphinx-build -b man doc/source man

install -p -D -m 644 man/cinder.1 %{buildroot}%{_mandir}/man1/cinder.1

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

%files
%doc LICENSE README.rst
%{_bindir}/cinder
%{python_sitelib}/cinderclient
%{python_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d/cinder.bash_completion
%{_mandir}/man1/cinder.1*

%files doc
%doc html

%changelog
* Wed Jan 06 2016 Zhao Chao<chao.zhao@eayun.com> 1.1.1-4.eayunstack.1.1
- add 0005-cinderclient-accepts-arguments-after-metadata-withou.patch
- add 0006-Add-volume-multi-attach-support.patch

* Fri Dec 11 2015 Dunrong Huang<dunrong.huang@eayun.com> 1.1.1-3.eayunstack.1.0.1
- add 0004-Add-support-for-os-volume-type-access-extension.patch

* Mon May 11 2015 Zhao Chao <chao.zhao@eayun.com> 1.1.1-2.eayunstack.1.0
- add 0003-Fix-search_opts-error-with-backup-delete-command.patch

* Mon Oct 13 2014 Jakub Ruzicka <jruzicka@redhat.com> 1.1.1-1
- Update to upstream 1.1.1
- New -doc BuildRequires: python-oslo-sphinx
- oslosphinx -> oslo.sphinx fix

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Jakub Ruzicka <jruzicka@redhat.com> 1.0.9-1
- Update to upstream 1.0.9

* Tue Mar 25 2014 Jakub Ruzicka <jruzicka@redhat.com> 1.0.8-1
- Update to upstream 1.0.8
- Remove {test-,}requirements.txt in .spec instead of patch

* Thu Dec 19 2013 Jakub Ruzicka <jruzicka@redhat.com> 1.0.7-2
- Add search_opts into the method list() for VolumeTypeManager (rhbz#1048326)

* Wed Nov 06 2013 Jakub Ruzicka <jruzicka@redhat.com> 1.0.7-1
- Update to upstream version 1.0.7

* Wed Oct 23 2013 Jakub Ruzicka <jruzicka@redhat.com> 1.0.6-2
- Fix DeprecationWarning when printing exception
- Provide -doc package with auto-generated documentation
- Provide upstream manpage
- Improve package description

* Thu Oct 10 2013 Jakub Ruzicka <jruzicka@redhat.com> 1.0.6-1
- Update to upstream 1.0.6

* Thu Sep 19 2013 Jakub Ruzicka <jruzicka@redhat.com> 1.0.5-2
- Add update_snapshot_metadata action

* Thu Sep 12 2013 Jakub Ruzicka <jruzicka@redhat.com> 1.0.5-1
- Update to upstream version 1.0.5.
- Update dependencies.
- Remove runtime dependency on python-pbr.
- Change Source0 to PyPI.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 Jakub Ruzicka <jruzicka@redhat.com> 1.0.4-1
- Update to upstream version 1.0.4.

* Tue Apr 02 2013 Jakub Ruzicka <jruzicka@redhat.com> 1.0.3-1
- Update to upstream version 1.0.3.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 14 2013 Eric Harney <eharney@redhat.com> 1.0.2-1
- Add bash completion support
- Update to latest client

* Tue Sep 25 2012 Pádraig Brady <P@draigBrady.com> 0.2.26-1
- Update to latest client to support latest cinder

* Mon Sep  3 2012 Pádraig Brady <P@draigBrady.com> 0.2-2
- Initial release
