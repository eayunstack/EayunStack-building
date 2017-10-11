%global USE_FIPSCHECK true
%global USE_LIBCAP_NG true
%global USE_LABELED_IPSEC true
%global USE_CRL_FETCHING true
%global USE_DNSSEC true
%global USE_NM true
%global USE_LINUX_AUDIT true

%global _hardened_build 1

%global buildefence 0
%global development 0

#global prever rc1

Name: libreswan
Summary: IPsec implementation with IKEv1 and IKEv2 keying protocols
Version: 3.12
Release: %{?prever:0.}5%{?prever:.%{prever}}%{?dist}
License: GPLv2
Url: https://www.libreswan.org/
Source: https://download.libreswan.org/%{name}-%{version}%{?prever}.tar.gz
Group: System Environment/Daemons
BuildRequires: gmp-devel bison flex redhat-rpm-config pkgconfig
BuildRequires: systemd
Requires(post): coreutils bash systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: iproute

Patch1: libreswan-3.12-1052811.patch
Patch2: libreswan-3.12-1105171-manpage.patch
Patch3: libreswan-3.12-1144120-camellia-ikev2.patch
Patch4: libreswan-3.12-1074018-audit.patch
Patch5: libreswan-3.12-1131503-invalid-ke.patch
Patch6: libreswan-3.12-1134297-aes_ctr.patch
Patch7: libreswan-3.12-1162770-gcm-man.patch
Patch8: libreswan-3.12-826264-ike-aes-gcm.patch

Conflicts: openswan < %{version}-%{release}
Obsoletes: openswan < %{version}-%{release}
Provides: openswan = %{version}-%{release}
Provides: openswan-doc = %{version}-%{release}

BuildRequires: pkgconfig hostname
BuildRequires: nss-devel >= 3.12.6-2, nspr-devel
BuildRequires: pam-devel
%if %{USE_DNSSEC}
BuildRequires: unbound-devel
%endif
%if %{USE_FIPSCHECK}
BuildRequires: fipscheck-devel
# we need fipshmac
Requires: fipscheck%{_isa}
%endif
%if %{USE_LINUX_AUDIT}
Buildrequires: audit-libs-devel
%endif

%if %{USE_LIBCAP_NG}
BuildRequires: libcap-ng-devel
%endif
%if %{USE_CRL_FETCHING}
BuildRequires: openldap-devel curl-devel
%endif
%if %{buildefence}
BuildRequires: ElectricFence
%endif
# Needed if xml man pages are modified and need regeneration
BuildRequires: xmlto

Requires: nss-tools, nss-softokn

%description
Libreswan is a free implementation of IPsec & IKE for Linux.  IPsec is
the Internet Protocol Security and uses strong cryptography to provide
both authentication and encryption services.  These services allow you
to build secure tunnels through untrusted networks.  Everything passing
through the untrusted net is encrypted by the ipsec gateway machine and
decrypted by the gateway at the other end of the tunnel.  The resulting
tunnel is a virtual private network or VPN.

This package contains the daemons and userland tools for setting up
Libreswan. To build KLIPS, see the kmod-libreswan.spec file.

Libreswan also supports IKEv2 (RFC4309) and Secure Labeling

Libreswan is based on Openswan-2.6.38 which in turn is based on FreeS/WAN-2.04

%prep
%setup -q -n libreswan-%{version}%{?prever}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
# remove man page for ipsec.conf so it is forced to regenerate
rm ./programs/configs/ipsec.conf.5

%build
%if %{buildefence}
 %define efence "-lefence"
%endif

#796683: -fno-strict-aliasing
%{__make} \
%if %{development}
   USERCOMPILE="-g -DGCC_LINT %(echo %{optflags} | sed -e s/-O[0-9]*/ /) %{?efence} -fPIE -pie -fno-strict-aliasing -Wformat-nonliteral -Wformat-security" \
%else
  USERCOMPILE="-g -DGCC_LINT %{optflags} %{?efence} -fPIE -pie -fno-strict-aliasing -Wformat-nonliteral -Wformat-security" \
%endif
  USERLINK="-g -pie -Wl,-z,relro,-z,now %{?efence}" \
  INITSYSTEM=systemd \
  USE_NM=%{USE_NM} \
  USE_XAUTHPAM=true \
%if %{USE_FIPSCHECK}
  USE_FIPSCHECK="%{USE_FIPSCHECK}" \
  FIPSPRODUCTCHECK=/etc/system-fips \
%endif
  USE_LIBCAP_NG="%{USE_LIBCAP_NG}" \
  USE_LABELED_IPSEC="%{USE_LABELED_IPSEC}" \
  USE_LINUX_AUDIT="%{USE_LINUX_AUDIT}" \
%if %{USE_CRL_FETCHING}
  USE_LDAP=true \
  USE_LIBCURL=true \
%endif
  USE_DNSSEC="%{USE_DNSSEC}" \
  INC_USRLOCAL=%{_prefix} \
  FINALLIBDIR=%{_libexecdir}/ipsec \
  FINALLIBEXECDIR=%{_libexecdir}/ipsec \
  MANTREE=%{_mandir} \
  INC_RCDEFAULT=%{_initrddir} \
  programs
