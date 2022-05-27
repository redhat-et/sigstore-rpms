# Generated by go2rpm 1.6.0
%bcond_without check

# https://github.com/google/certificate-transparency-go
%global goipath         github.com/google/certificate-transparency-go
Version:                1.1.2

%gometa

%global common_description %{expand:
Auditing for TLS certificates (Go code).}

%global golicenses      LICENSE third_party/prometheus/LICENSE
%global godocs          CONTRIBUTING.md AUTHORS README.md CHANGELOG.md\\\
                        CONTRIBUTORS PULL_REQUEST_TEMPLATE.md\\\
                        trillian/README.md trillian/migrillian/README.md\\\
                        gossip/README.md asn1/README.md x509/README.md

Name:           trillian-certificate-transparency-server
Release:        1%{?dist}
Summary:        Auditing for TLS certificates (Go code)

# Upstream license specification: Apache-2.0
License:        ASL 2.0
URL:            %{gourl}
Source0:        %{gosource}

%description
%{common_description}

%gopkg

%prep
%goprep

%generate_buildrequires
%go_generate_buildrequires

%build
for cmd in trillian/ctfe/ct_server; do
  %gobuild -o %{gobuilddir}/bin/$(basename $cmd) %{goipath}/$cmd
done

%install
%gopkginstall
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/

%if %{with check}
%check
%gocheck
%endif

%files
%license LICENSE third_party/prometheus/LICENSE
%doc CONTRIBUTING.md AUTHORS README.md CHANGELOG.md CONTRIBUTORS
%doc PULL_REQUEST_TEMPLATE.md trillian/README.md
%doc trillian/migrillian/README.md gossip/README.md asn1/README.md
%doc x509/README.md
%{_bindir}/*

%gopkgfiles

%changelog
* Tue Apr 26 2022 Ivan Font <ifont@redhat.com> - 1.1.2-1
- Initial package
