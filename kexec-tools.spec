#
# Conditional build:
%bcond_without	xen		# Xen support
%bcond_with	booke		# [PPC] build for BookE
%bcond_with	gamecube	# [PPC] build for GameCube

%ifarch x32
# Xen not (yet?) available
%undefine	with_xen
%endif
Summary:	Tool for starting new kernel without reboot
Summary(pl.UTF-8):	Narzędzie pozwalające załadować nowe jądro bez konieczności restartu
Name:		kexec-tools
Version:	2.0.28
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	https://www.kernel.org/pub/linux/utils/kernel/kexec/%{name}-%{version}.tar.xz
# Source0-md5:	c775dfc1c5f1397f390b5478845185be
Source1:	kexec.init
Source2:	kexec.sysconfig
# from http://patchwork.openembedded.org/patch/90971/raw/ (stripped to remaining syscall part)
Patch0:		%{name}-x32.patch
URL:		https://www.kernel.org/pub/linux/utils/kernel/kexec/
BuildRequires:	autoconf >= 2.50
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	tar >= 1:1.22
%{?with_xen:BuildRequires:	xen-devel >= 4.4}
BuildRequires:	xz
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts >= 0.4.0.9
ExclusiveArch:	%{ix86} %{x8664} x32 alpha %{arm} aarch64 cris ia64 m68k mips ppc ppc64 s390 s390x sh
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
kexec is a set of system calls that allows you to load another kernel
from the currently executing Linux kernel. The current implementation
has only been tested, and had the kinks worked out on x86, but the
generic code should work on any architecture.

%description -l pl.UTF-8
kexec to zestaw wywołań systemowych pozwalających załadować następne
jądro z poziomu aktualnie działającego jądra Linuksa. Aktualna
implementacja była testowana tylko na x86, ale ogólny kod powinien
działać na każdej architekturze.

%prep
%setup -q
%patch0 -p1

%build
%{__autoconf}
%configure \
	%{?with_booke:--with-booke} \
	%{?with_gamecube:--with-gamecube} \
	%{!?with_xen:--without-xen}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/kexec
cp -a %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/kexec

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add kexec
%service kexec restart

%preun
if [ "$1" = "0" ]; then
	%service -q kexec stop
	/sbin/chkconfig --del kexec
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS News TODO
%attr(754,root,root) /etc/rc.d/init.d/kexec
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/kexec
%attr(755,root,root) %{_sbindir}/kexec
%attr(755,root,root) %{_sbindir}/vmcore-dmesg
%{_mandir}/man8/kexec.8*
%{_mandir}/man8/vmcore-dmesg.8*
%ifarch %{ix86} x32
%dir %{_libdir}/kexec-tools
# what is this anyway, is it needed on other arches?
%attr(755,root,root) %{_libdir}/kexec-tools/kexec_test
%endif
