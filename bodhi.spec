%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

Name:           bodhi
Version:        0.8.4
Release:        1%{?dist}
Summary:        A modular framework that facilitates publishing software updates
Group:          Applications/Internet
License:        GPLv2+
URL:            https://fedorahosted.org/bodhi
Source0:        bodhi-%{version}.tar.bz2

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires: python-setuptools 
BuildRequires: python-setuptools-devel
BuildRequires: python-devel

BuildRequires: TurboGears python-bugzilla
BuildRequires: python-fedora python-TurboMail TurboGears yum koji
BuildRequires: python-turboflot python-tgcaptcha
BuildRequires: python-fedora-turbogears

%description
Bodhi is a web application that facilitates the process of publishing
updates for a software distribution.

A modular piece of the Fedora Infrastructure stack
* Utilizes the Koji Buildsystem for tracking RPMs
* Creates the update repositories using Mash, which composes a repository based
  on tagged builds in Koji. 


%package client
Summary: Bodhi Client
Group: Applications/Internet
Requires: python-simplejson koji yum
Requires: python-fedora >= 0.3.5
Requires: python-kitchen

%description client
Client tools for interacting with bodhi


%package server
Summary: A modular framework that facilitates publishing software updates
Group: Applications/Internet
Requires: TurboGears
Requires: python-TurboMail
Requires: intltool
Requires: mash
Requires: cvs
Requires: koji
Requires: python-fedora
Requires: python-bugzilla
Requires: python-imaging
Requires: python-crypto
Requires: python-turboflot
Requires: python-tgcaptcha
Requires: python-decorator
Requires: mod_wsgi
Requires: httpd
Requires: python-markdown
Requires: python-hashlib
Requires: python-kitchen
Requires: python-simplemediawiki


%description server
Bodhi is a modular framework that facilitates the process of publishing
updates for a software distribution.

%prep
%setup -q
rm -rf bodhi/tests bodhi/tools/test-bodhi.py

%build
%{__python} setup.py build --install-data=%{_datadir}

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build \
    --install-data=%{_datadir} --root %{buildroot}

%{__mkdir_p} %{buildroot}/var/lib/bodhi
%{__mkdir_p} %{buildroot}%{_sysconfdir}/httpd/conf.d
%{__mkdir_p} %{buildroot}%{_sysconfdir}/bodhi
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}
%{__mkdir_p} -m 0755 %{buildroot}/%{_localstatedir}/log/bodhi

