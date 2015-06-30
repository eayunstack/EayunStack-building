%global dist_eayunstack .eayunstack.1.0

Name:             python-glanceclient
Epoch:            1
Version:          0.15.0
Release:          2%{?dist_eayunstack}
Summary:          Python API and CLI for OpenStack Glance

Group:            Development/Languages
License:          ASL 2.0
URL:              http://github.com/openstack/python-glanceclient
Source0:          https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

Patch0001: 0001-Remove-runtime-dependency-on-python-pbr.patch
Patch0002: 0002-Fix-Requests-breaking-download-progress-bar.patch

BuildArch:        noarch
BuildRequires:    python2-devel
BuildRequires:    python-setuptools
BuildRequires:    python-d2to1
BuildRequires:    python-pbr
BuildRequires:    python-oslo-sphinx

Requires:         python-httplib2
Requires:         python-keystoneclient
Requires:         python-oslo-utils
Requires:         python-prettytable
Requires:         python-requests >= 2.2.0
Requires:         python-setuptools
Requires:         python-warlock
Requires:         pyOpenSSL

%description
This is a client for the OpenStack Glance API. There's a Python API (the
glanceclient module), and a command-line script (glance). Each implements
100% of the OpenStack Glance API.


%package doc
Summary:          Documentation for OpenStack Nova API Client
Group:            Documentation

BuildRequires:    python-sphinx

%description      doc
This is a client for the OpenStack Glance API. There's a Python API (the
glanceclient module), and a command-line script (glance). Each implements
100% of the OpenStack Glance API.

This package contains auto-generated documentation.


%prep
%setup -q

%patch0001 -p1
%patch0002 -p1

# We provide version like this in order to remove runtime dep on pbr.
sed -i s/REDHATGLANCECLIENTVERSION/%{version}/ glanceclient/__init__.py

# Remove bundled egg-info
rm -rf python_glanceclient.egg-info
# let RPM handle deps
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py
rm -rf {,test-}requirements.txt

sed -i 's/oslosphinx/oslo.sphinx/' doc/source/conf.py

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html

# generate man page
sphinx-build -b man doc/source man
install -p -D -m 644 man/glance.1 %{buildroot}%{_mandir}/man1/glance.1


%files
%doc README.rst
%doc LICENSE
%{_bindir}/glance
%{python_sitelib}/glanceclient
%{python_sitelib}/*.egg-info
%{_mandir}/man1/glance.1.gz

%files doc
%doc html


%changelog
* Thu Jun 30 2015 Zhe Ma <zhe.ma@eayun.com> - 2014.2.1-4.eayunstack.1.0
- add 0002-Fix-Requests-breaking-download-progress-bar.patch (redmine#4331)

* Tue Jan 13 2015 Jakub Ruzicka <jruzicka@redhat.com> 1:0.15.0-1
- Update to upstream 0.15.0

* Tue Nov 25 2014 Haikel Guemar <hguemar@redhat.com> 1:0.14.2-2
- Pulls the right version of python-requests (RHBZ #1166894)

* Mon Nov 17 2014 Haikel Guemar <hguemar@fedoraproject.org> 1:0.14.2-1
- Update to upstream 0.14.2
- New Requires: python-oslo-utils

* Thu Sep 25 2014 Jakub Ruzicka <jruzicka@redhat.com> 1:0.14.1-1
- Update to upstream 0.14.1
- New Requires: python-requests
- New BuildRequires: python-oslo-sphinx
- oslosphinx -> oslo.sphinx fix

* Thu Jul 31 2014 Jakub Ruzicka <jruzicka@redhat.com> 1:0.13.1-1
- Update to upstream 0.13.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov 19 2013 Jakub Ruzicka <jruzicka@redhat.com> 1:0.12.0-1
- Update to upstream 0.12.0
- Provide upstream man page

* Fri Aug 16 2013 Jakub Ruzicka <jruzicka@redhat.com> - 1:0.10.0-2
- Bump release as previous build failed due to pbr package problem.

* Wed Aug 14 2013 Jakub Ruzicka <jruzicka@redhat.com> - 1:0.10.0-1
- Update to upstream 0.10.0.
- Remove runtime dependency on python-pbr.
- Add doc package.
- New BuildRequires: python2-devel, python-d2to1, python-pbr
- Remove python-keystoneclient version cap.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 06 2013 Jakub Ruzicka <jruzicka@redhat.com> - 1:0.9.0-2
- versioninfo is gone from tarball, generate it.

* Mon May 06 2013 Jakub Ruzicka <jruzicka@redhat.com> - 1:0.9.0-1
- Update to 0.9.0.
- Include selected fixes.

* Wed Mar 27 2013 Pádraig Brady <P@draigBrady.com> - 1:0.8.0-2
- Add a dependency on pyOpenSSL

* Mon Mar 11 2013 Jakub Ruzicka <jruzicka@redhat.com> - 1:0.8.0-1
- Update to 0.8.0.
- Switch from tarballs.openstack.org to pypi sources.

* Wed Jan 30 2013 Alan Pevec <apevec@redhat.com> 1:0.7.0-1
- Update to 0.7.0

* Fri Nov 23 2012 Alan Pevec <apevec@redhat.com> 1:0.6.0-1
- Update to 0.6.0

* Sat Sep 15 2012 Alan Pevec <apevec@redhat.com> 1:0.5.1-1
- Update to 0.5.1

* Wed Aug 22 2012 Alan Pevec <apevec@redhat.com> 1:0.4.1-1
- Add dependency on python-setuptools (#850844)
- Revert client script rename, old glance client is now deprecated.
- New upstream release.

* Fri Aug 03 2012 Alan Pevec <apevec@redhat.com> 2012.2-0.3.f1
- rename client script to avoid conflict with old glance client

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012.2-0.2.f1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Pádraig Brady <P@draigBrady.com> 2012.2-0.1.f1
- Initial (folsom-1) release
