Summary: Drupal 7 VMOD for Varnish
Name: varnish-vmod-drupal7
Version: 0.1
Release: 1%{?dist}
License: BSD
Group: System Environment/Daemons
Source0: https://git.kindwolf.org/libvmod-drupal7/tarball/4.0?file=varnish-vmod-drupal7.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: varnish >= 4.0.2
BuildRequires: make
BuildRequires: python-docutils
BuildRequires: varnish >= 4.0.2
BuildRequires: varnish-libs-devel >= 4.0.2

%description
Drupal 7 VMOD provides Drupal-related functions within Varnish.

%prep
%setup 

%build
%configure --prefix=/usr/
%{__make} %{?_smp_mflags}
%{__make} %{?_smp_mflags} check

%install
[ %{buildroot} != "/" ] && %{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

%clean
[ %{buildroot} != "/" ] && %{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_libdir}/varnis*/vmods/
%doc /usr/share/doc/lib%{name}/*
%doc LICENSE
%{_mandir}/man?/*

%changelog
* Wed Feb 04 2015 Xavier Guerrin <xavier@tuxfamily.org> - 0.1-0.20150204
- Initial version.
