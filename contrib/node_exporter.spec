%define debug_package %{nil}

Name:		node-exporter
Version:	1.2.2
Release:	1%{?dist}
Summary:	Prometheus exporter for machine metrics, written in Go with pluggable metric collectors.
Group:		System Environment/Daemons
License:	See the LICENSE file at github.
URL:		https://github.com/prometheus/node_exporter
Source0:        https://github.com/prometheus/node_exporter/releases/download/v%{version}/node_exporter-%{version}.linux-amd64.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Requires(pre):  /usr/sbin/useradd systemd
AutoReqProv:	No

%description

Prometheus exporter for machine metrics, written in Go with pluggable metric collectors.

%prep
%setup -q -n node_exporter-%{version}.linux-amd64

%build
echo

%install
mkdir -vp $RPM_BUILD_ROOT/var/run/prometheus
mkdir -vp $RPM_BUILD_ROOT/var/lib/prometheus
mkdir -vp $RPM_BUILD_ROOT/usr/sbin
mkdir -vp $RPM_BUILD_ROOT/usr/lib/systemd/system
mkdir -vp $RPM_BUILD_ROOT/etc/sysconfig
mkdir -vp $RPM_BUILD_ROOT/opt/prometheus
install -m 755 node_exporter $RPM_BUILD_ROOT/usr/sbin/node_exporter
install -m 755 contrib/node_exporter.service $RPM_BUILD_ROOT/usr/lib/systemd/system/node_exporter.service
install -m 644 contrib/node_exporter.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/node_exporter

%clean

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -s /sbin/nologin \
    -d $RPM_BUILD_ROOT/var/lib/prometheus/ -c "Prometheus Daemons" prometheus
exit 0

%post
chgrp prometheus /var/run/prometheus
chmod 774 /var/run/prometheus
chown prometheus:prometheus /opt/prometheus
chmod 744 /opt/prometheus

%files
%defattr(-,root,root,-)
/usr/sbin/node_exporter
/usr/lib/systemd/system/node_exporter.service
%config(noreplace) /etc/sysconfig/node_exporter
/var/run/prometheus
/opt/prometheus

%changelog
* Wed Oct 20 2021 Darshan Pradhan <darshannnn@gmail.com> 1.2.2-1
- Bump version to 1.2.2
* Wed Apr 14 2021 Tsvetan Gerov <tsvetan@gerov.eu> 1.1.2-1
* Bump version to 1.1.2
* Mon Feb 15 2021 Tsvetan Gerov <tsvetan@gerov.eu> 1.1.1-1
- Bump version to 1.1.1
* Thu Nov 12 2020 Tsvetan Gerov <tsvetan@gerov.eu> 1.0.1-2
- Moved binary from bin to sbin
* Thu Nov 12 2020 Tsvetan Gerov <tsvetan@gerov.eu> 1.0.1-1
- Updated to 1.0.1
