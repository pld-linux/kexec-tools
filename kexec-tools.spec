%define		kernel_version	2.5.73
Summary:	Tool for starting new kernel without reboot
Summary(pl):	Narzêdzie pozwalaj±ce za³adowaæ nowe j±dro bez konieczno¶ci restartu
Name:		kexec-tools
Version:	1.8
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	http://www.osdl.org/archive/andyp/kexec/%{kernel_version}/%{name}-%{version}-%{kernel_version}.tgz
# Source0-md5:	1fb70ca3ab2075a4da1acc79917fd084
Source1:	do-kexec.sh
Patch0:		%{name}-opt.patch
URL:		http://www.xmission.com/~ebiederm/files/kexec/
BuildRequires:	glibc-static
Requires:	kernel >= %{kernel_version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%setup -q -n %{name}-%{version}-%{kernel_version}
%patch -p1

%build
find ./objdir -type f | xargs rm -f
%{__make} \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
install objdir/build/sbin/kexec $RPM_BUILD_ROOT%{_sbindir}
install objdir/build/bin/kexec_test $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc TODO News
%attr(755,root,root) %{_sbindir}/*
