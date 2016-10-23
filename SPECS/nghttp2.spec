Summary: Experimental HTTP/2 client, server and proxy
Name: nghttp2
Version: 1.15.0
Release: 1%{?dist}
License: MIT
Group: Applications/Internet
URL: https://nghttp2.org/
Source0: https://github.com/tatsuhiro-t/nghttp2/releases/download/v%{version}/nghttp2-%{version}.tar.xz

# prevent nghttpx from crashing on armv7hl (#1358845)

BuildRequires: CUnit-devel
BuildRequires: libev-devel
BuildRequires: openssl-devel
BuildRequires: zlib-devel

Requires: libnghttp2%{?_isa} = %{version}-%{release}

%description
This package contains the HTTP/2 client, server and proxy programs.


%package -n libnghttp2
Summary: A library implementing the HTTP/2 protocol
Group: Development/Libraries

%description -n libnghttp2
libnghttp2 is a library implementing the Hypertext Transfer Protocol
version 2 (HTTP/2) protocol in C.


%package -n libnghttp2-devel
Summary: Files needed for building applications with libnghttp2
Group: Development/Libraries
Requires: libnghttp2%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description -n libnghttp2-devel
The libnghttp2-devel package includes libraries and header files needed
for building applications with libnghttp2.


%prep
%setup -q


%build
%configure                                  \
    --disable-python-bindings               \
    --disable-static                        \
    --without-libxml2                       \
    --without-spdylay

# avoid using rpath
sed -i libtool                              \
    -e 's/^runpath_var=.*/runpath_var=/'    \
    -e 's/^hardcode_libdir_flag_spec=".*"$/hardcode_libdir_flag_spec=""/'

make %{?_smp_mflags} V=1


%install
%make_install

# not needed on Fedora/RHEL
rm -f "$RPM_BUILD_ROOT%{_libdir}/libnghttp2.la"

# will be installed via %%doc
rm -f "$RPM_BUILD_ROOT%{_datadir}/doc/nghttp2/README.rst"

%post -n libnghttp2 -p /sbin/ldconfig

%postun -n libnghttp2 -p /sbin/ldconfig


%check
# test the just built library instead of the system one, without using rpath
export "LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}:$LD_LIBRARY_PATH"
make %{?_smp_mflags} check


%files
%{_bindir}/h2load
%{_bindir}/nghttp
%{_bindir}/nghttpd
%{_bindir}/nghttpx
%{_datadir}/nghttp2
%{_mandir}/man1/h2load.1*
%{_mandir}/man1/nghttp.1*
%{_mandir}/man1/nghttpd.1*
%{_mandir}/man1/nghttpx.1*

%files -n libnghttp2
%{_libdir}/libnghttp2.so.*
%{!?_licensedir:%global license %%doc}
%license COPYING

%files -n libnghttp2-devel
%{_includedir}/nghttp2
%{_libdir}/pkgconfig/libnghttp2.pc
%{_libdir}/libnghttp2.so
%doc README.rst


%changelog
* Mon Sep 26 2016 Kamil Dudka <kdudka@redhat.com> 1.15.0-1
- update to the latest upstream release

* Mon Sep 12 2016 Kamil Dudka <kdudka@redhat.com> 1.14.1-1
- update to the latest upstream release

* Thu Aug 25 2016 Kamil Dudka <kdudka@redhat.com> 1.14.0-1
- update to the latest upstream release

* Tue Jul 26 2016 Kamil Dudka <kdudka@redhat.com> 1.13.0-2
- prevent nghttpx from crashing on armv7hl (#1358845)

* Thu Jul 21 2016 Kamil Dudka <kdudka@redhat.com> 1.13.0-1
- update to the latest upstream release

* Mon Jun 27 2016 Kamil Dudka <kdudka@redhat.com> 1.12.0-1
- update to the latest upstream release

* Sun May 29 2016 Kamil Dudka <kdudka@redhat.com> 1.11.1-1
- update to the latest upstream release

* Thu May 26 2016 Kamil Dudka <kdudka@redhat.com> 1.11.0-1
- update to the latest upstream release

* Mon Apr 25 2016 Kamil Dudka <kdudka@redhat.com> 1.10.0-1
- update to the latest upstream release

* Sun Apr 03 2016 Kamil Dudka <kdudka@redhat.com> 1.9.2-1
- update to the latest upstream release

* Tue Mar 29 2016 Kamil Dudka <kdudka@redhat.com> 1.9.1-1
- update to the latest upstream release

* Thu Feb 25 2016 Kamil Dudka <kdudka@redhat.com> 1.8.0-1
- update to the latest upstream release

* Thu Feb 11 2016 Kamil Dudka <kdudka@redhat.com> 1.7.1-1
- update to the latest upstream release (fixes CVE-2016-1544)

* Fri Feb 05 2016 Kamil Dudka <kdudka@redhat.com> 1.7.0-3
- make the package compile with gcc-6

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Kamil Dudka <kdudka@redhat.com> 1.7.0-1
- update to the latest upstream release

* Fri Dec 25 2015 Kamil Dudka <kdudka@redhat.com> 1.6.0-1
- update to the latest upstream release (fixes CVE-2015-8659)

* Thu Nov 26 2015 Kamil Dudka <kdudka@redhat.com> 1.5.0-1
- update to the latest upstream release

* Mon Oct 26 2015 Kamil Dudka <kdudka@redhat.com> 1.4.0-1
- update to the latest upstream release

* Thu Sep 24 2015 Kamil Dudka <kdudka@redhat.com> 1.3.4-1
- update to the latest upstream release

* Wed Sep 23 2015 Kamil Dudka <kdudka@redhat.com> 1.3.3-1
- update to the latest upstream release

* Wed Sep 16 2015 Kamil Dudka <kdudka@redhat.com> 1.3.2-1
- update to the latest upstream release

* Mon Sep 14 2015 Kamil Dudka <kdudka@redhat.com> 1.3.1-1
- update to the latest upstream release

* Mon Aug 31 2015 Kamil Dudka <kdudka@redhat.com> 1.3.0-1
- update to the latest upstream release

* Mon Aug 17 2015 Kamil Dudka <kdudka@redhat.com> 1.2.1-1
- update to the latest upstream release

* Sun Aug 09 2015 Kamil Dudka <kdudka@redhat.com> 1.2.0-1
- update to the latest upstream release

* Wed Jul 15 2015 Kamil Dudka <kdudka@redhat.com> 1.1.1-1
- update to the latest upstream release

* Tue Jun 30 2015 Kamil Dudka <kdudka@redhat.com> 1.0.5-1
- packaged for Fedora (#1237247)
