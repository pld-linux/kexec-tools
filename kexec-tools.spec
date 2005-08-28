Summary:	Tool for starting new kernel without reboot
Summary(pl):	Narzêdzie pozwalaj±ce za³adowaæ nowe j±dro bez konieczno¶ci restartu
Name:		kexec-tools
Version:	1.101
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://www.xmission.com/~ebiederm/files/kexec/%{name}-%{version}.tar.gz
# Source0-md5:	b4f7ffcc294d41a6a4c40d6e44b7734d
Source1:	do-kexec.sh
Source2:	http://www.xmission.com/~ebiederm/files/kexec/README
# Source2-md5:	b80e99096ec4ef37b09ecb5707233fb3
URL:		http://www.xmission.com/~ebiederm/files/kexec/
BuildRequires:	glibc-static
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
kexec is a set of system calls that allows you to load another kernel
from the currently executing Linux kernel. The current implementation
has only been tested, and had the kinks worked out on x86, but the
generic code should work on any architecture.

%description -l pl
Narzêdzie to pozwala wykorzystaæ zaimplementowany w j±drach 2.5/2.6
system pozwalaj±cy za³adowaæ nastêpne j±dro bez konieczno¶ci restartu
maszyny. Od momentu wydania polecenia kexec do startu nowego j±dra
up³ywa czas poni¿ej 0.5 sekundy!

Aktualna implementacja by³a testowana tylko na x86, ale ogólny kod
powinien dzia³aæ na ka¿dej architekturze.

%prep
%setup -q

%build
%configure
%{__make} \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags}"

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
%doc AUTHORS TODO News README
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/%{name}
