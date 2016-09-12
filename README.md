# RPM Edge Repository
 
## Introduction

### Goal

This repository is meant for people wanting to use the lastest version of software mainly in LAMP environment. 

### Who are we

Tired sysadmins not hoping for their **** datacenter to upgrade their OS anytime soon.

### Why

Because no repo is currently building publicly on travis-ci for 4 major linux distribution.

#### Redhat/Centos/SL/Oracle Linux 6 :

```rpm -ivh http://repo.siwhine.net/el/6/edge-repo-latest.rpm```

#### Redhat/Centos/SL/Oracle Linux 7 :

```rpm -ivh http://repo.siwhine.net/el/7/edge-repo-latest.rpm```

#### Fedora 23 :

```rpm -ivh http://repo.siwhine.net/fedora/23/edge-repo-latest.rpm```

#### Fedora 24 :

```rpm -ivh http://repo.siwhine.net/fedora/24/edge-repo-latest.rpm```

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
* Proot for providing an user-space alternative to chroot and making RPMs distributions possible on travis-ci. [proot project](https://github.com/proot-me/PRoot)
* All of CentOS developers [CentOS website](https://www.centos.org/)
* The Fedora developers for taking care of backporting in their spec files [Fedora website](https://getfedora.org/)
* Remirepo for the php spec file [Remirepo blog](https://blog.remirepo.net/)
* All other open-source projects involved
* Oracle, for screwing up the 1 closed-source RPM we use from them [Oracle site](http://eelslap.com/)

## Website

https://edge.siwhine.net
