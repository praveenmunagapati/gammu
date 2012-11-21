Name:               gammu
Version:            1.32.90
Release:            1
# Set to 0 to disable bluetooth support
%if 0%{?opensuse_bs} && 0%{?sles_version} == 9
%define bluetooth   0
%else
%define bluetooth   1
%endif
# Set to 0 to disable PostgreSQL support
%define pqsql     1
# Set to 0 to disable MySQL support
%define mysql     1
# Set to 0 to disable DBI support
%define dbi       1
# Set to 0 to disable ODBC support
%define odbc      1
# Set to 0 to disable USB support
%define usb       1
# Change if using tar.gz sources
%define extension   bz2

# Python name
%{!?__python: %define __python python}
%define g_python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%define g_python_major_version %(%{__python} -c 'import sys; print sys.version.split(" ")[0][:3]')

%if 0%{?fedora_version} || 0%{?centos_version} || 0%{?rhel_version} || 0%{?fedora} || 0%{?rhel}
%define gammu_docdir %_docdir/%{name}-%{version}
%else
%define gammu_docdir %_docdir/%{name}
%endif

Summary:            Mobile phone management utility
License:            GPLv2
%if 0%{?suse_version}
Group:              Hardware/Mobile
%else
Group:              Applications/Communications
%endif
Vendor:         Michal Čihař <michal@cihar.com>

# Detect build requires, I really hate this crap

# SUSE
%if 0%{?suse_version}

%define dist_usb_libs libusb-1_0-devel
%define dist_dbi_libs libdbi-devel libdbi-drivers-dbd-sqlite3 sqlite

# 11.1 changed name of devel package for Bluetooth
%if 0%{?suse_version} >= 1110
%define dist_bluez_libs bluez-devel
%else
%define dist_bluez_libs bluez-libs >= 2.0
%endif

%define dist_postgres_libs postgresql-devel

%else

# Mandriva
%if 0%{?mandriva_version}

%define dist_usb_libs libusb-1.0-devel
%define dist_dbi_libs libdbi-devel libdbi-drivers-dbd-sqlite3 sqlite3-tools

# 64-bit Mandriva has 64 in package name
%ifarch x86_64
%define mandriva_hack 64
%endif

# Bluetooth things got renamed several times
%if 0%{?mandriva_version} > 2007
%define dist_bluez_libs lib%{?mandriva_hack}bluez-devel
%else
%if 0%{?mandriva_version} > 2006
%define dist_bluez_libs lib%{?mandriva_hack}bluez2-devel
%else
%define dist_bluez_libs libbluez1-devel >= 2.0
%endif
%endif

# postgresql-devel does not work for whatever reason in buildservice
%if 0%{?mandriva_version} == 2009
%define dist_postgres_libs postgresql8.3-devel
%else
%define dist_postgres_libs postgresql-devel
%endif

%else

# Fedora / Redhat / Centos
%if 0%{?fedora_version} || 0%{?centos_version} || 0%{?rhel_version} || 0%{?fedora} || 0%{?rhel}

%define dist_usb_libs libusb1-devel
%define dist_dbi_libs libdbi-devel libdbi-dbd-sqlite sqlite
%define dist_bluez_libs bluez-libs-devel >= 2.0
%define dist_postgres_libs postgresql-devel

%else

#Defaults for not know distributions
%define dist_usb_libs libusb1-devel
%define dist_dbi_libs libdbi-devel libdbi-dbd-sqlite sqlite
%define dist_bluez_libs bluez-libs-devel >= 2.0
%define dist_postgres_libs postgresql-devel

%endif
%endif
%endif

%if %bluetooth
BuildRequires: %{dist_bluez_libs}
%endif

%if %pqsql
BuildRequires: %{dist_postgres_libs}
%endif

%if %mysql
BuildRequires: mysql-devel
%endif

%if %dbi
BuildRequires: %{dist_dbi_libs}
%endif

