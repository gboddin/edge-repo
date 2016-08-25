Summary: Collection of Varnish Cache modules (VMODs) by Varnish Software
Name: varnish-modules
Version: 0.9.1 
Release: 1%{?dist} 
Group: System Environment/Libraries
Packager: Edge Repo 
License: GPL 
Requires: varnish-libs >= 4.1
BuildRequires: autoconf, varnish-libs-devel >= 4.1
BuildRequires: libtool, make, gcc-c++
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
Source0:       https://github.com/varnish/varnish-modules/archive/varnish-modules-%{version}.tar.gz
Patch0:        libtoolize-configure-fix.patch

%description
Collection of Varnish Cache 4.1 modules (VMODs) by Varnish Software
 - vmod_cookie
 - vmod_header
 - vmod_saintmode
 - vmod_softpurge
 - vmod_tcp
 - vmod_var
 - vmod_vsthrottle
 - vmod_xkey

%prep
%setup -q -n varnish-modules-varnish-modules-%{version}
%patch0 -p1
libtoolize -cfi 
[ ! -d m4 ] && mkdir m4
aclocal -I m4 -I $(pkg-config --variable=datarootdir varnishapi 2>/dev/null)/aclocal
autoheader
automake --add-missing --copy --foreign --force
autoconf
%configure

%build
make

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot}/%{_libdir}/ -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files 
%doc docs/* 
%{_libdir}/varnish/vmods/*.so
%{_docdir}/*

%clean

rm -rf $RPM_BUILD_ROOT
