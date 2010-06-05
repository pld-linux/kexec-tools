Summary:	Tool for starting new kernel without reboot
Summary(pl.UTF-8):	Narzędzie pozwalające załadować nowe jądro bez konieczności restartu
Name:		kexec-tools
Version:	2.0.1
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	http://www.kernel.org/pub/linux/kernel/people/horms/kexec-tools/%{name}-%{version}.tar.bz2
# Source0-md5:	67c1a396fdf67b984dad939a59a01571
Source1:	kexec.init
Source2:	kexec.sysconfig
URL:		http://www.kernel.org/pub/linux/kernel/people/horms/kexec-tools/
BuildRequires:	autoconf
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts >= 0.4.0.9
ExclusiveArch:	%{ix86} %{x8664} alpha ia64 ppc ppc64
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
# fix for configure.ac
sed -i -e 's,]) fi,]); fi,' configure.ac

%build
%{__autoconf}
%configure
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
%attr(755,root,root) %{_sbindir}/kdump
%attr(755,root,root) %{_sbindir}/kexec
%ifnarch ppc ppc64
%dir %{_libdir}/kexec-tools
# what is this anyway, is it needed on other arches?
%attr(755,root,root) %{_libdir}/kexec-tools/kexec_test
%endif