%if %odbc
BuildRequires: unixODBC-devel
%endif

%if 0%{?fedora_version} || 0%{?centos_version} || 0%{?rhel_version} || 0%{?fedora} || 0%{?rhel}
BuildRequires: libgudev1-devel glib2-devel
%else
%if 0%{?mandriva_version}
BuildRequires: libgudev1.0-devel glib2-devel
%else
BuildRequires: libgudev-1_0-devel glib2-devel
%endif
%endif

BuildRequires: python-devel

%if 0%{?centos_version} || 0%{?rhel_version} || 0%{?rhel} || 0%{?suse_version} < 1100
BuildRequires: curl-devel
%else
BuildRequires: libcurl-devel
%endif

%if %usb
BuildRequires: %{dist_usb_libs}
%endif

BuildRequires: gettext cmake pkgconfig gcc

Source:         http://dl.cihar.com/gammu/releases/gammu-%{version}.tar.%{extension}
URL:            http://wammu.eu/gammu/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Gammu is command line utility and library to work with mobile phones
from many vendors. Support for different models differs, but basic
functions should work with majority of them. Program can work with
contacts, messages (SMS, EMS and MMS), calendar, todos, filesystem,
integrated radio, camera, etc. It also supports daemon mode to send and
receive SMSes.

Currently supported phones include:

* Many Nokia models.
* Alcatel BE5 (501/701), BF5 (715), BH4 (535/735).
* AT capable phones (Siemens, Nokia, Alcatel, IPAQ).
* OBEX and IrMC capable phones (Sony-Ericsson, Motorola).
* Symbian phones through gnapplet.

This package contains Gammu binary as well as some examples.

%package devel
License:      GPL v2
Summary:      Development files for Gammu
%if 0%{?suse_version}
Group:              Development/Libraries/C and C++
%else
Group:              Development/Libraries
%endif
Requires:           %{name} = %{version}-%{release} pkgconfig

%description devel
Gammu is command line utility and library to work with mobile phones
from many vendors. Support for different models differs, but basic
functions should work with majority of them. Program can work with
contacts, messages (SMS, EMS and MMS), calendar, todos, filesystem,
integrated radio, camera, etc. It also supports daemon mode to send and
receive SMSes.

Currently supported phones include:

* Many Nokia models.
* Alcatel BE5 (501/701), BF5 (715), BH4 (535/735).
* AT capable phones (Siemens, Nokia, Alcatel, IPAQ).
* OBEX and IrMC capable phones (Sony-Ericsson, Motorola).
* Symbian phones through gnapplet.

This package contain files needed for development.

%package -n python-gammu
License:    GPL v2
Summary:    Python module to communicate with mobile phones
%if 0%{?suse_version}
Group:      Development/Libraries/Python
%else
Group:      Development/Languages
%endif
Requires: python >= %{g_python_major_version}, python < %{g_python_major_version}.99
%{?py_requires}

%description -n python-gammu
This provides gammu module, that can work with any phone Gammu
supports - many Nokias, Siemens, Alcatel, ...

%package smsd
Summary:    SMS message daemon
%if 0%{?suse_version}
PreReq: %insserv_prereq  %fillup_prereq
%endif
%if 0%{?fedora_version} || 0%{?centos_version} || 0%{?rhel_version} || 0%{?fedora} || 0%{?rhel}
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
%endif
%if 0%{?suse_version}
Group:              Hardware/Mobile
%else
Group:              Applications/Communications
%endif

%description smsd
Gammu is command line utility and library to work with mobile phones
from many vendors. Support for different models differs, but basic
functions should work with majority of them. Program can work with
contacts, messages (SMS, EMS and MMS), calendar, todos, filesystem,
integrated radio, camera, etc. It also supports daemon mode to send and
receive SMSes.

Currently supported phones include:

