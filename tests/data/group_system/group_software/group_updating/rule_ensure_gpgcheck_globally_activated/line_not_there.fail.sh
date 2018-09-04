#!/bin/bash
#
# profiles = xccdf_org.ssgproject.content_profile_ospp

if which dnf ; then
	config_file="/etc/dnf/dnf.conf"
else
	config_file="/etc/yum.conf"
fi

sed -i "/^gpgcheck.*/d" "$config_file"
