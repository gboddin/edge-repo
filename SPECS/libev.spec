Name:             libev
Summary:          High-performance event loop/event model with lots of features
Group: Applications/Internet
Version:          4.22
Release:          1%{?dist}
License:          BSD or GPLv2+
URL:              http://software.schmorp.de/pkg/libev.html
Source0:          http://dist.schmorp.de/libev/Attic/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:    autoconf
BuildRequires:    automake
BuildRequires:    coreutils
BuildRequires:    findutils
BuildRequires:    gcc
BuildRequires:    libtool
BuildRequires:    make
BuildRequires:    tar

Provides:         bundled(libecb) = 1.05

%description
Libev is modeled (very loosely) after libevent and the Event Perl
module, but is faster, scales better and is more correct, and also more
featureful. And also smaller.


%package devel
Group: Development/Libraries
Summary:          Development headers for libev
Requires:         %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development headers and libraries for libev.


%package libevent-devel
Group: Development/Libraries
Summary:          Compatibility development header with libevent for %{name}.
Requires:         %{name}-devel%{?_isa} = %{version}-%{release}

# The event.h file actually conflicts with the one from libevent-devel
Conflicts:        libevent-devel

%description libevent-devel
This package contains a development header to make libev compatible with
libevent.

%prep
%setup -q 
autoreconf -vfi

%build
%configure --disable-static --with-pic
make %{?_smp_mflags}

%check
make check

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -rf %{buildroot}%{_libdir}/%{name}.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc LICENSE Changes README
%{_libdir}/%{name}.so.4
%{_libdir}/%{name}.so.4.0.0

%files devel
%{_includedir}/ev++.h
%{_includedir}/ev.h
%{_libdir}/%{name}.so
%{_mandir}/man?/*

%files libevent-devel
%{_includedir}/event.h

%changelog
* Mon Mar 28 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 4.22-1
- Update to 4.22 (RHBZ #1234039)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Oct 17 2015  Fabian Affolter <mail@fabian-.affolter.ch> - 4.20-2
- Remove patch

* Sat Jun 20 2015 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 4.20-1
- Update to 4.20 (#1234039)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Sep 29 2014 Mathieu Bridon <bochecha@fedoraproject.org> - 4.19-1
- Update to 4.19.

* Tue Sep 23 2014 Mathieu Bridon <bochecha@fedoraproject.org> - 4.18-2
- Fix C++ function definitions
  https://bugzilla.redhat.com/show_bug.cgi?id=1145190

* Mon Sep 08 2014 Mathieu Bridon <bochecha@fedoraproject.org> - 4.18-1
- Update to 4.18.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov 26 2013 Mathieu Bridon <bochecha@fedoraproject.org> - 4.15-3
- Get the package closer to what upstream intended:
  - Do not move the headers into a subfolder of /usr/include
  - Make a libev-libevent-devel subpackage to contain the libevent
    compatibility header, so that only this subpackage conflicts with
    libevent-devel, not all of libev-devel
  - Drop the pkgconfig file, as upstream rejected it several times already.

* Sun Sep  8 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 4.15-2
- Bump (koji was broken)

* Sun Sep  8 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 4.15-1
- Update to 4.15 (rhbz 987489)
- Fix dates in spec

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 08 2013 Mathieu Bridon <bochecha@fedoraproject.org> - 4.11-2
- Make a patch out of Michal's pkgconfig support.
- Modernize the configure.ac file for Automake >= 1.13.
- Respect the Fedora CFLAGS
  https://bugzilla.redhat.com/show_bug.cgi?id=908096

* Fri Sep 28 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 4.11-1
- Update to 4.11

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug  9 2011 Tom Callaway <spot@fedoraproject.org> - 4.04-1
- move man page
- cleanup spec
- update to 4.04

* Mon Jun 13 2011 Matěj Cepl <mcepl@redhat.com> - 4.03-2
- EL5 cannot have noarch subpackages.

* Mon Jan 10 2011 Michal Nowak <mnowak@redhat.com> - 4.01-1
- 4.01
- fix grammar in %%description

* Sat Jan  2 2010 Michal Nowak <mnowak@redhat.com> - 3.90-1
- 3.9

* Mon Aug 10 2009 Michal Nowak <mnowak@redhat.com> - 3.80-1
- 3.8
- always use the most recent automake
- BuildRequires now libtool

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.70-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Michal Nowak <mnowak@redhat.com> - 3.70-2
- spec file change, which prevented uploading most recent tarball
  so the RPM was "3.70" but tarball was from 3.60

* Fri Jul 17 2009 Michal Nowak <mnowak@redhat.com> - 3.70-1
- v3.7
- list libev soname explicitly

* Mon Jun 29 2009 Michal Nowak <mnowak@redhat.com> - 3.60-1
- previous version was called "3.6" but this is broken update
  path wrt version "3.53" -- thus bumping to "3.60"

* Thu Apr 30 2009 Michal Nowak <mnowak@redhat.com> - 3.6-1
- 3.60
- fixed few mixed-use-of-spaces-and-tabs warnings in spec file

* Thu Mar 19 2009 Michal Nowak <mnowak@redhat.com> - 3.53-1
- 3.53

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 07 2009 Michal Nowak <mnowak@redhat.com> - 3.52-1
- 3.52

* Wed Dec 24 2008 Michal Nowak <mnowak@redhat.com> - 3.51-1
- 3.51

* Thu Nov 20 2008 Michal Nowak <mnowak@redhat.com> - 3.49-1
- version bump: 3.49

* Sun Nov  9 2008 Michal Nowak <mnowak@redhat.com> - 3.48-1
- version bump: 3.48

* Mon Oct  6 2008 kwizart <kwizart at gmail.com> - 3.44-1
- bump to 3.44

* Tue Sep  2 2008 kwizart <kwizart at gmail.com> - 3.43-4
- Fix pkgconfig support

* Tue Aug 12 2008 Michal Nowak <mnowak@redhat.com> - 3.43-2
- removed libev.a
- installing with "-p"
- event.h is removed intentionaly, because is there only for 
  backward compatibility with libevent

* Mon Aug 04 2008 Michal Nowak <mnowak@redhat.com> - 3.43-1
- initial package

