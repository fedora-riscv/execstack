Name:           execstack
Version:        0.5.0
Release:        8%{?dist}
Summary:        Utility to set/clear/query executable stack bit

%global commit 4c79120bcdbde0616f592458ccde7035e92ca3d8
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%define date 20131005

License: GPLv2+
# work around for missing upstream tarball with latest checkin
Source0: https://github.com/keszybz/prelink/archive/%{commit}.tar.gz#/prelink-%{shortcommit}.tar.gz

BuildRequires: elfutils-libelf-devel
BuildRequires: libselinux-devel, libselinux-utils
Requires: glibc >= 2.2.4-18, coreutils, findutils
Requires: util-linux, gawk, grep

Obsoletes:     prelink < 0.5.0-8

%description
This package is built from prelink sources but contains just the
execstack binary. It can be used manipulate ELF binaries to run
with or without executable stack.

%prep
%autosetup -n prelink-%{commit}

%build
sed -i -e '/^prelink_LDADD/s/$/ -lpthread/' src/Makefile.{am,in}
%configure
make %{?_smp_mflags} -C gelf
make %{?_smp_mflags} -C gelfx
make %{?_smp_mflags} -C gelfx32
make %{?_smp_mflags} -C src execstack

%check
cp src/execstack test
src/execstack -q test | grep '^-'
src/execstack -s test
src/execstack -q test | grep '^X'
src/execstack -c test
src/execstack -q test | grep '^-'

%install
install -D src/execstack %{buildroot}%{_bindir}/execstack
install -Dm0644 doc/execstack.8 %{buildroot}%{_mandir}/man8/execstack.8

%files
%license COPYING
%doc ChangeLog NEWS README TODO THANKS
%{_bindir}/execstack
%{_mandir}/man8/execstack.8.*

%changelog
* Mon Jul 27 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.5.0-8
- Kill off most of prelink package
