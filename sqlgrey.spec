Summary:	Postfix grey-listing policy service
Name:		sqlgrey
Version:	1.7.6
Release:	5
License:	GPL
Group:		System/Servers
URL:		http://sqlgrey.sourceforge.net
Source0:	http://prdownloads.sourceforge.net/sqlgrey/%{name}-%{version}.tar.bz2
Source1:	sqlgrey.init
Patch0:         sqlgrey-1.7.4-sqlite.patch
Patch1:         sqlgrey-1.7.4-warnings.patch
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires:	perl-DBD-SQLite
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
SQLgrey is a Postfix grey-listing policy service with
auto-white-listing written in Perl with SQL database as storage
backend. Greylisting stops 50 to 90 % junk mails (spam and virus)
before they reach your Postfix server (saves BW, user time and CPU
time).

%prep

%setup -q
%patch0 -p1
%patch1 -p0

%build

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_sysconfdir}/sqlgrey
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_localstatedir}/lib/sqlgrey
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
%_pre_useradd sqlgrey %{_localstatedir}/lib/sqlgrey /bin/sh

%post
%_post_service sqlgrey

%preun
%_preun_service sqlgrey

%postun 
%_postun_userdel sqlgrey

%clean
rm -rf %{buildroot}

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
%attr(0755,sqlgrey,sqlgrey) %dir %{_localstatedir}/lib/sqlgrey
%attr(0755,sqlgrey,sqlgrey) %dir %{_var}/run/sqlgrey
#%attr(0644,root,root) %{_mandir}/man1/sqlgrey.1*


%changelog
* Wed Dec 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1.7.6-4mdv2011.0
+ Revision: 614954
- the mass rebuild of 2010.1 packages

* Thu May 06 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1.7.6-3mdv2010.1
+ Revision: 542780
- S1 updated for LBS complain

* Tue Sep 08 2009 Thierry Vignaud <tv@mandriva.org> 1.7.6-2mdv2010.0
+ Revision: 434082
- rebuild

* Sun Sep 07 2008 Oden Eriksson <oeriksson@mandriva.com> 1.7.6-1mdv2009.0
+ Revision: 282267
- 1.7.6
- rediffed P1

* Sat Aug 02 2008 Thierry Vignaud <tv@mandriva.org> 1.7.5-5mdv2009.0
+ Revision: 260983
- rebuild

* Tue Jul 29 2008 Thierry Vignaud <tv@mandriva.org> 1.7.5-4mdv2009.0
+ Revision: 253014
- rebuild

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1.7.5-2mdv2008.1
+ Revision: 171118
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Sep 05 2007 Jérôme Soyer <saispo@mandriva.org> 1.7.5-1mdv2008.0
+ Revision: 80488
- New release 1.7.5
- Import sqlgrey



* Tue May 09 2006 Jerome Soyer <saispo@mandriva.org> 1.6.6-1mdk
- New release 1.6.6

* Tue Jul 05 2005 Oden Eriksson <oeriksson@mandriva.com> 1.6.2-1mdk
- 1.6.2 (Minor bugfixes)

* Sun Jun 19 2005 Oden Eriksson <oeriksson@mandriva.com> 1.6.0-1mdk
- 1.6.0 (Major feature enhancements)
- fix deps
- use the %%mkrel macro

* Mon Mar 07 2005 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.5.3-1mdk
- initial Mandrakelinux package
- added P0 & S1
- used fragments of the provided spec file
