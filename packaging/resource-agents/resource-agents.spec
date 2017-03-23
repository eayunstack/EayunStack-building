#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
#






# 
# Since this spec file supports multiple distributions, ensure we
# use the correct group for each.
#

%global upstream_prefix ClusterLabs-resource-agents
%global upstream_version 5434e96

%global sap_script_prefix sap_redhat_cluster_connector
%global sap_hash 6353d27

# determine the ras-set to process based on configure invokation
%bcond_with rgmanager
%bcond_without linuxha

%global dist_eayunstack .eayunstack

Name:		resource-agents
Summary:	Open Source HA Reusable Cluster Resource Scripts
Version:	3.9.5
Release:	26.8%{?dist_eayunstack}
License:	GPLv2+ and LGPLv2+
URL:		https://github.com/ClusterLabs/resource-agents
%if 0%{?fedora} || 0%{?centos_version} || 0%{?rhel}
Group:		System Environment/Base
%else
Group:		Productivity/Clustering/HA
%endif
Source0:	%{upstream_prefix}-%{upstream_version}.tar.gz
Source1:	%{sap_script_prefix}-%{sap_hash}.tar.gz
Patch1:		bz984054.patch		
Patch2:		bz884164-multi-lib-fixes.patch
Patch3:		bz10005924-default-apache-config.patch
Patch4:		bz799065-apache-simple-monitor.patch
Patch5:		fix-LVM-clvmd-retry.patch
Patch6:		bz917806-oracle-tns-admin.patch
Patch7:		bz917681-VirtualDomain-heartbeat-updates.patch
Patch8:		bz917681_nodename_fixes.patch
Patch9:		bz1014641-VirtualDomain-syntax-error.patch 
Patch10:	bz917681-VirtualDomain-heartbeat-updates_v2.patch
Patch11:	bz1016140-start-predefined-domains.patch
Patch12:	bz917681-ipv6-send_ua-fix.patch
Patch13:	bz917681-ocft_fedora_supported_test_cases.patch
Patch14:	bz1033016-nfsserver-missing-etab.patch
Patch15:	bz917681-slapd-heartbeat-updates.patch
Patch16:	bz917681-tomcat-heartbeat-updates.patch
Patch17:	bz1029061-virtualdomain-parse-error.patch 
Patch18:	bz1064512-clvmd-agent.patch
Patch19:	bz1060367-vm-monitor-wo-libvirtd.patch
Patch20:	bz1060367-vm-monitor-wo-libvirtd_2.patch
Patch21:	bz1091101-nfs-updates.patch
Patch22:	bz1091101-nfs-error-msg-fix.patch
Patch23:	bz1091101-nfs-rquotad-port-option-fix.patch
Patch24:	bz1116166-galera-agent.patch
Patch25:	bz1116166-galera-updates.patch
Patch26:	rabbitmq-cluster.patch
Patch27:    Fix-rmq_join_list-to-only-return-online-nodes.patch

Obsoletes:	heartbeat-resources <= %{version}
Provides:	heartbeat-resources = %{version}

## Setup/build bits
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# Build dependencies
BuildRequires: automake autoconf pkgconfig
BuildRequires: perl python-devel
BuildRequires: libxslt glib2-devel
BuildRequires: which

%if 0%{?fedora} || 0%{?centos_version} || 0%{?rhel}
#BuildRequires: cluster-glue-libs-devel
BuildRequires: docbook-style-xsl docbook-dtds
%if 0%{?rhel} == 0
BuildRequires: libnet-devel
%endif
%endif

## Runtime deps
## These apply to rgmanager agents only to guarantee agents
## are functional
%if %{with rgmanager}
# system tools shared by several agents
Requires: /bin/bash /bin/grep /bin/sed /bin/gawk
Requires: /bin/ps /usr/bin/pkill /bin/hostname
Requires: /sbin/fuser
Requires: /sbin/findfs /bin/mount

# fs.sh
Requires: /sbin/quotaon /sbin/quotacheck
Requires: /sbin/fsck
Requires: /usr/sbin/fsck.ext2 /usr/sbin/fsck.ext3 /usr/sbin/fsck.ext4
Requires: /usr/sbin/fsck.xfs

# ip.sh
Requires: /sbin/ip /usr/sbin/ethtool
Requires: /sbin/rdisc /usr/sbin/arping /bin/ping /bin/ping6

# lvm.sh
Requires: /usr/sbin/lvm

# netfs.sh
Requires: /sbin/mount.nfs /sbin/mount.nfs4 /usr/sbin/mount.cifs
Requires: /usr/sbin/rpc.nfsd /sbin/rpc.statd /usr/sbin/rpc.mountd
%endif

## Runtime dependencies required to guarantee heartbeat agents
## are functional
%if %{with linuxha}
# tools needed for Filesystem resource
Requires: psmisc
# Tools needed for clvm resource. 
Requires: procps-ng
%endif

