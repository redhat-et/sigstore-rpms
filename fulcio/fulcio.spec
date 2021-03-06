# Generated by go2rpm 1.6.0
%bcond_without check

# https://github.com/sigstore/fulcio
%global goipath         github.com/sigstore/%{name}
Version:                0.4.0

%gometa

%global common_description %{expand:
Sigstore OIDC PKI.}

%global golicenses      COPYRIGHT.txt LICENSE
%global godocs          docs examples DEPRECATIONS.md CODE_OF_CONDUCT.md\\\
                        FEATURES.md README.md CHANGELOG.md\\\
                        federation/README.md release/README.md config/aws-\\\
                        cloudhsm.md config/README.md config/DEVELOPMENT.md\\\
                        tools/loadtest/requirements.txt\\\
                        tools/loadtest/README.md

Name:           fulcio
Release:        1%{?dist}
Summary:        Sigstore OIDC PKI

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
for cmd in cmd/* ; do
  %gobuild -o %{gobuilddir}/bin/$(basename $cmd) %{goipath}/$cmd
done
%gobuild -o %{gobuilddir}/bin/fulcio %{goipath}
for cmd in federation; do
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
%license COPYRIGHT.txt LICENSE
%doc docs examples DEPRECATIONS.md CODE_OF_CONDUCT.md FEATURES.md README.md
%doc CHANGELOG.md federation/README.md release/README.md config/aws-cloudhsm.md
%doc config/README.md config/DEVELOPMENT.md tools/loadtest/requirements.txt
%doc tools/loadtest/README.md
%{_bindir}/*

%gopkgfiles

%changelog
* Tue Apr 26 2022 Ivan Font <ifont@redhat.com> - 0.4.0-1
- Initial package
