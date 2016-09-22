%define		tag	RELEASE.2016-08-21T03-02-49Z
%define		subver	%(echo %{tag} | sed -e 's/[^0-9]//g')
Summary:	Minio Client: commands for filesystems and object storage
Name:		minio-mc
Version:	0.0.%{subver}
Release:	1
License:	Apache v2.0
Group:		Applications
Source0:	https://github.com/minio/mc/archive/%{tag}.tar.gz
# Source0-md5:	5d8c632198d83735966c62c38094544c
URL:		https://github.com/minio/mc
BuildRequires:	golang >= 1.3.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages 0
%define		gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%define		import_path	github.com/minio/mc

%description
Minio Client (mc) provides a modern alternative to UNIX commands like
ls, cat, cp, mirror, diff etc. It supports filesystems and Amazon S3
compatible cloud storage service (AWS Signature v2 and v4).

%prep
%setup -qc
mv mc-*/* .

install -d src/$(dirname %{import_path})
ln -s ../../.. src/%{import_path}

%build
export GOPATH=$(pwd)

%gobuild -o mc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -p mc $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md NOTICE
%attr(755,root,root) %{_bindir}/mc
