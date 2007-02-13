Summary:	Tool for starting new kernel without reboot
Summary(pl.UTF-8):	Narzędzie pozwalające załadować nowe jądro bez konieczności restartu
Name:		kexec-tools
Version:	1.101
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	http://www.xmission.com/~ebiederm/files/kexec/%{name}-%{version}.tar.gz
# Source0-md5:	b4f7ffcc294d41a6a4c40d6e44b7734d
Source1:	do-kexec.sh
Source2:	http://www.xmission.com/~ebiederm/files/kexec/README
# Source2-md5:	b80e99096ec4ef37b09ecb5707233fb3
Patch0:		%{name}-opt.patch
URL:		http://www.xmission.com/~ebiederm/files/kexec/
BuildRequires:	autoconf
BuildRequires:	tar >= 1:1.15.1
BuildRequires:	zlib-devel
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
%setup -q -c -T
# workaround for kexec-tools-%{version}.spec outside main directory in tarball
tar xzf %{SOURCE0} --strip-components=1
%patch0 -p1

%build
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE2} README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS News README TODO
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/%{name}