FS=$(pwd)

%if %{USE_FIPSCHECK}
# Add generation of HMAC checksums of the final stripped binaries
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
  fipshmac -d %{buildroot}%{_libdir}/fipscheck %{buildroot}%{_libexecdir}/ipsec/* \
  fipshmac -d %{buildroot}%{_libdir}/fipscheck %{buildroot}%{_sbindir}/ipsec \
%{nil}
%endif

%install
rm -rf ${RPM_BUILD_ROOT}
%{__make} \
  DESTDIR=%{buildroot} \
  INC_USRLOCAL=%{_prefix} \
  FINALLIBDIR=%{_libexecdir}/ipsec \
  FINALLIBEXECDIR=%{_libexecdir}/ipsec \
  MANTREE=%{buildroot}%{_mandir} \
  INC_RCDEFAULT=%{_initrddir} \
  INSTMANFLAGS="-m 644" \
  INITSYSTEM=systemd \
  install
FS=$(pwd)
rm -rf %{buildroot}/usr/share/doc/libreswan

install -d -m 0755 %{buildroot}%{_localstatedir}/run/pluto
# used when setting --perpeerlog without --perpeerlogbase
install -d -m 0700 %{buildroot}%{_localstatedir}/log/pluto/peer
install -d %{buildroot}%{_sbindir}

%if %{USE_FIPSCHECK}
mkdir -p %{buildroot}%{_libdir}/fipscheck
install -d %{buildroot}%{_sysconfdir}/prelink.conf.d/
install -m644 packaging/fedora/libreswan-prelink.conf %{buildroot}%{_sysconfdir}/prelink.conf.d/libreswan-fips.conf
%endif

echo "include /etc/ipsec.d/*.secrets" > %{buildroot}%{_sysconfdir}/ipsec.secrets
rm -fr %{buildroot}/etc/rc.d/rc*

%files
%doc CHANGES COPYING CREDITS README* LICENSE
%doc docs/*.* docs/examples

%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ipsec.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/pluto
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ipsec.secrets
%attr(0700,root,root) %dir %{_sysconfdir}/ipsec.d
%attr(0700,root,root) %dir %{_sysconfdir}/ipsec.d/cacerts
%attr(0700,root,root) %dir %{_sysconfdir}/ipsec.d/crls
%attr(0700,root,root) %dir %{_sysconfdir}/ipsec.d/policies
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ipsec.d/policies/*
%attr(0700,root,root) %dir %{_localstatedir}/log/pluto/peer
%attr(0755,root,root) %dir %{_localstatedir}/run/pluto
%attr(0644,root,root) %{_unitdir}/ipsec.service
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/pluto
%{_sbindir}/ipsec
%{_libexecdir}/ipsec
%doc %{_mandir}/*/*

