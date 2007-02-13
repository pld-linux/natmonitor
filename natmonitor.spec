Summary:	This utility monitor hosts bandwidth usage in your home lan
Summary(pl.UTF-8):	Narzędzie monitorujące użycie szerokości pasma w sieci lokalnej
Name:		natmonitor
Version:	2.4
Release:	2
License:	GPL
Group:		Networking
Source0:	http://dl.sourceforge.net/natmonitor/%{name}-%{version}.tgz
# Source0-md5:	22c15163254ec9f9f3e86c27a398d118
Source1:	%{name}.desktop
Source2:	%{name}d.init
Patch0:		%{name}-complex.patch
Patch1:		%{name}-etc.patch
Patch2:		%{name}-border_fix.patch
Patch3:		%{name}-command_line_conf.patch
URL:		http://natmonitor.sourceforge.net/
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	libpcap-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.202
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NAT Monitor is a graphical monitor to keep tracks of hosts' bandwidth
usage in a Linux-NAT local network. NAT Monitor draws a stacked graph
with a different color for every LAN host. It autodetects hosts and
has a nice summary statistic.

%description -l pl.UTF-8
NAT Monitor to graficzny monitor śledzący wykorzystanie pasma przez
hosty w sieci lokalnej za linuksowym NAT-em. NAT Monitor rysuje wykres
innym kolorem dla każdego hosta z sieci lokalnej. Automatycznie
wykrywa hosty i ma ładne statystyki podsumowujące.

%package -n natmonitord
Summary:	The NAT Monitor daemon
Summary(pl.UTF-8):	Daemon monitora NAT
Group:		Daemons
Requires:	rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Provides:	group(natmonitor)
Provides:	user(natmonitor)

%description -n natmonitord
The NAT Monitor daemon collects data for the natmonitor clients.

%description -n natmonitord -l pl.UTF-8
Daemon zbierający dane dla natmonitora.

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__sed} -i 's,USER.*,USER natmonitor,' natmonitord.conf
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

install natmonitor natmonitorconsole $RPM_BUILD_ROOT%{_bindir}
install natmonitord $RPM_BUILD_ROOT%{_sbindir}
install natmonitor.conf natmonitord.conf $RPM_BUILD_ROOT%{_sysconfdir}
install icons/%{name}48x48.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/natmonitord

cat > $RPM_BUILD_ROOT/var/lib/natmonitor/natmonitor.dat <<EOF
MINS SAMPLES 0
HOURS SAMPLES 0
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%pre -n natmonitord
%groupadd -g 159 natmonitor
%useradd -u 159 -d %{_var}/lib/natmonitor -c "NAT Monitor" -g natmonitor natmonitor

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

%postun -n natmonitord
if [ "$1" = "0" ]; then
	%userremove natmonitor
	%groupremove natmonitor
fi

%files
%defattr(644,root,root,755)
%doc CHANGELOG README BUGS TODO
%attr(755,root,root) %{_bindir}/natmonitor
%attr(755,root,root) %{_bindir}/natmonitorconsole
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%{_pixmapsdir}/%{name}.png
%{_desktopdir}/%{name}.desktop

%files -n natmonitord
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/natmonitord
%attr(754,root,root) %{_initrddir}/natmonitord
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/natmonitord.conf
%attr(750,natmonitor,natmonitor) %dir /var/lib/natmonitor
%attr(644,natmonitor,natmonitor) %ghost /var/lib/natmonitor/natmonitor.dat
