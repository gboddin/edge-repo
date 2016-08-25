Name:           edge-release
Version:        24
Release:        4%{?dist} 
Summary:        Edge Packages for Fedora Linux repository configuration

Group:          System Environment/Base
License:        GPLv2

# This is a Edge maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.
URL:            https://github.com/gboddin/el6-lamp-stack 
Source0:        https://repo.siwhine.net/EDGE-REPO-KEY.pub
Source1:        https://repo.siwhine.net/fedora/24.repo
Source2:        https://www.gnu.org/licenses/gpl.txt

BuildArch:     noarch
Requires:      fedora-release >=  %{version}

%description
This package contains the Edge Packages for Fedora Linux (Edge) repository
GPG key as well as configuration for yum.

%prep
%setup -q  -c -T
install -pm 644 %{SOURCE0} .
install -pm 644 %{SOURCE1} .
install -pm 644 %{SOURCE2} .

%build


%install
rm -rf $RPM_BUILD_ROOT

#GPG Key
install -Dpm 644 %{SOURCE0} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/EDGE-REPO-KEY

# yum
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE1}  \
    $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/edge.repo

%post
rpm --import %{_sysconfdir}/pki/rpm-gpg/EDGE-REPO-KEY

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc gpl.txt 
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/*

%changelog
* Mon Aug 22 2016 Gregory Boddin <gregory@siwhine.net> - 24-1
- Created package for easy install on Fedora
 
* Mon Aug 22 2016 Gregory Boddin <gregory@siwhine.net> - 7-1
- Created package for easy install on RHELs
 
* Mon Dec 16 2013 Dennis Gilmore <dennis@ausil.us> - 7-0.1
- initial epel 7 build. 

