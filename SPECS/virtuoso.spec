#
# spec file for virtuoso-opensource
#
Summary: Virtuoso Opensource Server
Name: virtuoso-opensource
Version: 7.2.4.2
Release: 1%{?dist}
# see LICENSE for exception details
License: GPLv2 with exceptions
Group: Applications/Databases
Source0: http://prdownloads.sourceforge.net/virtuoso/%{name}-%{version}.tar.gz
URL: http://virtuoso.sourceforge.net
Distribution: CentOS
Vendor: OpenLink Software, Inc.
Packager: Bade Iriabho

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: flex
BuildRequires: net-tools
BuildRequires: bison
BuildRequires: gperf
BuildRequires: gawk
#BuildRequires: htmldoc
BuildRequires: openssl-devel
BuildRequires: readline-devel
BuildRequires: openldap-devel
BuildRequires: libiodbc-devel
BuildRequires: libxml2-devel
BuildRequires: zlib-devel
BuildRequires: automake libtool

Provides: %{name} = %{version}-%{release}

%description
Virtuoso is a middleware and database engine hybrid that combines
the functionality of a traditional RDBMS, ORDBMS,
virtual database, RDF, XML, free-text, web application
server and file server functionality in a single system.

%package drivers
Summary: Virtuoso ODBC Driver
Group:   Applications/Databases
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
%description drivers
%{summary}.

%package doc
Summary: Documentation
Group:   Documentation
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
BuildArch: noarch
%description doc
%{summary}.

%prep
%setup

%build
export CFLAGS="-O2 -m64"
%configure  \
   --prefix=/var/lib/ \
   --enable-shared --disable-static \
   --with-readline \
   --with-debug \
   --enable-openssl \
   --disable-imagemagick \
   --program-transform-name="s/isql/isql-v/" \
   --with-layout=RedHat

make %{?_smp_mflags}

# fix for document html
touch %{_builddir}/%{name}-%{version}/docsrc/html_virt/test.html

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/virtuoso
mv %{buildroot}%{_var}/lib/virtuoso/db/virtuoso.ini %{buildroot}%{_sysconfdir}/virtuoso/
ln -s ../../../..%{_sysconfdir}/virtuoso/virtuoso.ini %{buildroot}%{_var}/lib/virtuoso/db/virtuoso.ini

# generic'ish binaries, hide them away safely
mkdir -p %{buildroot}%{_libexecdir}/virtuoso/
mv %{buildroot}%{_bindir}/{inifile,isql-v,isql-vw} \
   %{buildroot}%{_libexecdir}/virtuoso/

## unpackaged files
rm -vf %{buildroot}%{_libdir}/*.{la,a}
rm -vf %{buildroot}%{_libdir}/virtuoso/hosting/*.la
rm -vf  %{buildroot}%{_libdir}/{hibernate,jdbc-?.?,jena,jena2}/*.jar
rm -rvf %{buildroot}%{_libdir}/sesame

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING CREDITS LICENSE
%dir %{_sysconfdir}/virtuoso/
%config(noreplace) %{_sysconfdir}/virtuoso/virtuoso.ini
%{_bindir}/virtuoso-t
%dir %{_datadir}/virtuoso/
%dir %{_datadir}/virtuoso/vad/
#%dir %{_libdir}/virtuoso/
%dir %{_libexecdir}/virtuoso/
%dir %{_var}/lib/virtuoso
#%{_libdir}/virtuoso/hosting/
%{_libexecdir}/virtuoso/*
%{_datadir}/virtuoso/vad/*.vad
%{_var}/lib/virtuoso/db/
%{_var}/lib/virtuoso/vsp/
%{_bindir}/virt_mail

%files drivers
%defattr(-,root,root,-)
%{_libdir}/virt*.so

%files doc
%defattr(-,root,root,-)
%{_docdir}/virtuoso/

%changelog
