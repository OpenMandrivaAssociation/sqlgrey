Summary:	Postfix grey-listing policy service
Name:		sqlgrey
Version:	1.7.5
Release:	%mkrel 2
License:	GPL
Group:		System/Servers
URL:		http://sqlgrey.sourceforge.net
Source0:	http://prdownloads.sourceforge.net/sqlgrey/%{name}-%{version}.tar.bz2
Source1:	sqlgrey.init
Patch0:         sqlgrey-1.7.4-sqlite.patch
Patch1:         sqlgrey-1.7.4-warnings.patch
Requires(post,preun): rpm-helper
Requires(pre,postun): rpm-helper
Requires:	perl-DBD-SQLite
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
SQLgrey is a Postfix grey-listing policy service with
auto-white-listing written in Perl with SQL database as storage
backend. Greylisting stops 50 to 90 % junk mails (spam and virus)
before they reach your Postfix server (saves BW, user time and CPU
time).

%prep

%setup -q
%patch0 -p1
%patch1 -p1


%build

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_sysconfdir}/sqlgrey
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_localstatedir}/sqlgrey
install -d %{buildroot}%{_var}/run/sqlgrey

install -m0755 sqlgrey %{buildroot}%{_sbindir}/
install -m0755 update_sqlgrey_config %{buildroot}%{_sbindir}/
install -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/sqlgrey
install -m0644 etc/sqlgrey.conf %{buildroot}%{_sysconfdir}/sqlgrey/
install -m0644 etc/clients_ip_whitelist %{buildroot}%{_sysconfdir}/sqlgrey/
install -m0644 etc/clients_fqdn_whitelist %{buildroot}%{_sysconfdir}/sqlgrey/
install -m0644 etc/dyn_fqdn.regexp %{buildroot}%{_sysconfdir}/sqlgrey/
install -m0644 etc/smtp_server.regexp %{buildroot}%{_sysconfdir}/sqlgrey/
#install -m0644 sqlgrey.1 %{buildroot}%{_mandir}/man1/

%pre
%_pre_useradd sqlgrey %{_localstatedir}/sqlgrey /bin/sh

%post
%_post_service sqlgrey

%preun
%_preun_service sqlgrey

%postun 
%_postun_userdel sqlgrey

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING Changelog FAQ HOWTO README TODO
%attr(0755,root,root) %{_initrddir}/sqlgrey
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sqlgrey/sqlgrey.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sqlgrey/clients_ip_whitelist
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sqlgrey/clients_fqdn_whitelist
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sqlgrey/dyn_fqdn.regexp
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sqlgrey/smtp_server.regexp
%attr(0755,root,root) %{_sbindir}/sqlgrey
%attr(0755,root,root) %{_sbindir}/update_sqlgrey_config
%attr(0755,sqlgrey,sqlgrey) %dir %{_localstatedir}/sqlgrey
%attr(0755,sqlgrey,sqlgrey) %dir %{_var}/run/sqlgrey
#%attr(0644,root,root) %{_mandir}/man1/sqlgrey.1*