%{__install} -m 640 apache/%{name}.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
%{__install} -m 640 %{name}.cfg %{buildroot}%{_sysconfdir}/%{name}/
%{__install} -m 640 %{name}/config/*mash* %{buildroot}%{_sysconfdir}/%{name}/
%{__install} apache/%{name}.wsgi %{buildroot}%{_datadir}/%{name}/%{name}.wsgi

%{__install} %{name}/tools/client.py %{buildroot}%{_bindir}/%{name}


%clean
%{__rm} -rf %{buildroot}


%files server
%defattr(-,root,root,-)
%doc README COPYING
%{python_sitelib}/%{name}/
%{_bindir}/start-%{name}
%{_bindir}/%{name}-*
%config(noreplace) %{_sysconfdir}/httpd/conf.d/bodhi.conf
%dir %{_sysconfdir}/bodhi/
%attr(-,apache,root) %{_datadir}/%{name}
%attr(-,apache,root) %config(noreplace) %{_sysconfdir}/bodhi/*
%attr(-,apache,root) %{_localstatedir}/log/bodhi
%{python_sitelib}/%{name}-%{version}-py%{pyver}.egg-info/


%files client
%defattr(-,root,root,-)
%{_bindir}/bodhi
%{_mandir}/man1/bodhi.1.gz


%changelog
* Fri Oct 21 2011 Luke Macken <lmacken@redhat.com> - 0.8.3-1
- 0.8.3 release

* Mon Feb 28 2011 Luke Macken <lmacken@redhat.com> - 0.7.12
- 0.7.12 release

* Mon Jan 31 2011 Luke Macken <lmacken@redhat.com> - 0.7.11
- Require python-simplemediawiki for our test case integration

* Mon Jan 10 2011 Luke Macken <lmacken@redhat.com> - 0.7.10-1
- 0.7.10 release

* Fri Sep 10 2010 Luke Macken <lmacken@redhat.com> - 0.7.9-1
- 0.7.9 release

* Thu Aug 12 2010 Luke Macken <lmacken@redhat.com> - 0.7.8-1
- 0.7.8 release
- Have the bodhi-client subpackage require python-kitchen

* Tue Aug 03 2010 Luke Macken <lmacken@redhat.com> - 0.7.7-1
- 0.7.7 release

* Mon Jul 12 2010 Luke Macken <lmacken@redhat.com> - 0.7.6-1
- 0.7.6 release

* Tue Jun 29 2010 Luke Macken <lmacken@redhat.com> - 0.7.5-1
- 0.7.5 release

* Thu Mar 04 2010 Luke Macken <lmacken@redhat.com> - 0.7.4-1
- 0.7.4

* Thu Mar 04 2010 Luke Macken <lmacken@redhat.com> - 0.7.3-1
- 0.7.3

* Wed Mar 03 2010 Luke Macken <lmacken@redhat.com> - 0.7.2-1
- 0.7.2 bugfix release

* Tue Feb 16 2010 Luke Macken <lmacken@redhat.com> - 0.7.1-1
- Fix a regression in our metrics controller, and unvail a new
  metrics JSON API

* Mon Jan 18 2010 Luke Macken <lmacken@redhat.com> - 0.7.0-1
- 0.7.0 release, prepping for the F13 release
- Critical Path & No Frozen Rawhide proposals implemented
- Many other bugfixes, enhancements, and optimizations

* Fri Nov 06 2009 Luke Macken <lmacken@redhat.com> - 0.6.12-1
- 0.6.12, for F12

* Sat Sep 19 2009 Luke Macken <lmacken@redhat.com> - 0.6.11-1
- 0.6.11

* Fri Sep 18 2009 Luke Macken <lmacken@redhat.com> - 0.6.10-1
- 0.6.10

* Thu Sep 17 2009 Luke Macken <lmacken@redhat.com> - 0.6.9-2
- More CSRF tweaks

* Thu Sep 17 2009 Luke Macken <lmacken@redhat.com> - 0.6.9-1
- 0.6.9

* Mon Sep 14 2009 Luke Macken <lmacken@redhat.com> - 0.6.8-1
- 0.6.8

* Wed Sep 09 2009 Luke Macken <lmacken@redhat.com> - 0.6.7-1
- 0.6.7

* Wed Sep 09 2009 Luke Macken <lmacken@redhat.com> - 0.6.6-1
- 0.6.6

* Wed Sep 09 2009 Luke Macken <lmacken@redhat.com> - 0.6.5-1
- 0.6.5

* Fri Aug 14 2009 Luke Macken <lmacken@redhat.com> - 0.6.4-1
- 0.6.4

* Thu Aug 13 2009 Luke Macken <lmacken@redhat.com> - 0.6.3-1
- 0.6.3

* Fri Jul 10 2009 Luke Macken <lmacken@redhat.com> - 0.6.2-1
- 0.6.2

* Thu Jul 09 2009 Luke Macken <lmacken@redhat.com> - 0.6.1-1
- 0.6.1

* Thu Jul 09 2009 Luke Macken <lmacken@redhat.com> - 0.6.0-1
- 0.6.0 final

* Mon Jul 06 2009 Luke Macken <lmacken@redhat.com> - 0.6.0-0.7.beta
- beta7

* Mon Jul 06 2009 Luke Macken <lmacken@redhat.com> - 0.6.0-0.6.beta
- beta6

* Mon Jul 06 2009 Luke Macken <lmacken@redhat.com> - 0.6.0-0.5.beta
- beta5, with EPEL mash configs

* Fri Jul 03 2009 Luke Macken <lmacken@redhat.com> - 0.6.0-0.4.beta
- beta4

* Fri Jul 03 2009 Luke Macken <lmacken@redhat.com> - 0.6.0-0.3.beta
- beta3

* Fri Jul 03 2009 Luke Macken <lmacken@redhat.com> - 0.6.0-0.2.beta
- beta2
- Make our Bugzilla cookie file configurable

* Thu Jul 02 2009 Luke Macken <lmacken@redhat.com> - 0.6.0-0.1.beta
- 0.6.0 beta

* Mon Jun 22 2009 Luke Macken <lmacken@redhat.com> - 0.5.27-01
- Latest upstream release to bring in fixed mash config files.

* Fri Jun 12 2009 Luke Macken <lmacken@redhat.com> - 0.5.26-1
- Latest upstream release with a variety of fixes and pkgdb-0.4 support.

* Tue May 12 2009 Luke Macken <lmacken@redhat.com> - 0.5.25-1
- Latest upstream bugfix release to work around some TG 1.0.8
  brokenness, and make our masher a bit more robust.

* Tue May 12 2009 Luke Macken <lmacken@redhat.com> - 0.5.24-1
- 0.5.24 bugfix release

* Thu May 07 2009 Luke Macken <lmacken@redhat.com> - 0.5.23-1
- Add mash configs for F11, with deltarpm support.

* Thu Apr 30 2009 Luke Macken <lmacken@redhat.com> - 0.5.22-1
- Remove pagination patch, as Fedora Infrastructure is now TG 1.0.8

* Thu Apr 30 2009 Luke Macken <lmacken@redhat.com> - 0.5.21-1
- Update to TG 1.0.8 API (fixes a @paginate issue)

* Mon Apr 06 2009 Luke Macken <lmacken@redhat.com> - 0.5.20-1
- Fix a bug when sending mash requests through the ProxyClient
- More Python2.4 workarounds

* Mon Apr 06 2009 Luke Macken <lmacken@redhat.com> - 0.5.19-3
- Update to work with Python2.4

* Mon Apr 06 2009 Luke Macken <lmacken@redhat.com> - 0.5.19-2
- Revision bump to bring it up to speed with the fedora infra package

* Sat Mar 21 2009 Luke Macken <lmacken@redhat.com> - 0.5.19-1
- 0.5.19
- Add a patch to get pagination working in TG 1.0.4.4

* Sat Mar 14 2009 Luke Macken <lmacken@redhat.com> - 0.5.17-4
- Require httpd

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 10 2009 Luke Macken <lmacken@redhat.com> - 0.5.18-1
- Bugfix release, and to stop using deprecated python-fedora APIs.

* Mon Feb 2 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.5.17-2
- Own the %%{_sysconfdir}/bodhi directory.

* Thu Jan 22 2009 Luke Macken <lmacken@redhat.com> - 0.5.17-1
- Latest upstream bugfix release.

* Mon Jan 05 2009 Luke Macken <lmacken@redhat.com> - 0.5.16-1
- Latest upstream bugfix release.

* Mon Dec 22 2008 Luke Macken <lmacken@redhat.com> - 0.5.15-1
- Latest release, with more masher improvements.

* Fri Dec 19 2008 Luke Macken <lmacken@redhat.com> - 0.5.14-1
- Latest upstream release, containing some masher improvements.

* Wed Dec 10 2008 Luke Macken <lmacken@redhat.com> - 0.5.13-1
- Latest upstream release to fix various metrics/rss issues

* Mon Nov 24 2008 Luke Macken <lmacken@redhat.com> - 0.5.12-1
- Latest upstream release, to fix the 10k bug

* Fri Nov 21 2008 Luke Macken <lmacken@redhat.com> - 0.5.11-1
- Various F10 release tweaks

* Fri Oct 24 2008 Luke Macken <lmacken@redhat.com> - 0.5.10-3
- Latest upstream release

* Wed Oct 15 2008 Luke Macken <lmacken@redhat.com> - 0.5.9-2
- Fix a trivial module import issue

* Tue Oct 14 2008 Luke Macken <lmacken@redhat.com> - 0.5.9-1
- Fix a variety of bugs, including a race-condition when editing.

* Thu Oct 13 2008 Steve 'Ashcrow' Milner <smilner@redhat.com> - 0.5.8-2
- Added default attributes to client files.

* Sun Oct 12 2008 Luke Macken <lmacken@redhat.com> - 0.5.8-1
- Minor release to fix some new update creation bugs

* Thu Oct 09 2008 Luke Macken <lmacken@redhat.com> - 0.5.7-1
- Latest release, containing some API improvements

* Tue Oct 07 2008 Luke Macken <lmacken@redhat.com> - 0.5.6-1
- Latest upstream release.

* Mon Oct 06 2008 Luke Macken <lmacken@redhat.com> - 0.5.5-1
- Latest upstream release.

* Sat Oct 04 2008 Luke Macken <lmacken@redhat.com> - 0.5.4-2
- Make our masher extension point less obtrusive.

* Tue Sep 16 2008 Luke Macken <lmacken@redhat.com> - 0.5.4-1
- Latest upstream release, containing various bugfixes
- Make our python-fedora requirement explicit (#461518)

* Wed Sep 10 2008 Luke Macken <lmacken@redhat.com> - 0.5.3-1
- Latest upstream release

* Wed Sep 03 2008 Luke Macken <lmacken@redhat.com> - 0.5.2-2
- Add the masher deps to BuildRequires, since it now resides
  on the turbogears.extensions entry point and will be
  imported by pkg_resources at build time.

* Wed Sep 03 2008 Luke Macken <lmacken@redhat.com> - 0.5.2-1
- Latest upstream bugfix release

* Fri Aug 29 2008 Luke Macken <lmacken@redhat.com> - 0.5.1-3
- Fix some setuptools issues with our client subpackage

* Mon Aug 25 2008 Luke Macken <lmacken@redhat.com> - 0.5.1-2
- Include the egg-info in the client subpackage.

* Fri Aug 22 2008 Luke Macken <lmacken@redhat.com> - 0.5.1-1
- Latest upstream release

* Sun Jul 06 2008 Luke Macken <lmacken@redhat.com> - 0.5.0-1
- Latest upstream release

* Thu Jun 12 2008 Todd Zullinger <tmz@pobox.com> - 0.4.10-5
- update URL to point to fedorahosted.org

* Fri Apr 04 2008 Luke Macken <lmacken@redhat.com> - 0.4.10-4
- Add python-tgcaptcha to our server requirements

* Tue Feb 26 2008 Luke Macken <lmacken@redhat.com> - 0.4.10-3
- Add python-bugzilla to our server requirements

* Fri Jan 25 2008 Luke Macken <lmacken@redhat.com> - 0.4.10-2
- Add python-elixir to BuildRequires to make the new TG happy

* Fri Jan 25 2008 Luke Macken <lmacken@redhat.com> - 0.4.10-1
- 0.4.10
- Remove yum-utils requirement from bodhi-server

* Sun Jan  6 2008 Luke Macken <lmacken@redhat.com> - 0.4.9-1
- 0.4.9

* Sat Dec  7 2007 Luke Macken <lmacken@redhat.com> - 0.4.8-1
- 0.4.8

* Wed Nov 28 2007 Luke Macken <lmacken@redhat.com> - 0.4.7-1
- 0.4.7

* Tue Nov 20 2007 Luke Macken <lmacken@redhat.com> - 0.4.6-1
- 0.4.6

* Sun Nov 18 2007 Luke Macken <lmacken@redhat.com> - 0.4.5-2
- Add python-genshi to BuildRequires

* Sat Nov 17 2007 Luke Macken <lmacken@redhat.com> - 0.4.5-1
- 0.4.5

* Wed Nov 14 2007 Luke Macken <lmacken@redhat.com> - 0.4.4-1
- 0.4.4

* Mon Nov 12 2007 Luke Macken <lmacken@redhat.com> - 0.4.3-1
- 0.4.3

* Mon Nov 12 2007 Luke Macken <lmacken@redhat.com> - 0.4.2-1
- 0.4.2

* Mon Nov 12 2007 Luke Macken <lmacken@redhat.com> - 0.4.1-1
- 0.4.1

* Sun Nov 11 2007 Luke Macken <lmacken@redhat.com> - 0.4.0-1
- Lots of bodhi-client features

* Wed Nov  7 2007 Luke Macken <lmacken@redhat.com> - 0.3.3-1
- 0.3.3

* Thu Oct 18 2007 Luke Macken <lmacken@redhat.com> - 0.3.2-2
- Add TurboGears to BuildRequires
- Make some scripts executable to silence rpmlint

* Sat Oct 16 2007 Luke Macken <lmacken@redhat.com> - 0.3.2-1
- 0.3.2
- Add COPYING file
- s/python-json/python-simplejson/

* Sat Oct  6 2007 Luke Macken <lmacken@redhat.com> - 0.3.1-1
- 0.3.1

* Wed Oct  3 2007 Luke Macken <lmacken@redhat.com> - 0.2.0-5
- Add python-fedora to bodhi-client Requires

* Mon Sep 17 2007 Luke Macken <lmacken@redhat.com> - 0.2.0-4
- Add python-json to bodhi-client Requires

* Sun Sep 16 2007 Luke Macken <lmacken@redhat.com> - 0.2.0-3
- Add cvs to bodhi-server Requires

* Thu Sep 15 2007 Luke Macken <lmacken@redhat.com> - 0.2.0-2
- Handle python-setuptools-devel changes in Fedora 8
- Update license to GPLv2+

* Thu Sep 13 2007 Luke Macken <lmacken@redhat.com> - 0.2.0-1
- Split spec file into client/server subpackages