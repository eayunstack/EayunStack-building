srpm_repo = http://192.168.2.65:11080/pulp/repos/rdo/openstack-juno/epel-7
base_srpm = openstack-neutron-2014.2-11.el7.centos.src.rpm
spec_file = openstack-neutron.spec

sources:
	mv $(spec_file) $(spec_file).new
	wget "$(srpm_repo)/$(base_srpm)" && \
	rpm2cpio $(base_srpm) | cpio -idmv && \
	rm -f $(spec_file) && \
	mv $(spec_file).new $(spec_file) && \
	for patch in out-of-tree-patches/*.patch; do \
			if [ -f $$patch ]; then \
					patch -p1 < $$patch; \
			fi; \
	done && \
	rm -f $(base_srpm)