%description
A set of scripts to interface with several services to operate in a
High Availability environment for both Pacemaker and rgmanager
service managers.

%package sap
License:      GPLv2+
Summary:      SAP cluster resource agents and connector script
%if 0%{?fedora} || 0%{?centos_version} || 0%{?rhel}
Group:		System Environment/Base
%else
Group:		Productivity/Clustering/HA
%endif
Requires:     %{name} = %{version}-%{release}
Requires:	perl

%description sap
The SAP resource agents and connector script interface with 
Pacemaker to allow SAP instances to be managed in a cluster
environment.

%prep
%if 0%{?suse_version} == 0 && 0%{?fedora} == 0 && 0%{?centos_version} == 0 && 0%{?rhel} == 0
%{error:Unable to determine the distribution/version. This is generally caused by missing /etc/rpm/macros.dist. Please install the correct build packages or define the required macros manually.}
exit 1
%endif
%setup -q -n %{upstream_prefix}-%{upstream_version}
%setup -a 1 -n %{upstream_prefix}-%{upstream_version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1 -b .bz917681.1
%patch13 -p1 -b .bz917681.1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1

%build
if [ ! -f configure ]; then
	./autogen.sh
fi

chmod 755 heartbeat/galera
chmod 755 heartbeat/mysql-common.sh
chmod 755 heartbeat/nfsnotify
chmod 755 heartbeat/rabbitmq-cluster

%if 0%{?fedora} >= 11 || 0%{?centos_version} > 5 || 0%{?rhel} > 5
CFLAGS="$(echo '%{optflags}')"
%global conf_opt_fatal "--enable-fatal-warnings=no"
%else
CFLAGS="${CFLAGS} ${RPM_OPT_FLAGS}"
%global conf_opt_fatal "--enable-fatal-warnings=yes"
%endif

%if %{with rgmanager}
%global rasset rgmanager
%endif
%if %{with linuxha}
%global rasset linux-ha
%endif
%if %{with rgmanager} && %{with linuxha}
%global rasset all
%endif

export CFLAGS

chmod 755 heartbeat/clvm

%configure \
	%{conf_opt_fatal} \
	--with-pkg-name=%{name} \
	--with-ras-set=%{rasset} \
	--with-ocft-cases=fedora

%if %{defined jobs}
JFLAGS="$(echo '-j%{jobs}')"
%else
JFLAGS="$(echo '%{_smp_mflags}')"
%endif

make $JFLAGS

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

test -d %{buildroot}/usr/sbin || mkdir %{buildroot}/usr/sbin
mv %{sap_script_prefix}-%{sap_hash}/sap_redhat_cluster_connector %{buildroot}/usr/sbin/sap_redhat_cluster_connector

## tree fixup
# remove docs (there is only one and they should come from doc sections in files)
rm -rf %{buildroot}/usr/share/doc/resource-agents

##
# Create symbolic link between IPAddr and IPAddr2
##
rm -f %{buildroot}/usr/lib/ocf/resource.d/heartbeat/IPaddr
ln -s /usr/lib/ocf/resource.d/heartbeat/IPaddr2 %{buildroot}/usr/lib/ocf/resource.d/heartbeat/IPaddr

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING COPYING.GPLv3 ChangeLog
%if %{with linuxha}
%doc doc/README.webapps
%doc %{_datadir}/%{name}/ra-api-1.dtd
%endif

%if %{with rgmanager}
%{_datadir}/cluster
%{_sbindir}/rhev-check.sh
%endif

%if %{with linuxha}
%dir /usr/lib/ocf
%dir /usr/lib/ocf/resource.d
%dir /usr/lib/ocf/lib

/usr/lib/ocf/lib/heartbeat

/usr/lib/ocf/resource.d/heartbeat
%if %{with rgmanager}
/usr/lib/ocf/resource.d/redhat
%endif

%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/ocft
%{_datadir}/%{name}/ocft/configs
%{_datadir}/%{name}/ocft/caselib
%{_datadir}/%{name}/ocft/README
%{_datadir}/%{name}/ocft/README.zh_CN

%{_sbindir}/ocft

%{_includedir}/heartbeat

%dir %attr (1755, root, root)	%{_var}/run/resource-agents

%{_mandir}/man7/*.7*

###
# Supported, but in another sub package
###
%exclude %{_sbindir}/sap_redhat_cluster_connector
%exclude /usr/lib/ocf/resource.d/heartbeat/SAP*
%exclude /usr/lib/ocf/lib/heartbeat/sap*
%exclude %{_mandir}/man7/*SAP*

###
# Unsupported
###
%exclude /usr/lib/ocf/resource.d/heartbeat/AoEtarget
%exclude /usr/lib/ocf/resource.d/heartbeat/AudibleAlarm
%exclude /usr/lib/ocf/resource.d/heartbeat/ClusterMon
%exclude /usr/lib/ocf/resource.d/heartbeat/EvmsSCC
%exclude /usr/lib/ocf/resource.d/heartbeat/Evmsd
%exclude /usr/lib/ocf/resource.d/heartbeat/ICP
%exclude /usr/lib/ocf/resource.d/heartbeat/LinuxSCSI
%exclude /usr/lib/ocf/resource.d/heartbeat/ManageRAID
%exclude /usr/lib/ocf/resource.d/heartbeat/ManageVE
%exclude /usr/lib/ocf/resource.d/heartbeat/Pure-FTPd
%exclude /usr/lib/ocf/resource.d/heartbeat/Raid1
%exclude /usr/lib/ocf/resource.d/heartbeat/ServeRAID
%exclude /usr/lib/ocf/resource.d/heartbeat/SphinxSearchDaemon
%exclude /usr/lib/ocf/resource.d/heartbeat/Stateful
%exclude /usr/lib/ocf/resource.d/heartbeat/SysInfo
%exclude /usr/lib/ocf/resource.d/heartbeat/VIPArip
%exclude /usr/lib/ocf/resource.d/heartbeat/WAS
%exclude /usr/lib/ocf/resource.d/heartbeat/WAS6
%exclude /usr/lib/ocf/resource.d/heartbeat/WinPopup
%exclude /usr/lib/ocf/resource.d/heartbeat/Xen
%exclude /usr/lib/ocf/resource.d/heartbeat/anything
%exclude /usr/lib/ocf/resource.d/heartbeat/asterisk
%exclude /usr/lib/ocf/resource.d/heartbeat/db2
%exclude /usr/lib/ocf/resource.d/heartbeat/eDir88
%exclude /usr/lib/ocf/resource.d/heartbeat/fio
%exclude /usr/lib/ocf/resource.d/heartbeat/iSCSILogicalUnit
%exclude /usr/lib/ocf/resource.d/heartbeat/iSCSITarget
%exclude /usr/lib/ocf/resource.d/heartbeat/ids
%exclude /usr/lib/ocf/resource.d/heartbeat/iscsi
%exclude /usr/lib/ocf/resource.d/heartbeat/jboss
%exclude /usr/lib/ocf/resource.d/heartbeat/ldirectord
%exclude /usr/lib/ocf/resource.d/heartbeat/lxc
%exclude /usr/lib/ocf/resource.d/heartbeat/oracle
%exclude /usr/lib/ocf/resource.d/heartbeat/oralsnr
%exclude /usr/lib/ocf/resource.d/heartbeat/pingd
%exclude /usr/lib/ocf/resource.d/heartbeat/portblock
%exclude /usr/lib/ocf/resource.d/heartbeat/pound
%exclude /usr/lib/ocf/resource.d/heartbeat/proftpd
%exclude /usr/lib/ocf/resource.d/heartbeat/scsi2reservation
%exclude /usr/lib/ocf/resource.d/heartbeat/sfex
%exclude /usr/lib/ocf/resource.d/heartbeat/syslog-ng
%exclude /usr/lib/ocf/resource.d/heartbeat/varnish
%exclude /usr/lib/ocf/resource.d/heartbeat/vmware
%exclude /usr/lib/ocf/resource.d/heartbeat/zabbixserver
%exclude /usr/lib/ocf/resource.d/heartbeat/mysql-proxy
%exclude /usr/lib/ocf/resource.d/heartbeat/nginx
%exclude /usr/lib/ocf/resource.d/heartbeat/rsyslog
%exclude %{_mandir}/man7/ocf_heartbeat_AoEtarget.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_AudibleAlarm.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_ClusterMon.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_EvmsSCC.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_Evmsd.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_ICP.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_IPaddr.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_LinuxSCSI.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_ManageRAID.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_ManageVE.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_Pure-FTPd.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_Raid1.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_ServeRAID.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_SphinxSearchDaemon.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_Stateful.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_SysInfo.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_VIPArip.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_WAS.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_WAS6.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_WinPopup.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_Xen.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_anything.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_asterisk.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_db2.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_eDir88.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_fio.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_iSCSILogicalUnit.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_iSCSITarget.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_ids.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_iscsi.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_jboss.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_lxc.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_oracle.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_oralsnr.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_pingd.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_portblock.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_pound.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_proftpd.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_scsi2reservation.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_sfex.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_syslog-ng.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_varnish.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_vmware.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_zabbixserver.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_mysql-proxy.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_nginx.7.gz
%exclude %{_mandir}/man7/ocf_heartbeat_rsyslog.7.gz

###
# Other excluded files.
###
# This tool has to be updated for the new pacemaker lrmd.
%exclude %{_sbindir}/ocf-tester
%exclude %{_mandir}/man8/ocf-tester.8*
# ldirectord is not supported
%exclude /etc/ha.d/resource.d/ldirectord
%exclude /etc/init.d/ldirectord
%exclude /etc/logrotate.d/ldirectord
%exclude /usr/sbin/ldirectord
%exclude %{_mandir}/man8/ldirectord.8.gz

# For compatability with pre-existing agents
%dir %{_sysconfdir}/ha.d
%{_sysconfdir}/ha.d/shellfuncs

%{_libexecdir}/heartbeat
%endif

%if %{with rgmanager}
%post -n resource-agents
ccs_update_schema > /dev/null 2>&1 ||:
%endif

%files sap
%defattr(-,root,root)
%{_sbindir}/sap_redhat_cluster_connector
/usr/lib/ocf/resource.d/heartbeat/SAP*
/usr/lib/ocf/lib/heartbeat/sap*
%{_mandir}/man7/*SAP*

%changelog

* Tue May 05 2015 Zhao Chao <chao.zhao@eayun.com> - 3.9.5-26.8.eayunstack.1.0
- add Fix-rmq_join_list-to-only-return-online-nodes.patch

* Mon Jan 26 2015 David Vossel <dvossel@redhat.com> - 3.9.5-26.7
- Support for rabbitmq-cluster resource-agent

  Resolves: rhbz#1185753

* Thu Oct 30 2014 David Vossel <dvossel@redhat.com> - 3.9.5-26.6
- Support for galera resource-agent

  Resolves: rhbz#1116166

* Thu Oct 30 2014 David Vossel <dvossel@redhat.com> - 3.9.5-26.5
- Support NFSv4 Active/Passive use case.

  Resolves: rhbz#1158901

* Tue Mar 18 2014 David Vossel <dvossel@redhat.com> - 3.9.5-26
- Handle monitor qemu based VirtualDomain resources without
  requiring libvirtd even if configuration file does not
  contain an 'emulator' value pointing to the emulator binary.

  Resolves: rhbz#1060367

* Fri Feb 14 2014 David Vossel <dvossel@redhat.com> - 3.9.5-25
- Rename clvmd agent to clvm to avoid problems associated
  with having a resource-agent named the same exact name
  as the binary the agent manages.

  Resolves: rhbz#1064512

* Fri Feb 14 2014 David Vossel <dvossel@redhat.com> - 3.9.5-24
- Addition of the clvmd resource-agent
- Support monitoring qemu based VirtualDomain resources without
  requiring libvirtd to be running.

  Resolves: rhbz#1064512
  Resolves: rhbz#1060367

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.9.5-23
- Mass rebuild 2014-01-24

* Mon Jan 20 2014 David Vossel <dvossel@redhat.com> - 3.9.5-22
- Fixes VirtualDomain config parse error.

  Resolves: rhbz#1029061

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.9.5-21
- Mass rebuild 2013-12-27

* Tue Nov 26 2013 David Vossel <dvossel@redhat.com> - 3.9.5-20
- tomcat agent updates for pacemaker support
- slapd agent updates for pacemaker support
- Fixes missing etab file required for nfsserver

  Resolves: rhbz#1033016
  Resolves: rhbz#917681

* Wed Nov 20 2013 David Vossel <dvossel@redhat.com> - 3.9.5-19
- Add back the Delay agent.

  Resolves: rhbz#917681

* Thu Nov 07 2013 David Vossel <dvossel@redhat.com> - 3.9.5-18
- Remove support for (nginx, mysql-proxy, rsyslog). nginx and
  mysql-proxy are not a supported projects. Rsyslog is not an
  agent we will be supporting in an HA environment.

  Resolves: rhbz#917681

* Wed Nov 06 2013 David Vossel <dvossel@redhat.com> - 3.9.5-17
- Split send_ua utility out of IPv6addr.c source so it can be
  re-used in IPaddr2 without requiring cluster-glue.
- Fixes issue with pgsql and SAPInstance not setting transient
  attributes correctly when local corosync node name is not
  equal to 'uname -n'
- High: ocft: Fedora supported test cases

  Resolves: rhbz#917681

* Mon Oct 07 2013 David Vossel <dvossel@redhat.com> - 3.9.5-16
- Fixes issue with mysql agent not being able to set transient
  attributes on local node correctly.
- Fixes bash syntax error in VirtualDomain during 'stop'
- Fixes VirtualDomain default hypervisor usage.
- Fixes VirtualDomain 'start' of pre-defined domain

  Resolves: rhbz#917681
  Resolves: rhbz#1014641
  Resolves: rhbz#1016140

* Thu Sep 26 2013 David Vossel <dvossel@redhat.com> - 3.9.5-15
- Update VirtualDomain heartbeat agent for heartbeat merger.
- Includes upstream fixes for pacemaker_remote lxc test case.

  Resolves: rhbz#917681

* Thu Sep 12 2013 David Vossel <dvossel@redhat.com> - 3.9.5-14
- Add ability for apache agent to perform simple monitoring
  of server request/response without requiring server-status
  to be enabled.
- Fixes invalid return statement in LVM agent.
- Oracle TNS_ADMIN option 

  Resolves: rhbz#917806
  Resolves: rhbz#917681
  Resolves: rhbz#799065

* Mon Sep 9 2013 David Vossel <dvossel@redhat.com> - 3.9.5-13
- Use correct default config for apache
  Resolves: rhbz#1005924

* Tue Jul 30 2013 David Vossel <dvossel@redhat.com> - 3.9.5-12
- Symbolic links do not have file permissions.

* Tue Jul 30 2013 David Vossel <dvossel@redhat.com> - 3.9.5-11
- Fixes file permissions problem detected in rpmdiff test

* Tue Jul 30 2013 David Vossel <dvossel@redhat.com> - 3.9.5-10
- Removes ldirectord package
- Puts sap agents and connector script in subpackage
- exclude unsupported packages
- symlink ipaddr to ipaddr2 so only a single agent is supported

* Mon Jul 29 2013 David Vossel <dvossel@redhat.com> - 3.9.5-9
- Fixes more multi-lib problems.

* Mon Jul 29 2013 David Vossel <dvossel@redhat.com> - 3.9.5-8
- Add runtime dependencies section for Heartbeat agents.
- Fix multi-lib inconsistencies found during rpm diff testing.
- Add dist field back to rpm release name.

* Tue Jul 16 2013 David Vossel <dvossel@redhat.com> - 3.9.5-7
- Detect duplicate resources with the same volgrpname
  name when using exclusive activation with tags

  Resolves: # rhbz984054

* Tue Jun 18 2013 David Vossel <dvossel@redhat.com> - 3.9.5-6
- Restores rsctmp directory to upstream default.

* Tue Jun 18 2013 David Vossel <dvossel@redhat.com> - 3.9.5-5
- Merges redhat provider into heartbeat provider. Remove
  rgmanager's redhat provider.

  Resolves: rhbz#917681
  Resolves: rhbz#928890
  Resolves: rhbz#952716
  Resolves: rhbz#960555

* Tue Mar 12 2013 David Vossel <dvossel@redhat.com> - 3.9.5-4
- Fixes build system error with conditional logic involving
  IPv6addr.

* Mon Mar 11 2013 David Vossel <dvossel@redhat.com> - 3.9.5-3
- Fixes build dependency for pod2man when building against
  rhel-7.

* Mon Mar 11 2013 David Vossel <dvossel@redhat.com> - 3.9.5-2
- Resolves rhbz#915050

* Mon Mar 11 2013 David Vossel <dvossel@redhat.com> - 3.9.5-1
- New upstream release.

* Fri Nov 09 2012 Chris Feist <cfeist@redhat.com> - 3.9.2-5
- Fixed upstream tarball location

* Fri Nov 09 2012 Chris Feist <cfeist@redhat.com> - 3.9.2-4
- Removed version after dist tag
- Resolves: rhbz#875250

* Mon Oct 29 2012 Chris Feist <cfeist@redhat.com> - 3.9.2-3.8
- Remove cluster-glue-libs-devel
- Disable IPv6addr & sfex to fix deps on libplumgpl & libplum (due to
  disappearance of cluster-glue in F18)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.2-3.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 05 2012 Chris Feist <cfeist@redhat.com> - 3.9.2-3.4
- Fix location of lvm (change from /sbin to /usr/sbin)

* Tue Apr 04 2012 Jon Ciesla <limburgher@gmail.com> - 3.9.2-3.3
- Rebuilt to fix rawhide dependency issues (caused by move of fsck from
  /sbin to /usr/sbin).

* Fri Mar 30 2012 Jon Ciesla <limburgher@gmail.com> - 3.9.2-3.1
- libnet rebuild.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.2-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul  8 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.9.2-2
- add post call to resource-agents to integrate with cluster 3.1.4

* Thu Jun 30 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.9.2-1
- new upstream release
- fix 2 regressions from 3.9.1

* Mon Jun 20 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.9.1-1
- new upstream release
- import spec file from upstream

* Tue Mar  1 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.1.1-1
- new upstream release 3.1.1 and 1.0.4

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  2 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.1.0-1
- new upstream release
- spec file update:
  Update upstream URL
  Update source URL
  use standard configure macro
  use standard make invokation

* Thu Oct  7 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.17-1
- new upstream release
  Resolves: rhbz#632595, rhbz#633856, rhbz#632385, rhbz#628013
  Resolves: rhbz#621313, rhbz#595383, rhbz#580492, rhbz#605733
  Resolves: rhbz#636243, rhbz#591003, rhbz#637913, rhbz#634718
  Resolves: rhbz#617247, rhbz#617247, rhbz#617234, rhbz#631943
  Resolves: rhbz#639018

* Thu Oct  7 2010 Andrew Beekhof <andrew@beekhof.net> - 3.0.16-2
- new upstream release of the Pacemaker agents: 71b1377f907c

* Thu Sep  2 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.16-1
- new upstream release
  Resolves: rhbz#619096, rhbz#614046, rhbz#620679, rhbz#619680
  Resolves: rhbz#621562, rhbz#621694, rhbz#608887, rhbz#622844
  Resolves: rhbz#623810, rhbz#617306, rhbz#623816, rhbz#624691
  Resolves: rhbz#622576

* Thu Jul 29 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.14-1
- new upstream release
  Resolves: rhbz#553383, rhbz#557563, rhbz#578625, rhbz#591003
  Resolves: rhbz#593721, rhbz#593726, rhbz#595455, rhbz#595547
  Resolves: rhbz#596918, rhbz#601315, rhbz#604298, rhbz#606368
  Resolves: rhbz#606470, rhbz#606480, rhbz#606754, rhbz#606989
  Resolves: rhbz#607321, rhbz#608154, rhbz#608887, rhbz#609181
  Resolves: rhbz#609866, rhbz#609978, rhbz#612097, rhbz#612110
  Resolves: rhbz#612165, rhbz#612941, rhbz#614127, rhbz#614356
  Resolves: rhbz#614421, rhbz#614457, rhbz#614961, rhbz#615202
  Resolves: rhbz#615203, rhbz#615255, rhbz#617163, rhbz#617566
  Resolves: rhbz#618534, rhbz#618703, rhbz#618806, rhbz#618814

* Mon Jun  7 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.13-1
- new upstream release
  Resolves: rhbz#592103, rhbz#593108, rhbz#578617, rhbz#594626
  Resolves: rhbz#594511, rhbz#596046, rhbz#594111, rhbz#597002
  Resolves: rhbz#599643

* Tue May 18 2010 Andrew Beekhof <andrew@beekhof.net> - 3.0.12-2
- libnet is not available on RHEL
- Do not package ldirectord on RHEL
  Resolves: rhbz#577264

* Mon May 10 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.12-1
- new upstream release
  Resolves: rhbz#585217, rhbz#586100, rhbz#581533, rhbz#582753
  Resolves: rhbz#582754, rhbz#585083, rhbz#587079, rhbz#588890
  Resolves: rhbz#588925, rhbz#583789, rhbz#589131, rhbz#588010
  Resolves: rhbz#576871, rhbz#576871, rhbz#590000, rhbz#589823

* Mon May 10 2010 Andrew Beekhof <andrew@beekhof.net> - 3.0.12-1
- New pacemaker agents upstream release: a7c0f35916bf
  + High: pgsql: properly implement pghost parameter
  + High: RA: mysql: fix syntax error
  + High: SAPInstance RA: do not rely on op target rc when monitoring clones (lf#2371)
  + High: set the HA_RSCTMP directory to /var/run/resource-agents (lf#2378)
  + Medium: IPaddr/IPaddr2: add a description of the assumption in meta-data
  + Medium: IPaddr: return the correct code if interface delete failed
  + Medium: nfsserver: rpc.statd as the notify cmd does not work with -v (thanks to Carl Lewis)
  + Medium: oracle: reduce output from sqlplus to the last line for queries (bnc#567815)
  + Medium: pgsql: implement "config" parameter
  + Medium: RA: iSCSITarget: follow changed IET access policy

* Wed Apr 21 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.11-1
- new upstream release
  Resolves: rhbz#583945, rhbz#581047, rhbz#576330, rhbz#583017
  Resolves: rhbz#583019, rhbz#583948, rhbz#584003, rhbz#582017
  Resolves: rhbz#555901, rhbz#582754, rhbz#582573, rhbz#581533
- Switch to file based Requires.
  Also address several other problems related to missing runtime
  components in different agents.
  With the current Requires: set, we guarantee all basic functionalities
  out of the box for lvm/fs/clusterfs/netfs/networking.
  Resolves: rhbz#570008

* Sat Apr 17 2010 Andrew Beekhof <andrew@beekhof.net> - 3.0.10-2
- New pacemaker agents upstream release
  + High: RA: vmware: fix set_environment() invocation (LF 2342)
  + High: RA: vmware: update to version 0.2
  + Medium: Filesystem: prefer /proc/mounts to /etc/mtab for non-bind mounts (lf#2388)
  + Medium: IPaddr2: don't bring the interface down on stop (thanks to Lars Ellenberg)
  + Medium: IPsrcaddr: modify the interface route (lf#2367)
  + Medium: ldirectord: Allow multiple email addresses (LF 2168)
  + Medium: ldirectord: fix setting defaults for configfile and ldirectord (lf#2328)
  + Medium: meta-data: improve timeouts in most resource agents
  + Medium: nfsserver: use default values (lf#2321)
  + Medium: ocf-shellfuncs: don't log but print to stderr if connected to a terminal
  + Medium: ocf-shellfuncs: don't output to stderr if using syslog
  + Medium: oracle/oralsnr: improve exit codes if the environment isn't valid
  + Medium: RA: iSCSILogicalUnit: fix monitor for STGT
  + Medium: RA: make sure that OCF_RESKEY_CRM_meta_interval is always defined (LF 2284)
  + Medium: RA: ManageRAID: require bash
  + Medium: RA: ManageRAID: require bash
  + Medium: RA: VirtualDomain: bail out early if config file can't be read during probe (Novell 593988)
  + Medium: RA: VirtualDomain: fix incorrect use of __OCF_ACTION
  + Medium: RA: VirtualDomain: improve error messages
  + Medium: RA: VirtualDomain: spin on define until we definitely have a domain name
  + Medium: Route: add route table parameter (lf#2335)
  + Medium: sfex: don't use pid file (lf#2363,bnc#585416)
  + Medium: sfex: exit with success on stop if sfex has never been started (bnc#585416)

* Fri Apr  9 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.10-1
- New rgmanager resource agents upstream release
  Resolves: rhbz#519491, rhbz#570525, rhbz#571806, rhbz#574027
  Resolves: rhbz#574215, rhbz#574886, rhbz#576322, rhbz#576335
  Resolves: rhbz#575103, rhbz#577856, rhbz#577874, rhbz#578249
  Resolves: rhbz#578625, rhbz#578626, rhbz#578628, rhbz#578626
  Resolves: rhbz#579621, rhbz#579623, rhbz#579625, rhbz#579626
  Resolves: rhbz#579059

* Wed Mar 24 2010 Andrew Beekhof <andrew@beekhof.net> - 3.0.9-2
- Resolves: rhbz#572993 - Patched build process to correctly generate ldirectord man page
- Resolves: rhbz#574732 - Add libnet-devel as a dependancy to ensure IPaddrv6 is built

* Mon Mar  1 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.9-1
- New rgmanager resource agents upstream release
  Resolves: rhbz#455300, rhbz#568446, rhbz#561862, rhbz#536902
  Resolves: rhbz#512171, rhbz#519491

* Mon Feb 22 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.8-1
- New rgmanager resource agents upstream release
  Resolves: rhbz#548133, rhbz#565907, rhbz#545602, rhbz#555901
  Resolves: rhbz#564471, rhbz#515717, rhbz#557128, rhbz#536157
  Resolves: rhbz#455300, rhbz#561416, rhbz#562237, rhbz#537201
  Resolves: rhbz#536962, rhbz#553383, rhbz#556961, rhbz#555363
  Resolves: rhbz#557128, rhbz#455300, rhbz#557167, rhbz#459630
  Resolves: rhbz#532808, rhbz#556603, rhbz#554968, rhbz#555047
  Resolves: rhbz#554968, rhbz#555047
- spec file update:
  * update spec file copyright date
  * use bz2 tarball

* Fri Jan 15 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.7-2
- Add python as BuildRequires

* Mon Jan 11 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.7-1
- New rgmanager resource agents upstream release
  Resolves: rhbz#526286, rhbz#533461

* Mon Jan 11 2010 Andrew Beekhof <andrew@beekhof.net> - 3.0.6-2
- Update Pacameker agents to upstream version: c76b4a6eb576
  + High: RA: VirtualDomain: fix forceful stop (LF 2283)
  + High: apache: monitor operation of depth 10 for web applications (LF 2234)
  + Medium: IPaddr2: CLUSTERIP/iptables rule not always inserted on failed monitor (LF 2281)
  + Medium: RA: Route: improve validate (LF 2232)
  + Medium: mark obsolete RAs as deprecated (LF 2244)
  + Medium: mysql: escalate stop to KILL if regular shutdown doesn't work

* Mon Dec 7 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.6-1
- New rgmanager resource agents upstream release
- spec file update:
  * use global instead of define
  * use new Source0 url
  * use %name macro more aggressively

* Mon Dec 7 2009 Andrew Beekhof <andrew@beekhof.net> - 3.0.5-2
- Update Pacameker agents to upstream version: bc00c0b065d9
  + High: RA: introduce OCF_FUNCTIONS_DIR, allow it to be overridden (LF2239)
  + High: doc: add man pages for all RAs (LF2237)
  + High: syslog-ng: new RA
  + High: vmware: make meta-data work and several cleanups (LF 2212)
  + Medium: .ocf-shellfuncs: add ocf_is_probe function
  + Medium: Dev: make RAs executable (LF2239)
  + Medium: IPv6addr: ifdef out the ip offset hack for libnet v1.1.4 (LF 2034)
  + Medium: add mercurial repository version information to .ocf-shellfuncs
  + Medium: build: add perl-MailTools runtime dependency to ldirectord package (LF 1469)
  + Medium: iSCSITarget, iSCSILogicalUnit: support LIO
  + Medium: nfsserver: use check_binary properly in validate (LF 2211)
  + Medium: nfsserver: validate should not check if nfs_shared_infodir exists (thanks to eelco@procolix.com) (LF 2219)
  + Medium: oracle/oralsnr: export variables properly
  + Medium: pgsql: remove the previous backup_label if it exists
  + Medium: postfix: fix double stop (thanks to Dinh N. Quoc)
  + RA: LVM: Make monitor operation quiet in logs (bnc#546353)
  + RA: Xen: Remove instance_attribute "allow_migrate" (bnc#539968)
  + ldirectord: OCF agent: overhaul

* Fri Nov 20 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.5-1
- New rgmanager resource agents upstream release
- Allow pacemaker to use rgmanager resource agents

* Wed Oct 28 2009 Andrew Beekhof <andrew@beekhof.net> - 3.0.4-2
- Update Pacameker agents to upstream version: e2338892f59f
  + High: send_arp - turn on unsolicited mode for compatibilty with the libnet version's exit codes
  + High: Trap sigterm for compatibility with the libnet version of send_arp
  + Medium: Bug - lf#2147: IPaddr2: behave if the interface is down
  + Medium: IPv6addr: recognize network masks properly
  + Medium: RA: VirtualDomain: avoid needlessly invoking "virsh define"

* Wed Oct 21 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.4-1
- New rgmanager resource agents upstream release

* Mon Oct 12 2009 Andrew Beekhof <andrew@beekhof.net> - 3.0.3-3
- Update Pacameker agents to upstream version: 099c0e5d80db
  + Add the ha_parameter function back into .ocf-shellfuncs.
  + Bug bnc#534803 - Provide a default for MAILCMD
  + Fix use of undefined macro @HA_NOARCHDATAHBDIR@
  + High (LF 2138): IPsrcaddr: replace 0/0 with proper ip prefix (thanks to Michael Ricordeau and Michael Schwartzkopff)
  + Import shellfuncs from heartbeat as badly written RAs use it
  + Medium (LF 2173): nfsserver: exit properly in nfsserver_validate
  + Medium: RA: Filesystem: implement monitor operation
  + Medium: RA: VirtualDomain: loop on status if libvirtd is unreachable
  + Medium: RA: VirtualDomain: loop on status if libvirtd is unreachable (addendum)
  + Medium: RA: iSCSILogicalUnit: use a 16-byte default SCSI ID
  + Medium: RA: iSCSITarget: be more persistent deleting targets on stop
  + Medium: RA: portblock: add per-IP filtering capability
  + Medium: mysql-proxy: log_level and keepalive parameters
  + Medium: oracle: drop spurious output from sqlplus
  + RA: Filesystem: allow configuring smbfs mounts as clones

* Wed Sep 23 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.3-1
- New rgmanager resource agents upstream release

* Thu Aug 20 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.1-1
- New rgmanager resource agents upstream release

* Tue Aug 18 2009 Andrew Beekhof <andrew@beekhof.net> - 3.0.0-16
- Create an ldirectord package
- Update Pacameker agents to upstream version: 2198dc90bec4
  + Build: Import ldirectord.
  + Ensure HA_VARRUNDIR has a value to substitute
  + High: Add findif tool (mandatory for IPaddr/IPaddr2)
  + High: IPv6addr: new nic and cidr_netmask parameters
  + High: postfix: new resource agent
  + Include license information
  + Low (LF 2159): Squid: make the regexp match more precisely output of netstat
  + Low: configure: Fix package name.
  + Low: ldirectord: add dependency on $remote_fs.
  + Low: ldirectord: add mandatory required header to init script.
  + Medium (LF 2165): IPaddr2: remove all colons from the mac address before passing it to send_arp
  + Medium: VirtualDomain: destroy domain shortly before timeout expiry
  + Medium: shellfuncs: Make the mktemp wrappers work.
  + Remove references to Echo function
  + Remove references to heartbeat shellfuncs.
  + Remove useless path lookups
  + findif: actually include the right header. Simplify configure.
  + ldirectord: Remove superfluous configure artifact.
  + ocf-tester: Fix package reference and path to DTD.

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 3.0.0-15
- Use bzipped upstream hg tarball.

* Wed Jul 29 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-14
- Merge Pacemaker cluster resource agents:
  * Add Source1.
  * Drop noarch. We have real binaries now.
  * Update BuildRequires.
  * Update all relevant prep/build/install/files/description sections.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul  8 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-12
- spec file updates:
  * Update copyright header
  * final release.. undefine alphatag

* Thu Jul  2 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-11.rc4
- New upstream release.

* Sat Jun 20 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-10.rc3
- New upstream release.

* Wed Jun 10 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-9.rc2
- New upstream release + git94df30ca63e49afb1e8aeede65df8a3e5bcd0970

* Tue Mar 24 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-8.rc1
- New upstream release.
- Update BuildRoot usage to preferred versions/names

* Mon Mar  9 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-7.beta1
- New upstream release.

* Fri Mar  6 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-6.alpha7
- New upstream release.

* Tue Mar  3 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-5.alpha6
- New upstream release.

* Tue Feb 24 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-4.alpha5
- Drop Conflicts with rgmanager.

* Mon Feb 23 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-3.alpha5
- New upstream release.

* Thu Feb 19 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-2.alpha4
- Add comments on how to build this package.

* Thu Feb  5 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-1.alpha4
- New upstream release.
- Fix datadir/cluster directory ownership.

* Tue Jan 27 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.0.0-1.alpha3
  - Initial packaging
