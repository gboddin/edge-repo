%define commit daa4f1da5e34b274ca533766c5730696b1db7ca7 
Summary: Collection of Varnish Cache modules (VMODs) by Varnish Software
Name: varnish-modules
Version: 0.10.0
Release: 2%{?dist} 
Group: System Environment/Libraries
Packager: Edge Repo 
License: GPL 
Requires: varnish-libs >= 5.0
BuildRequires: autoconf, varnish-libs-devel >= 5.0
BuildRequires: python-docutils, libtool, make, gcc-c++
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
Source0:       https://github.com/varnish/varnish-modules/archive/%{commit}.tar.gz

%description
Collection of Varnish Cache 5.0 modules (VMODs) by Varnish Software
 - vmod_cookie
 - vmod_header
 - vmod_saintmode
 - vmod_softpurge
 - vmod_tcp
 - vmod_var
 - vmod_vsthrottle
 - vmod_xkey

%prep
%setup -q -n varnish-modules-%{commit}
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
%{_mandir}/man3/vmod_*
%{_libdir}/varnish/vmods/*.so
%{_docdir}/*


%clean

rm -rf $RPM_BUILD_ROOT
