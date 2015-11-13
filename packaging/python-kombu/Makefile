srpm_repo = http://192.168.2.65/testing/EayunStack/base_srpm
base_srpm = python-kombu-2.5.16-1.el7.src.rpm
spec_file = python-kombu.spec

sources:
	mv $(spec_file) $(spec_file).new
	wget "$(srpm_repo)/$(base_srpm)" && \
	rpm2cpio $(base_srpm) | cpio -idmv && \
	rm -f $(spec_file) && \
	mv $(spec_file).new $(spec_file) && \
	rm -f $(base_srpm)

