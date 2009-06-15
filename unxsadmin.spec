Summary:	unxsadmin provides the http shared content and httpd conf.d file for all unxsVZ web admins
Name:		unxsadmin
Version:	1.4
Release:	0.1
License:	GPL
Group:		Networking/Admin
Source0:	http://unixservice.com/source/%{name}-%{version}.tar.gz
# Source0-md5:	fdffbedd992dbac31c8b6a3a6932ee4d
Source1:	%{name}.conf
URL:		http://openisp.net/unxsAdmin/
BuildRequires:	rpmbuild(macros) >= 1.268
Patch0:		%{name}-DESTDIR.patch
Requires(triggerpostun):	sed >= 4.0
Requires:	apache >= 2.2
Requires:	apache-mod_ssl >= 2.2
Requires:	apache-mod_dir >= 2.2
Requires:	rrdtool
Requires:	webapps

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
unxsadmin provides the http shared content and conf for all unxsVZ web
admins. It provides the dir layout in /var/www/unxs and all the shared
css, js and image content needed by unxsVZ family of web
administration interfaces like unxsMail, unxsApache, unxsVZ, unxsBind
and unxsISP. It also provides some common binary utilities like
lastmonth.

%prep
%setup -q
%patch0 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -d $RPM_BUILD_ROOT%{_datadir}/unxs/{cgi-bin,logs,html/{images,js,css}}

cp -a images/*.gif $RPM_BUILD_ROOT%{_datadir}/unxs/html/images/
cp -a js/*.js $RPM_BUILD_ROOT%{_datadir}/unxs/html/js
cp -a css/*.css $RPM_BUILD_ROOT%{_datadir}/unxs/html/css
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc README
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%dir %{_datadir}/unxs
%dir %{_datadir}/unxs/cgi-bin
%dir %{_datadir}/unxs/logs
%dir %{_datadir}/unxs/html
%dir %{_datadir}/unxs/html/css
%{_datadir}/unxs/html/css/*.css
%dir %{_datadir}/unxs/html/images
%{_datadir}/unxs/html/images/*.gif
%dir %{_datadir}/unxs/html/js
%{_datadir}/unxs/html/js/*.js
%attr(755,root,root) %{_bindir}/lastmonth
