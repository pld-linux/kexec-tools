%define		kernel_version	2.5.73
Summary:	Tool to starting new kernel without reboot.
Summary(pl):	Narzêdzie pozwalaj±ce za³adowaæ nowe j±dro bez konieczno¶ci restartu.
Name:		kexec-tools
Version:	1.8
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	http://www.osdl.org/archive/andyp/kexec/%{kernel_version}/%{name}-%{version}-%{kernel_version}.tgz
# Source0-md5:	1fb70ca3ab2075a4da1acc79917fd084
Source1:	do-kexec.sh
URL:		http://www.xmission.com/~ebiederm/files/kexec/
BuildRequires:	libstdc++-devel
Requires:	kernel >= %{kernel_version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl
Narzedzie to pozwala wykorzystac zaimplementowany w jadrach 2.5/2.6
system pozwalajacy zaladowac nastepny kernel bez koniecznosci restartu
maszyny. Od momentu wydania polecenia kexec do startu nowego kernela
uplywa czas ponizej 0.5 sekundy!

%prep
rm -rf $RPM_BUILD_ROOT
%setup -q -n %{name}-%{version}-%{kernel_version}

%build
find ./objdir -type f | xargs rm -f
%{__make}

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