* Many Nokia models.
* Alcatel BE5 (501/701), BF5 (715), BH4 (535/735).
* AT capable phones (Siemens, Nokia, Alcatel, IPAQ).
* OBEX and IrMC capable phones (Sony-Ericsson, Motorola).
* Symbian phones through gnapplet.

This package contains Gammu SMS Daemon and tool to inject messages 
into the queue.

%package -n libGammu7
Summary:    Mobile phone management library
Group:      System/Libraries

%description -n libGammu7
Gammu is command line utility and library to work with mobile phones
from many vendors. Support for different models differs, but basic
functions should work with majority of them. Program can work with
contacts, messages (SMS, EMS and MMS), calendar, todos, filesystem,
integrated radio, camera, etc. It also supports daemon mode to send and
receive SMSes.

Currently supported phones include:

* Many Nokia models.
* Alcatel BE5 (501/701), BF5 (715), BH4 (535/735).
* AT capable phones (Siemens, Nokia, Alcatel, IPAQ).
* OBEX and IrMC capable phones (Sony-Ericsson, Motorola).
* Symbian phones through gnapplet.

This package contains Gammu shared library.

%package -n libgsmsd7
Summary:    SMS daemon helper library
Group:      System/Libraries

%description -n libgsmsd7
Gammu is command line utility and library to work with mobile phones
from many vendors. Support for different models differs, but basic
functions should work with majority of them. Program can work with
contacts, messages (SMS, EMS and MMS), calendar, todos, filesystem,
integrated radio, camera, etc. It also supports daemon mode to send and
receive SMSes.

Currently supported phones include:

* Many Nokia models.
* Alcatel BE5 (501/701), BF5 (715), BH4 (535/735).
* AT capable phones (Siemens, Nokia, Alcatel, IPAQ).
* OBEX and IrMC capable phones (Sony-Ericsson, Motorola).
* Symbian phones through gnapplet.

This package contains Gammu SMS daemon shared library.

%prep
%setup -q

%build
mkdir build-dir
cd build-dir
cmake ../ \
    -DBUILD_SHARED_LIBS=ON \
    -DINSTALL_LSB_INIT=ON \
    -DBUILD_PYTHON=/usr/bin/python \
    -DCMAKE_INSTALL_PREFIX=%_prefix \
    -DINSTALL_DOC_DIR=%gammu_docdir \
    -DINSTALL_LIB_DIR=%_lib \
    -DINSTALL_LIBDATA_DIR=%_lib
make %{?_smp_mflags} %{!?_smp_mflags:%{?jobs:-j %jobs}}

%check
cd build-dir
ctest -V

%install
%if 0%{?suse_version} == 0
rm -rf %buildroot
mkdir %buildroot
%endif
make -C build-dir install DESTDIR=%buildroot
%find_lang %{name}
%find_lang libgammu
cat libgammu.lang >> %{name}.lang
install -m644 docs/config/smsdrc %buildroot/etc/gammu-smsdrc

%post -n libGammu7 -p /sbin/ldconfig

%post -n libgsmsd7 -p /sbin/ldconfig

%postun -n libGammu7 -p /sbin/ldconfig

%postun -n libgsmsd7 -p /sbin/ldconfig

%post smsd
%if 0%{?mandriva_version}
%_post_service gammu-smsd
%endif
%if 0%{?suse_version}
%fillup_and_insserv gammu-smsd
%endif
%if 0%{?fedora_version} || 0%{?centos_version} || 0%{?rhel_version} || 0%{?fedora} || 0%{?rhel}
/sbin/chkconfig --add gammu-smsd
%endif

%preun smsd
%if 0%{?suse_version}
%stop_on_removal gammu-smsd
%endif
%if 0%{?mandriva_version}
%_preun_service gammu-smsd
%endif
%if 0%{?fedora_version} || 0%{?centos_version} || 0%{?rhel_version} || 0%{?fedora} || 0%{?rhel}
if [ $1 = 0 ] ; then
    /sbin/service gammu-smsd stop >/dev/null 2>&1
    /sbin/chkconfig --del <script>
