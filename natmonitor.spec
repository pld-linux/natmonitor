Summary:	This utility monitor hosts bandwidth usage in your home lan
Summary(pl):	Narz�dzie to monitoruje u�ycie szeroko�ci pasma w sieci lokalnej
Name:		natmonitor
Version:	0.9
Release:	1
License:	GPL
Group:		Networking
Source0:	%{name}-%{version}.tgz
Source1:	%{name}.desktop
URL:		http://natmonitor.sourceforge.net/
BuildRequires:	gtk+2-devel
Requires:	gtk+2
Requires:	libpcap
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NAT Monitor is a graphical monitor to keep tracks of hosts' bandwidth
usage in a Linux-NAT local network. NAT Monitor draws a stacked graph
with a different color for every LAN host. It autodetects hosts and
has a nice summary statistic.

%description -l pl

%prep
%setup -q -n %{name}

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir} \
	$RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_pixmapsdir} \
	$RPM_BUILD_ROOT%{_applnkdir}/Network/Misc
install natmonitor $RPM_BUILD_ROOT%{_bindir}
install natmonitor.conf $RPM_BUILD_ROOT%{_sysconfdir}
#for i in 16x16 32x32 36x36 48x48 64x64; do
#	install -d $RPM_BUILD_ROOT%{_pixmapsdir}/hicolor/$i/apps
#	install icons/%{name}$i.png $RPM_BUILD_ROOT%{_pixmapsdir}/hicolor/$i/apps/%{name}.png
#done
install icons/%{name}48x48.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png
install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Network/Misc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG README BUGS TODO
%attr(755,root,root) %{_bindir}/*
%attr(644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/%{name}.conf
%{_pixmapsdir}/%{name}.png
%{_applnkdir}/Network/Misc/%{name}.desktop