%if %{USE_FIPSCHECK}
%{_libdir}/fipscheck/*.hmac
# We own the directory so we don't have to require prelink
%attr(0755,root,root) %dir %{_sysconfdir}/prelink.conf.d/
%{_sysconfdir}/prelink.conf.d/libreswan-fips.conf
%endif

%preun
%systemd_preun ipsec.service

%postun
%systemd_postun_with_restart ipsec.service

%post
%systemd_post ipsec.service
if [ ! -f %{_sysconfdir}/ipsec.d/cert8.db ] ; then
    certutil -N -d %{_sysconfdir}/ipsec.d --empty-password || :
    restorecon %{_sysconfdir}/ipsec.d/*db 2>/dev/null || :
fi

%changelog
* Tue Jan 20 2015 Paul Wouters <pwouters@redhat.com> - 3.12-5
- Resolves: rhbz#826264 aes-gcm implementation support (for IKEv2)
- Resolves: rhbz#1074018 Audit key agreement (integ gcm fixup)

* Tue Dec 30 2014 Paul Wouters <pwouters@redhat.com> - 3.12-4
- Resolves: rhbz#1134297 aes-ctr cipher is not supported
- Resolves: rhbz#1131503 non-zero rSPI on INVALID_KE (and proper INVALID_KE handling)

* Thu Dec 04 2014 Paul Wouters <pwouters@redhat.com> - 3.12-2
- Resolves: rhbz#1105171 (Update man page entry)
- Resolves: rhbz#1144120 (Update for ESP CAMELLIA with IKEv2)
- Resolves: rhbz#1074018 Audit key agreement

* Fri Nov 07 2014 Paul Wouters <pwouters@redhat.com> - 3.12-1
- Resolves: rhbz#1136124 rebase to libreswan 3.12
- Resolves: rhbz#1052811 [TAHI] (also clear reserved flags for isakmp_sa header)
- Resolves: rhbz#1157379 [TAHI][IKEv2] IKEv2.EN.R.1.3.3.1: Non RESERVED fields in INFORMATIONAL request

* Mon Oct 27 2014 Paul Wouters <pwouters@redhat.com> - 3.11-2
- Resolves: rhbz#1136124 rebase to libreswan 3.11 (coverity fixup, dpdaction=clear fix)

* Wed Oct 22 2014 Paul Wouters <pwouters@redhat.com> - 3.11-1
- Resolves: rhbz#1136124 rebase to libreswan 3.11
- Resolves: rhbz#1099905 ikev2 delete payloads are not delivered to peer
- Resolves: rhbz#1147693 NetworkManger-libreswan can not connect to Red Hat IPSec Xauth VPN
- Resolves: rhbz#1055865 [TAHI][IKEv2] libreswan do not ignore the content of version bit
- Resolves: rhbz#1146106 Pluto crashes after start when some ah algorithms are used
- Resolves: rhbz#1108256 addconn compatibility with openswan
- Resolves: rhbz#1152625 [TAHI][IKEv2] IKEv2.EN.I.1.1.6.2 Part D: Integrity Algorithm AUTH_AES_XCBC_96 fail
- Resolves: rhbz#1119704 [TAHI][IKEv2]IKEv2Interop.1.13a test fail
- Resolves: rhbz#1100261 libreswan does not send response when when it receives Delete Payload for a CHILD_SA
- Resolves: rhbz#1100239 ikev2 IKE SA responder does not send delete request to IKE SA initiator
- Resolves: rhbz#1052811 [TAHI][IKEv2]IKEv2.EN.I.1.1.11.1: Non zero RESERVED fields in IKE_SA_INIT response
- Resolves: rhbz#1126868 ikev2 sequence numbers are implemented incorrectly
- Resolves: rhbz#1145245 Libreswan appears to start with systemd before all the NICs are up and running.
- Resolves: rhbz#1145231 libreswan 3.10 upgrade breaks old ipsec.secrets configs
- Resolves: rhbz#1144123 Add ESP support for AES_XCBC hash for USGv6 and IPsec-v3 compliance
- Resolves: rhbz#1144120 Add ESP support for CAMELLIA for USGv6 and IPsec-v3 compliance
- Resolves: rhbz#1099877 Missing man-pages ipsec_whack, ipsec_manual
- Resolves: rhbz#1100255 libreswan Ikev2 implementation does not send an INFORMATIONAL response when it receives an INFORMATIONAL request with a Delete Payload for an IKE_SA

* Tue Sep 09 2014 Paul Wouters <pwouters@redhat.com> - 3.10-3
- Resolves: rhbz#1136124 rebase to 3.10 (auto=route bug on startup)

* Mon Sep 08 2014 Paul Wouters <pwouters@redhat.com> - 3.10-2
- Resolves: rhbz#1136124 rebase to libreswan 3.10

* Mon Jul 14 2014 Paul Wouters <pwouters@redhat.com> - 3.8-6
- Resolves: rhbz#1092047 pluto cannot write to directories not owned by root

* Thu Apr 10 2014 Paul Wouters <pwouters@redhat.com> - 3.8-5
- Resolves: rhbz#1052834 create_child_sa message ID handling


* Tue Mar 18 2014 Paul Wouters <pwouters@redhat.com> - 3.8-4
- Resolves: rhbz#1052834 create_child_sa response

* Wed Mar 05 2014 Paul Wouters <pwouters@redhat.com> - 3.8-3
- Resolves: rhbz#1069024  erroneous debug line with mixture [...]
- Resolves: rhbz#1030939 update nss/x509 documents, don't load acerts
- Resolves: rhbz#1058813 newhostkey returns zero value when it fails

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.8-2
- Mass rebuild 2014-01-24

* Thu Jan 16 2014 Paul Wouters <pwouters@redhat.com> - 3.8-1
- Resolves: rhbz#CVE-2013-6467 
- Resolves: rhbz#1043642 rebase to version 3.8
- Resolves: rhbz#1029912 ipsec force-reload doesn't work
- Resolves: rhbz#826261 Implement SHA384/512 support for Openswan
- Resolves: rhbz#1039655 ipsec newhostkey generates false configuration

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.6-3
- Mass rebuild 2013-12-27

* Fri Nov 08 2013 Paul Wouters <pwouters@redhat.com> - 3.6-2
- Fix race condition in post for creating nss db

* Thu Oct 31 2013 Paul Wouters <pwouters@redhat.com> - 3.6-1
- Updated to version 3.6 (IKEv2, MODECFG, Cisco interop fixes)
- Generate empty NSS db if none exists
- FIPS update using /etc/system-fips
- Provide: openswan-doc

* Fri Aug 09 2013 Paul Wouters <pwouters@redhat.com> - 3.5-2
- rebuilt and bumped EVR to avoid confusion of import->delete->import
- require iproute

* Mon Jul 15 2013 Paul Wouters <pwouters@redhat.com> - 3.5-1
- Initial package for RHEL7
- Added interop patch for (some?) Cisco VPN clients sending 16 zero
  bytes of extraneous IKE data
- Removed fipscheck_version
