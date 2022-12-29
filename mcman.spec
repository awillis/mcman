%define _mcman_root /usr/lib/mcman
%define _mcman_conf /etc/mcman

Name:       mcman
Version:    0.1.0
Release:    1%{?dist}
Summary:    Minecraft server instance manager.

License:    MIT
URL:        https://github.com/awillis/mcman
Source:     mcman-%{version}.tar.gz
BuildArch:  noarch
BuildRequires: python3-devel
BuildRequires: pyproject-rpm-macros
Requires: /usr/bin/java
Requires: /usr/bin/python3

%description


%prep
%autosetup

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files instance provider

%pre

%post

%systemd_post mcman

%preun

%systemd_preun mcman

%postun

%systemd_postun mcman

# TODO: create mcman user
# TODO: add mcman service to firewalld and enable permanent
# TODO: create systemd unit that supports multiple instances
# TODO: create python script that retrieves latest version of mcman, place under _mcman_root/<version>/server.jar
# TODO: create default mcman config file with version of server to use when creating new instances
# TODO: per instance directory is under /etc/mcman/instances/<name>, includes copy of mcman version config and server properties
# TODO: always fetch latest build version in python update script

%files -n python3-mcman -f %{pyproject_files}

%files
%attr(0755,mcman,mcman) %{_mcman_root}
%attr(0755,mcman,mcman) %{_mcman_root}/instance
%attr(0755,mcman,mcman) %{_mcman_root}/version
%attr(0644,root,root) %{_unitdir}/mcman@.service
%license add-license-file-here
%doc add-docs-here

%changelog
* Sun Dec 25 2022 Alan Willis
- Initial release
