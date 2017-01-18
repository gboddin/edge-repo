# RPM Edge Repository
 
## Introduction

### WARNING

Some of the packages are compiled with custom patches suiting the author's need. We'll provide a list of those in the future, but they mainly contains license changes and small improvement/tweaks.

Since this repo is customized and usually won't accept external changes, I suggest looking at the well supported [IUSCommunity](iuscommunity.org) packages. Most of our packages are imported from IUS.

### Goal

This repository is meant for people wanting to use the lastest version of software mainly in LAMP environment. 

### Who are we

Tired sysadmins not hoping for their **** datacenter to upgrade their OS anytime soon.

### Why

Because no repo is currently building publicly on travis-ci for EL distributions.

#### Redhat/Centos/SL/Oracle Linux 6 :

```rpm -ivh http://repo.siwhine.net/el/6/edge-repo-latest.rpm```

#### Redhat/Centos/SL/Oracle Linux 7 :

```rpm -ivh http://repo.siwhine.net/el/7/edge-repo-latest.rpm```

## GPG

The GPG key is available here : http://repo.siwhine.net/EDGE-REPO-KEY.pub

## Updates

This repository is directly connected to the repo. Once the compilations are successful, the RPMs are automatically deployed to the repository.
The compilations are triggered on travis-ci by branch name.

## Contribution

Any pull-request is welcome just make sure you pick the right branch to work on.

## Addition

We won't add software on request, but feel free to add it yourself by creating a PR.

## License

All hosted software remain in their original license. This repository itself and its scripts are under GPLv3 licence.

## Thanks and credits

* travis-ci for offering free build for opensource projects. [travis-ci website](https://travis-ci.org)
* All of CentOS developers [CentOS website](https://www.centos.org/)
* The Fedora developers for taking care of backporting in their spec files [Fedora website](https://getfedora.org/)
* [IUSCommunity](iuscommunity.org) / Rackspace
* Remirepo for the php spec file [Remirepo blog](https://blog.remirepo.net/)
* Docker [Docker](https://www.docker.com/)
* All other open-source projects involved
* Oracle, for screwing up the 1 closed-source RPM we use from them [Oracle site](http://eelslap.com/)