fi
%endif


%postun smsd
%if 0%{?suse_version}
%restart_on_update gammu-smsd
%insserv_cleanup
%endif


%files -f %name.lang
%defattr(-,root,root)
%doc %gammu_docdir
%config /etc/bash_completion.d/gammu
%_bindir/gammu
%_bindir/gammu-config
%_bindir/gammu-detect
%_bindir/jadmaker
%_mandir/man1/gammu.1*
%_mandir/man1/gammu-config.1*
%_mandir/man1/gammu-detect.1*
%_mandir/man1/jadmaker.1*
%_mandir/man5/gammurc.5*
%_mandir/man5/gammu-backup.5*
%_mandir/man5/gammu-smsbackup.5*

%files smsd
%defattr(-,root,root)
%_bindir/gammu-smsd
%_bindir/gammu-smsd-inject
%_bindir/gammu-smsd-monitor
%_mandir/man1/gammu-smsd*
%_mandir/man7/gammu-smsd*
%_mandir/man5/gammu-smsd*
%attr(755,root,root) %config /etc/init.d/gammu-smsd
%config /etc/gammu-smsdrc

%files -n libGammu7
%defattr(-,root,root)
%_libdir/libGammu*.so.*
%_datadir/gammu/

%files -n libgsmsd7
%defattr(-,root,root)
%_libdir/libgsmsd*.so.*

%files devel
%defattr(-,root,root)
%_includedir/%name
%_libdir/pkgconfig/%name.pc
%_libdir/pkgconfig/%name-smsd.pc
%_libdir/*.so

%files -n python-gammu
%defattr(-,root,root)
%doc README.Python python/examples
%g_python_sitearch/*

%clean
rm -rf %buildroot

%changelog
* Fri Apr  3 2009 Michal Čihař <michal@cihar.com> - 1.23.93-1
- do not define own %%version, %%name, %%rel
- always use pkgconfig, pkg-config provides it
- do not delete build root on SUSE
- fix some package names (DBI and libusb) for Fedora
- drop support for Fedora 8

* Thu Jan 22 2009 Michal Čihař <michal@cihar.com> - 1.21.91-1
- merged python-gammu packaging as upstream merged the code

* Fri Oct 24 2008 Michal Čihař <michal@cihar.com> - 1.21.0-1
- fixed according to Fedora policy

* Wed Oct  8 2008  Michal Cihar <michal@cihar.com>
- do not remove build root in %%install
- move make test to %%check

* Tue Oct  7 2008  Michal Cihar <michal@cihar.com>
- use find_lang macro

* Thu Mar 28 2007  Michal Cihar <michal@cihar.com>
- update to current code status

* Thu Jan  6 2005  Michal Cihar <michal@cihar.com>
- add support for Mandrake, thanks to Olivier BERTEN <Olivier.Berten@advalvas.be> for testing
- use new disable-bluetooth

* Wed Nov 12 2003 Michal Cihar <michal@cihar.com>
- distiguish between packaging on SUSE and Redhat
- build depends on bluez if wanted

* Mon Nov 10 2003 Peter Soos <sp@osb.hu>
- using rpm macros where is possible
- added ldconfig to post/postun

* Mon Nov 03 2003 Michal Cihar <michal@cihar.com>
- split devel package

* Thu Jan 02 2003 Michal Cihar <michal@cihar.com>
- made it install in directories that are defined in rpm

* Sun Nov 10 2002 Marcin Wiacek <marcin@mwiacek.com>
- topnet.pl email no more available

* Sun Sep 30 2002 Marcin Wiacek <marcin-wiacek@topnet.pl>
- build system is now really working OK

* Sat Sep 15 2002 R P Herrold <herrold@owlriver.com>
- initial packaging
