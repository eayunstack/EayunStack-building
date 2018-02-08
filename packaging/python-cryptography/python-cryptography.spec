%if 0%{?fedora} > 20
%global with_python3 1
%else
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%global dist_eayunstack .eayunstack.dev

Name:           python-cryptography
Version:        1.2.1
Release:        4%{?dist_eayunstack}
Summary:        PyCA's cryptography library

Group:          Development/Libraries
License:        ASL 2.0 or BSD
URL:            https://cryptography.io/en/latest/
Source0:        https://pypi.python.org/packages/source/c/cryptography/cryptography-%{version}.tar.gz

BuildRequires:  openssl-devel

BuildRequires:  python2-devel
BuildRequires:  pytest
BuildRequires:  python-setuptools
BuildRequires:  python-pretend
BuildRequires:  python2-iso8601
BuildRequires:  python2-cryptography-vectors = %{version}
BuildRequires:  python-pyasn1-modules >= 0.1.6
BuildRequires:  python2-hypothesis

BuildRequires:  python-idna >= 2.0
BuildRequires:  python-pyasn1 >= 0.1.6
BuildRequires:  python-six >= 1.4.1
BuildRequires:  python2-cffi >= 1.4.1
BuildRequires:  python-enum34
BuildRequires:  python-ipaddress

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-setuptools >= 1.0
BuildRequires:  python3-pretend
BuildRequires:  python3-iso8601
BuildRequires:  python3-cryptography-vectors = %{version}
BuildRequires:  python3-pyasn1-modules >= 0.1.8
BuildRequires:  python3-hypothesis

BuildRequires:  python3-idna >= 2.0
BuildRequires:  python3-pyasn1 >= 0.1.8
BuildRequires:  python3-six >= 1.4.1
BuildRequires:  python3-cffi >= 1.4.1
%endif

%description
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.

%package -n  python2-cryptography
Group:          Development/Libraries
Summary:        PyCA's cryptography library
Obsoletes:      python-cryptography <= 1.2.1-1
%{?python_provide:%python_provide python2-cryptography}

Requires:       openssl
Requires:       python-idna >= 2.0
Requires:       python2-pyasn1 >= 0.1.8
Requires:       python-six >= 1.4.1
Requires:       python2-cffi >= 1.4.1
Requires:       python-enum34
Requires:       python-ipaddress

%description -n python2-cryptography
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.

%if 0%{?with_python3}
%package -n  python3-cryptography
Group:          Development/Libraries
Summary:        PyCA's cryptography library
%{?python_provide:%python_provide python3-cryptography}

Requires:       openssl
Requires:       python3-idna >= 2.0
Requires:       python3-pyasn1 >= 0.1.8
Requires:       python3-six >= 1.4.1
Requires:       python3-cffi >= 1.4.1

%description -n python3-cryptography
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.
%endif

%prep
%setup -q -n cryptography-%{version}
# EL7 ships setuptools 0.9.8
sed -i 's/setuptools>=1.0/setuptools/g' setup.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!/usr/bin/python|#!%{__python3}|'
%endif

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif


%install
# Actually other *.c and *.h are appropriate
# see https://github.com/pyca/cryptography/issues/1463
find . -name .keep -print -delete

%{__python2} setup.py install --skip-build --prefix=%{_prefix} --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --prefix=%{_prefix} --root %{buildroot}
popd
%endif


%check
%{__python} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif


%files -n python2-cryptography
%doc LICENSE LICENSE.APACHE LICENSE.BSD README.rst docs
%{python_sitearch}/*


%if 0%{?with_python3}
%files -n python3-cryptography
%doc LICENSE LICENSE.APACHE LICENSE.BSD README.rst docs
%{python3_sitearch}/*
%endif


%changelog
* Tue Jul 11 2017 Tang Cheng <cheng.tang@eayun.com> - 1.2.1-4
- Change python-pyasn1 build requires from 0.1.8 to 0.1.6

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Nathaniel McCallum <npmccallum@redhat.com> - 1.2.1-2
- Move python-cryptograph => python2-cryptography

* Sat Jan 09 2016 Nathaniel McCallum <npmccallum@redhat.com> - 1.2.1-1
- Update to v1.2.1

* Wed Nov 11 2015 Robert Kuska <rkuska@redhat.com> - 1.1-1
- Update to v1.1

* Wed Nov 04 2015 Robert Kuska <rkuska@redhat.com> - 1.0.2-2
- Rebuilt for Python3.5 rebuild

* Wed Sep 30 2015 Matěj Cepl <mcepl@redhat.com> - 1.0.2-1
- New upstream release (fix #1267548)

* Wed Aug 12 2015 Nathaniel McCallum <npmccallum@redhat.com> - 1.0-1
- New upstream release

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Nathaniel McCallum <npmccallum@redhat.com> - 0.9-1
- New upstream release
- Run tests on RHEL
- New deps: python-idna, python-ipaddress

* Fri Apr 17 2015 Nathaniel McCallum <npmccallum@redhat.com> - 0.8.2-1
- New upstream release
- Add python3-pyasn1 Requires (#1211073)

* Tue Apr 14 2015 Matej Cepl <mcepl@redhat.com> - 0.8-2
- Add python-pyasn1 Requires (#1211073)

* Fri Mar 13 2015 Nathaniel McCallum <npmccallum@redhat.com> - 0.8-1
- New upstream release
- Remove upstreamed patch

* Wed Mar 04 2015 Nathaniel McCallum <npmccallum@redhat.com> - 0.7.2-2
- Add python3-cryptography-vectors build requires
- Add python-enum34 requires

* Tue Feb 03 2015 Nathaniel McCallum <npmccallum@redhat.com> - 0.7.2-1
- New upstream release. BSD is now an optional license.
- Fix test running on python3
- Add upstream patch to fix test paths

* Fri Nov 07 2014 Matej Cepl <mcepl@redhat.com> - 0.6.1-2
- Fix requires, for reasons why other development files were not
  eliminated see https://github.com/pyca/cryptography/issues/1463.

* Wed Nov 05 2014 Matej Cepl <mcepl@redhat.com> - 0.6.1-1
- New upstream release.

* Sun Jun 29 2014 Terry Chia <terrycwk1994@gmail.com> 0.4-1
- initial version
