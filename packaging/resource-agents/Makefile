srpm_repo = http://vault.centos.org/7.0.1406/updates/Source/SPackages
base_srpm = resource-agents-3.9.5-26.el7_0.7.src.rpm
spec_file = resource-agents.spec

sources:
	mv $(spec_file) $(spec_file).new
	wget "$(srpm_repo)/$(base_srpm)" && \
	rpm2cpio $(base_srpm) | cpio -idmv && \
	rm -f $(spec_file) && \
	mv $(spec_file).new $(spec_file) && \
	rm -f $(base_srpm)
