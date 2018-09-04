# platform = multi_platform_fedora
. /usr/share/scap-security-guide/remediation_functions

replace_or_append '/etc/dnf/dnf.conf' '^gpgcheck' '1' '@CCENUM@'
