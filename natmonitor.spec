Summary:	This utility monitor hosts bandwidth usage in your home lan
Summary(pl):	Narzêdzie monitoruj±ce u¿ycie szeroko¶ci pasma w sieci lokalnej
Name:		natmonitor
Version:	2.4
Release:	0.3
License:	GPL
Group:		Networking
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tgz
# Source0-md5:	22c15163254ec9f9f3e86c27a398d118
Source1:	%{name}.desktop
Source2:	natmonitord.init
Patch0:		natmonitord-datadir.patch
Patch1:		%{name}-make.patch
Patch2:		%{name}-noc99.patch
URL:		http://natmonitor.sourceforge.net/
BuildRequires:	gtk+2-devel
BuildRequires:	libpcap-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NAT Monitor is a graphical monitor to keep tracks of hosts' bandwidth
usage in a Linux-NAT local network. NAT Monitor draws a stacked graph
with a different color for every LAN host. It autodetects hosts and
has a nice summary statistic.

%description -l pl
NAT Monitor to graficzny monitor ¶ledz±cy wykorzystanie pasma przez
hosty w sieci lokalnej za linuksowym NAT-em. NAT Monitor rysuje wykres
innym kolorem dla ka¿dego hosta z sieci lokalnej. Automatycznie
wykrywa hosty i ma ³adne statystyki podsumowuj±ce.

%package -n     natmonitord
Summary:        The NAT Monitor daemon
Summary(pl):	Daemon monitora NAT
Group:          System/Servers

%description -n natmonitord
The NAT Monitor daemon collects data for the natmonitor clients.

%description -n natmonitord -l pl
Daemon zbierajacy dane dla natmonitora.

%prep
%setup -q
%patch0 -p0

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir} \
	$RPM_BUILD_ROOT%{_initrddir} \
	$RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_sbindir} \
	$RPM_BUILD_ROOT%{_pixmapsdir} \
	$RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT/var/lib/natmonitor

install natmonitor natmonitord natmonitorconsole $RPM_BUILD_ROOT%{_bindir}
install natmonitord $RPM_BUILD_ROOT%{_sbindir}
install natmonitor.conf natmonitord.conf $RPM_BUILD_ROOT%{_sysconfdir}
#for i in 16x16 32x32 36x36 48x48 64x64; do
#	install -d $RPM_BUILD_ROOT%{_pixmapsdir}/hicolor/$i/apps
#	install icons/%{name}$i.png $RPM_BUILD_ROOT%{_pixmapsdir}/hicolor/$i/apps/%{name}.png
#done
install icons/%{name}48x48.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/natmonitord
%clean
rm -rf $RPM_BUILD_ROOT

%post -n natmonitord
/sbin/chkconfig --add natmonitord
if [ -f /var/lock/subsys/natmonitord ]; then
        /etc/rc.d/init.d/natmonitord restart >&2
else
        echo "Run \"/etc/rc.d/init.d/natmonitord start\" to start natmonitord daemon." >&2
fi

%preun -n natmonitord
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/natmonitord ]; then
                /etc/rc.d/init.d/natmonitord stop >&2
        fi
        /sbin/chkconfig --del natmonitord
fi

%files
%defattr(644,root,root,755)
%doc CHANGELOG README BUGS TODO
%attr(755,root,root) %{_bindir}/natmonitor
%attr(755,root,root) %{_bindir}/natmonitorconsole
%attr(644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/%{name}.conf
%{_pixmapsdir}/%{name}.png
%{_desktopdir}/%{name}.desktop

%files -n natmonitord
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/natmonitord
%attr(755,root,root) %{_initrddir}/natmonitord
%attr(644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/natmonitord.conf
%attr(755,root,root) %dir /var/lib/natmonitor
