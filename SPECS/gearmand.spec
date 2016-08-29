# Use systemd unit files on Fedora 18 and above.
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 18
  %global _with_systemd 1
%endif

# Skip deps that are too old on EL5.
%if 0%{?el5}
  %global _with_gperftools 0
  %global _with_sqlite 0
  %global _with_tokyocabinet 0
%else
  %global _with_gperftools 1
  %global _with_sqlite 1
  %global _with_tokyocabinet 1
%endif

Name:           gearmand
Version:        1.1.12
Release:        19%{?dist}
Summary:        A distributed job system

Group:          System Environment/Daemons
License:        BSD
URL:            http://www.gearman.org
Source0:        https://launchpad.net/gearmand/1.2/%{version}/+download/gearmand-%{version}.tar.gz
Source1:        gearmand.init
Source2:        gearmand.sysconfig
Source3:        gearmand.service
Patch0:		gearmand-1.1.12-ppc64le.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Fails to build on PPC.
# See https://bugzilla.redhat.com/987104 and https://bugzilla.redhat.com/987109
ExcludeArch:    ppc

%if 0%{?el5}
BuildRequires:  e2fsprogs-devel
BuildRequires:  boost141-devel, boost141-thread
#BuildRequires:  gcc44 gcc44-c++ libstdc++44-devel
%else
BuildRequires:  libuuid-devel
BuildRequires:  boost-devel >= 1.37.0, boost-thread
%endif
%if %{_with_sqlite}
BuildRequires:  sqlite-devel
%endif
%if %{_with_tokyocabinet}
BuildRequires:  tokyocabinet-devel
%endif
BuildRequires:  libevent-devel
BuildRequires:  libmemcached-devel, memcached
BuildRequires:  gperf
BuildRequires:  mysql-devel
BuildRequires:  postgresql-devel
BuildRequires:  zlib-devel

%if 0%{?_with_systemd}
BuildRequires: systemd-units
%endif

# For %%check
#BuildRequires:  curl-devel
#%if 0%{?fedora} >= 20 || 0%{?rhel} >= 7
#BuildRequires:  mariadb-server
#%else
#BuildRequires:  mysql-server
#%endif

# google perftools available only on these
%ifarch %{ix86} x86_64 ppc64 ppc64le aarch64 %{arm}
%if %{_with_gperftools}
BuildRequires: gperftools-devel
%endif
%endif
Requires(pre):   shadow-utils
Requires:        procps

%if 0%{?_with_systemd}
# This is actually needed for the %%triggerun script but Requires(triggerun)
# is not valid.  We can use %%post because this particular %%triggerun script
# should fire just after this package is installed.
Requires(post): systemd-sysv
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%else
Requires(post):  chkconfig
Requires(preun): chkconfig, initscripts
%endif

%description
Gearman provides a generic framework to farm out work to other machines
or dispatch function calls to machines that are better suited to do the work.
It allows you to do work in parallel, to load balance processing, and to
call functions between languages. It can be used in a variety of applications,
from high-availability web sites to the transport for database replication.
In other words, it is the nervous system for how distributed processing
communicates.


%package -n libgearman
Summary:        Development libraries for gearman
Group:          Development/Libraries
Provides:       libgearman-1.0 = %{version}-%{release}
Obsoletes:      libgearman-1.0 < %{version}-%{release}
%if 0%{?el5}
# gearman requires uuid_generate_time_safe, which only exists in newer
# e2fsprogs-libs
Requires:       e2fsprogs-libs >= 1.39-32
%endif

%description -n libgearman
Development libraries for %{name}.

%package -n libgearman-devel
Summary:        Development headers for libgearman
Requires:       pkgconfig, libgearman = %{version}-%{release}
Group:          Development/Libraries
Requires:       libevent-devel
Provides:       libgearman-1.0-devel = %{version}-%{release}
Obsoletes:      libgearman-1.0-devel < %{version}-%{release}

%description -n libgearman-devel
Development headers for %{name}.

%prep
%setup -q
%patch0 -p1

