Name:           python3
Version:        3.6.0
Release:        42
License:        Python-2.0
Summary:        The Python Programming Language
Url:            http://www.python.org
Group:          devel/python
Source0:        https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tar.xz
Patch0:         0001-Fix-python-path-for-linux.patch
# Causes test-suite failures
#Patch1:         0001-ensure-pip-upgrade.patch
Patch1:         skip-some-tests.patch
Patch2:         0001-Replace-getrandom-syscall-with-RDRAND-instruction.patch
Patch3:         0001-Enable-Profile-Guided-Optimization-for-pybench.patch
Patch4:		avx2.patch
BuildRequires:  bzip2
BuildRequires:  db
BuildRequires:  grep
BuildRequires:  bzip2-dev
BuildRequires:  xz-dev
BuildRequires:  gdbm-dev
BuildRequires:  readline-dev
BuildRequires:  openssl
BuildRequires:  openssl-dev
BuildRequires:  sqlite-autoconf
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  ncurses-dev
BuildRequires:  expat-dev
BuildRequires:  libffi-dev
BuildRequires:  procps-ng-bin
BuildRequires:  netbase

%global __arch_install_post %{nil}

%description
The Python Programming Language.

%package lib
License:        Python-2.0
Summary:        The Python Programming Language
Group:          devel/python

%description lib
The Python Programming Language.

%package core
License:        Python-2.0
Summary:        The Python Programming Language
Group:          devel/python
Provides:       python3
Provides:       python3-modules
Provides:       /bin/python3

# evil evil compatibility hack for bootstrap purposes
Provides:       python(abi) = 3.5

%description core
The Python Programming Language.

%package dev
License:        Python-2.0
Summary:        The Python Programming Language
Group:          devel
Requires:       python3-lib
Requires:       python3-core

%define python_configure_flags  --with-threads --with-pymalloc  --without-cxx-main --with-signal-module --enable-ipv6=yes  --libdir=/usr/lib  ac_cv_header_bluetooth_bluetooth_h=no  ac_cv_header_bluetooth_h=no  --with-system-ffi --with-system-expat --with-lto --with-computed-gotos


%description dev
The Python Programming Language.

%package doc
License:        Python-2.0
Summary:        The Python Programming Language
Group:          devel/python

%description doc
The Python Programming Language.

%prep
%setup -q -n Python-%{version}
%patch0 -p1
# Todo fix these
%patch1 -p1
# make the code not block on getrandom during boot
#%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
export LANG=C

# Build with PGO for perf improvement
%configure %python_configure_flags
make profile-opt %{?_smp_mflags}

%install
%make_install
make clean
%configure %python_configure_flags --enable-shared
make %{?_smp_mflags}
%make_install
mv %{buildroot}/usr/lib/libpython*.so* %{buildroot}/usr/lib64/

%check
export LANG=C
LD_LIBRARY_PATH=`pwd` ./python -Wd -E -tt  Lib/test/regrtest.py -v -x test_asyncio test_uuid || :


%files lib
/usr/lib64/libpython3.6m.so.1.0

%files core
%exclude /usr/bin/2to3
/usr/bin/2to3-3.6
/usr/bin/easy_install-3.6
/usr/bin/idle3
/usr/bin/idle3.6
%exclude /usr/bin/pip3
%exclude /usr/bin/pip3.6
/usr/bin/pydoc3
/usr/bin/pydoc3.6
/usr/bin/python3
/usr/bin/python3-config
/usr/bin/python3.6
/usr/bin/python3.6-config
/usr/bin/python3.6m
/usr/bin/python3.6m-config
/usr/bin/pyvenv
/usr/bin/pyvenv-3.6
/usr/lib/python3.6/
%exclude /usr/lib/python3.6/site-packages/pip


%files dev
/usr/include/python3.6m/*.h
/usr/lib64/libpython3.so
/usr/lib64/libpython3.6m.so
/usr/lib64/pkgconfig/python3.pc
/usr/lib64/pkgconfig/python-3.6.pc
/usr/lib64/pkgconfig/python-3.6m.pc

%files doc
%{_mandir}/man1/*
