#!/bin/bash
#
# profiles = xccdf_org.ssgproject.content_profile_ospp

if which dnf ; then
	config_file="/etc/dnf/dnf.conf"
else
	config_file="/etc/yum.conf"
fi

if grep -q "^gpgcheck" "$config_file" ; then
	sed -i "s/^gpgcheck.*/gpgcheck=0/" "$config_file"
else
	echo "gpgcheck=0" >> "$config_file"
fi