%if 0%{?el5}
  # libgearman-1.0 requires a header that's newer than what we have on EL5.
  # It looks like it's optional. (If not, we will have to build with gcc44.)
  sed -i '/include <tr1\/cinttypes>/d' libgearman-1.0/gearman.h
%endif

%build
%if 0%{?el5}
  # We have to use the parallel version of Boost
  #export CC='gcc44'
  #export CXX='gcc44-c++'
  #export CPPFLAGS="-I%{_includedir}/boost141 -I%{_includedir}/c++/4.4.7"
  export CPPFLAGS="-I%{_includedir}/boost141"
  export LDFLAGS="-L%{_libdir}/boost141"
%else
  # HACK to work around boost issues.
  export LDFLAGS="$LDFLAGS -lboost_system"
%endif

%ifarch ppc64 sparc64
# no tcmalloc
%configure --disable-static --disable-rpath --disable-silent-rules
%else
%configure --disable-static --disable-rpath --enable-tcmalloc --disable-silent-rules
%endif

%if 0%{?el5}
# the sed operations may be causing this to fail on EL5
%else
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%endif
make %{_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -v %{buildroot}%{_libdir}/libgearman*.la
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/gearmand

%if 0%{?_with_systemd}
  # install systemd unit file
  mkdir -p %{buildroot}%{_unitdir}
  install -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service
%else
  # install legacy SysV init script
  install -p -D -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/gearmand
  mkdir -p %{buildroot}/var/run/gearmand
%endif

mkdir -p %{buildroot}/var/log
touch %{buildroot}/var/log/gearmand.log

%check
#make check

%clean
rm -rf %{buildroot}


%pre
getent group gearmand >/dev/null || groupadd -r gearmand
getent passwd gearmand >/dev/null || \
        useradd -r -g gearmand -d / -s /sbin/nologin \
        -c "Gearmand job server" gearmand
exit 0

%post
%if 0%{?_with_systemd}
  %systemd_post gearmand.service
%else
  if [ $1 = 1 ]; then
    /sbin/chkconfig --add gearmand
  fi
%endif
/bin/touch /var/log/gearmand.log


%preun
%if 0%{?_with_systemd}
  %systemd_preun gearmand.service
%else
  if [ "$1" = 0 ] ; then
    /sbin/service gearmand stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del gearmand
  fi
  exit 0
%endif

%postun
%if 0%{?_with_systemd}
  %systemd_postun_with_restart gearmand.service
%endif

%post -n libgearman -p /sbin/ldconfig

%postun -n libgearman -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%if 0%{?el5} || 0%{?el6}
%attr(755,gearmand,gearmand) /var/run/gearmand
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/gearmand
%{_sbindir}/gearmand
%{_bindir}/gearman
%{_bindir}/gearadmin
%{_mandir}/man1/*
%{_mandir}/man8/*
%attr(0640,gearmand,gearmand) %config(noreplace) %verify(not md5 size mtime) /var/log/gearmand.log
%if 0%{?_with_systemd}
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%endif

%files -n libgearman
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libgearman.so.8
%{_libdir}/libgearman.so.8.0.0

%files -n libgearman-devel
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%dir %{_includedir}/libgearman
%{_includedir}/libgearman/*.h
%{_libdir}/pkgconfig/gearmand.pc
%{_libdir}/libgearman.so
%{_includedir}/libgearman-1.0/
%{_mandir}/man3/*


%changelog
* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.12-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Feb 02 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.1.12-17
- Rebuilt for Boost 1.60
- Append --disable-silent-rules to %%configure.

* Tue Jan 19 2016 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 1.1.12-16
- gperftools is available on wider selection of architectures - rhbz#1256287

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 1.1.12-15
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.12-14
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 1.1.12-13
- rebuild for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.12-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.1.12-11
- Rebuilt for GCC 5 C++11 ABI change

* Wed Mar 18 2015 Adam Jackson <ajax@redhat.com> 1.1.12-10
- Re-add Fedora conditional dropped in 1.1.12-1, which had the (probably)
  unintended side-effect of reverting Fedora to sysvinit from systemd.

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 1.1.12-9
- Rebuild for boost 1.57.0

* Tue Sep 09 2014 Karsten Hopp <karsten@redhat.com> 1.1.12-8
- enable ppc64

* Tue Sep 09 2014 Karsten Hopp <karsten@redhat.com> 1.1.12-7
- fix library path for ppc64le

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 1.1.12-4
- Rebuild for boost 1.55.0

* Fri May 23 2014 David Tardon <dtardon@redhat.com> - 1.1.12-3
- rebuild for boost 1.55.0

* Fri Apr 25 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.1.12-2
- Add missing Source0 tarball (oops)

* Fri Apr 25 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.1.12-1
- Update to latest upstream release
- Drop Fedora 18 conditional
- Add el5 e2fsprogs-libs minimum version requirement
- Fix bogus changelog date

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 27 2013 pmachata@redhat.com - 1.1.8-3
- Rebuild for boost 1.54.0

* Mon Jul 22 2013 Blake Gardner <blakegardner@cox.net> - 1.1.8-2
- ExcludeArch ppc ppc64

* Thu Jul 18 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.1.8-1
- Update to latest upstream release.
- Add EL5 and EL6 conditionals to unify the spec across all branches.
- Add mandirs.
- Add /var/log/gearmand.log.
- Add tokyocabinet support.
- Remove commented patches.
- rpmlint fixes (macros in comments).

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.1.2-3
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.1.2-2
- Rebuild for Boost-1.53.0

* Thu Oct 18 2012 BJ Dierkes <wdierkes@rackspace.com> - 1.1.2-1
- Bumping to 1.2 branch (1.1.2 current development version).
  Release notes are available here:
  https://launchpad.net/gearmand/1.2/1.1.2
- Repackaged libgearman-1.0, and libgearman-1.0-devel under the
  devel sub-package.
- Updated scriptlets per BZ#850127
 
* Mon Sep 24 2012 BJ Dierkes <wdierkes@rackspace.com> - 0.39-1
- Latest sources from upstream. Release notes here:
  https://launchpad.net/gearmand/trunk/0.39
- Added Postgres support
- Added Sqlite support

* Wed Aug 15 2012 BJ Dierkes <wdierkes@rackspace.com> - 0.35-1
- Latest sources from upstream. Release notes here:
  https://launchpad.net/gearmand/trunk/0.35
- Removed Patch3: gearmand-0.33-lp1020778.patch (applied upstream)
- Added zlib support
- Added MySQL support 

* Wed Aug 15 2012 BJ Dierkes <wdierkes@rackspace.com> - 0.33-3
- Rebuilt for latest boost.
- BuildRequires: boost-thread
- Added -lboost_system to LDFLAGS to work around boost issue
  related to boost-thread.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 03 2012 BJ Dierkes <wdierkes@rackspace.com> - 0.33-1
- Latest sources from upstream.  Release notes here:
  https://launchpad.net/gearmand/trunk/0.33
- Adding Patch3: gearmand-0.33-lp1020778.patch

* Mon Apr 23 2012  Remi Collet <remi@fedoraproject.org> - 0.32-2
- rebuild against libmemcached.so.10

* Wed Apr 18 2012 BJ Dierkes <wdierkes@rackspace.com> - 0.32-1
- Latest sources from upstream.  Release notes here:
  https://launchpad.net/gearmand/trunk/0.32
- Removed Patch2: gearmand-0.31-lp978235.patch (applied upstream)

* Tue Apr 10 2012 BJ Dierkes <wdierkes@rackspace.com> - 0.31-1
- Latest sources from upstream.  Release notes here:
  https://launchpad.net/gearmand/trunk/0.31
  https://launchpad.net/gearmand/trunk/0.29
- Removed Patch1: gearmand-0.28-lp932994.patch (applied upstream)
- Added Patch2: gearmand-0.31-lp978235.patch.  Resolves LP#978235.

* Wed Mar 07 2012 BJ Dierkes <wdierkes@rackspace.com> - 0.28-3
- Adding back _smp_mflags

* Wed Mar 07 2012 BJ Dierkes <wdierkes@rackspace.com> - 0.28-2
- Added Patch1: gearmand-0.28-lp932994.patch.  Resolves: LP#932994

* Fri Jan 27 2012 BJ Dierkes <wdierkes@rackspace.com> - 0.28-1
- Latest sources from upstream.  Release notes here:
  https://launchpad.net/gearmand/trunk/0.28
- Removing Patch0: gearmand-0.27-lp914495.patch (applied upstream)
- Removing _smp_mflags per https://bugs.launchpad.net/bugs/901007

* Thu Jan 12 2012 BJ Dierkes <wdierkes@rackspace.com> - 0.27-2
- Adding Patch0: gearmand-0.27-lp914495.patch Resolves LP#914495

* Tue Jan 10 2012 BJ Dierkes <wdierkes@rackspace.com> - 0.27-1
- Latest sources from upstream.  Release notes here:
  https://launchpad.net/gearmand/trunk/0.27
 
* Tue Nov 22 2011 BJ Dierkes <wdierkes@rackspace.com> - 0.25-1
- Latest sources from upstream.  Release notes here:
  https://launchpad.net/gearmand/trunk/0.25
- Also rebuild against libboost_program_options-mt.so.1.47.0 
- Added libgearman-1.0, libgearman-1.0-devel per upstream 

* Sat Sep 17 2011  Remi Collet <remi@fedoraproject.org> - 0.23-2
- rebuild against libmemcached.so.8

* Thu Jul 21 2011 BJ Dierkes <wdierkes@rackspace.com> - 0.23-1
- Latest source from upstream.  Release information available at:
  https://launchpad.net/gearmand/+milestone/0.23

* Fri Jun 03 2011 BJ Dierkes <wdierkes@rackspace.com> - 0.20-1
- Latest sources from upstream.  
- Add %%ghost to /var/run/gearmand. Resolves BZ#656592
- BuildRequires: boost-devel >= 1.37.0
- Adding gearadmin files
- Converted to Systemd.  Resolves BZ#661643

* Tue Mar 22 2011 Dan Horák <dan[at]danny.cz> - 0.14-4
- switch to %%ifarch for google-perftools as BR

* Thu Feb 17 2011 BJ Dierkes <wdierkes@rackspace.com> - 0.14-3
- Rebuild against latest libevent in rawhide/f15

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 BJ Dierkes <wdierkes@rackspace.com> - 0.14-1
- Latest sources from upstream.  Full changelog available from:
  https://launchpad.net/gearmand/trunk/0.14

* Wed Oct 06 2010 Remi Collet <fedora@famillecollet.com> - 0.13-3
- rebuild against new libmemcached

* Wed May 05 2010 Remi Collet <fedora@famillecollet.com> - 0.13-2
- rebuild against new libmemcached

* Wed Apr 07 2010 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.13-1
- Upstream released new version

* Fri Feb 19 2010 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.12-1
- Upstream released new version

* Wed Feb 17 2010 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.11-2
- Add BR on libtool

* Tue Feb 16 2010 Oliver Falk <oliver@linux-kernel.at> 0.11-1
- Update to latest upstream version (#565808)
- Add missing Req. libevent-devel for libgearman-devel (#565808)
- Remove libmemcache patch - should be fixed in 0.11

* Sun Feb 07 2010 Remi Collet <fedora@famillecollet.com> - 0.9-3
- patch to detect libmemcached

* Sun Feb 07 2010 Remi Collet <fedora@famillecollet.com> - 0.9-2
- rebuilt against new libmemcached

* Fri Jul 31 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.9-1
- Upstream released new version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.8-1
- Upstream released new version
- Enable libmemcached backend

* Mon Jun 22 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.7-1
- Upstream released new version

* Mon Jun 22 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.6-3
- Don't build with tcmalloc on sparc64

* Sun May 24 2009 Peter Lemenkov <lemenkov@gmail.com> 0.6-2
- Fixed issues, reported in https://bugzilla.redhat.com/show_bug.cgi?id=487148#c9

* Wed May 20 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.6-1
- Upstream released new version

* Mon Apr 27 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.5-1
- Upstream released new version
- Cleanups for review (bz #487148)

* Wed Feb 25 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.3-2
- Add init script

* Sat Feb 07 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.3-1
- Initial import

