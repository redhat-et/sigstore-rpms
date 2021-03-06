# Generated by go2rpm 1.6.0
%bcond_without check

# https://github.com/google/trillian
%global goipath         github.com/google/%{name}
Version:                1.4.0

%gometa

%global common_description %{expand:
A transparent, highly scalable and cryptographically verifiable data store.}

%global gobinaries      %{name}_log_server %{name}_log_signer
%global golicenses      LICENSE
%global godocs          docs examples CONTRIBUTING.md AUTHORS README.md\\\
                        CHANGELOG.md CONTRIBUTORS PULL_REQUEST_TEMPLATE.md\\\
                        extension/README.md integration/README.md\\\
                        experimental/batchmap/README.md quota/etcd/README.md\\\
                        deployment/README.md storage/README.md

Name:           trillian
Release:        1%{?dist}
Summary:        A transparent, highly scalable and cryptographically verifiable data store

# Upstream license specification: Apache-2.0
License:        ASL 2.0
URL:            %{gourl}
Source0:        %{gosource}
Source1:        %{name}_log_server.service
Source2:        %{name}_log_server.conf
Source3:        %{name}_log_signer.service
Source4:        %{name}_log_signer.conf
Requires:       mariadb-server

%if %{with check}
BuildRequires: golang(go.etcd.io/etcd/server/etcdserver/api/v3rpc)
%endif

BuildRequires:  systemd-rpm-macros

%description
%{common_description}

%gopkg

%prep
%goprep

%generate_buildrequires
%go_generate_buildrequires

%build
for f in %{gobinaries}; do
  %gobuild -o %{gobuilddir}/bin/$f %{goipath}/cmd/$f
done

%install
%gopkginstall
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/
install -m 0755 -vd                     %{buildroot}/%{_unitdir}
install -m 0644 -vp %{SOURCE1}          %{buildroot}%{_unitdir}
install -m 0755 -vd                     %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 -vp %{SOURCE2}          %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 -vp %{SOURCE3}          %{buildroot}%{_unitdir}
install -m 0644 -vp %{SOURCE4}          %{buildroot}%{_sysconfdir}/%{name}

%if %{with check}
%check
# Disabling tests that rely on a database server and a type mismatch error.
%gocheck -d client/rpcflags \
         -d experimental/batchmap \
         -d storage/testdb
%endif

%post
%systemd_post %{name}_log_server.service
%systemd_post %{name}_log_signer.service

%preun
%systemd_preun %{name}_log_server.service
%systemd_preun %{name}_log_signer.service

%postun
%systemd_postun %{name}_log_server.service
%systemd_postun %{name}_log_signer.service

%files
%license LICENSE
%doc docs examples CONTRIBUTING.md AUTHORS README.md CHANGELOG.md CONTRIBUTORS
%doc extension/README.md integration/README.md
%doc experimental/batchmap/README.md quota/etcd/README.md deployment/README.md
%doc storage/README.md
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/%{name}
%{_unitdir}/%{name}_log_server.service
%{_unitdir}/%{name}_log_signer.service
%gopkgfiles

%changelog
* Thu Apr 14 2022 Ivan Font <ifont@redhat.com> - 1.4.0-1
- Initial package
