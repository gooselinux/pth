Summary:        The GNU Portable Threads library
Name:           pth
Version:        2.0.7
Release:        9.3%{?dist}
License:        LGPLv2+
Group:          System Environment/Libraries
URL:            http://www.gnu.org/software/pth/
Source:         ftp://ftp.gnu.org/gnu/pth/pth-%{version}.tar.gz
Source1:        ftp://ftp.gnu.org/gnu/pth/pth-%{version}.tar.gz.sig
Patch1:         pth-2.0.7-dont-remove-gcc-g.patch
Patch2:         pth-2.0.7-config-script.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Pth is a very portable POSIX/ANSI-C based library for Unix platforms
which provides non-preemptive priority-based scheduling for multiple
threads of execution ("multithreading") inside server applications.
All threads run in the same address space of the server application,
but each thread has it's own individual program-counter, run-time
stack, signal mask and errno variable.

%package devel
Summary:        Development headers and libraries for GNU Pth
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Development headers and libraries for GNU Pth.


%prep
%setup -q
%patch1 -p1 -b .dont-remove-gcc-g
%patch2 -p1 -b .config-script


%build
%configure --disable-static ac_cv_func_sigstack='no'

# Work around multiarch conflicts in the pth-config script in order
# to complete patch2. Make the script choose between /usr/lib and
# /usr/lib64 at run-time.
if [ "%_libdir" == "/usr/lib64" ] ; then
    if grep -e '^pth_libdir="/usr/lib64"' pth-config ; then
        sed -i -e 's!^pth_libdir="/usr/lib64"!pth_libdir="/usr/lib"!' pth-config
    else
        echo "ERROR: Revisit the multiarch pth_libdir fixes for pth-config!"
        exit 1
    fi
fi
if grep -e "$RPM_OPT_FLAGS" pth-config ; then
    # Remove our extra CFLAGS from the pth-config script, since they
    # don't belong in there.
    sed -i -e "s!$RPM_OPT_FLAGS!!g" pth-config
else
    echo "ERROR: Revisit the multiarch CFLAGS fix for pth-config!"
    exit 1
fi

# this is necessary; without it make -j fails
make pth_p.h
make %{?_smp_mflags}


%check
make test
l=$($(pwd)/pth-config --libdir)
%ifarch x86_64 ppc64
    [ "$l" == "/usr/lib64" ]
%endif


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc ANNOUNCE AUTHORS COPYING ChangeLog HISTORY NEWS PORTING README
%doc SUPPORT TESTS THANKS USERS
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc HACKING
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.so
%{_mandir}/*/*
%{_datadir}/aclocal/*


%changelog
* Wed Jun 16 2010 Andreas Schwab <schwab@redhat.com> - 2.0.7-9.3
- Add %{?dist} (#604531)

* Mon Apr 26 2010 Dennis Gregorovic <dgregor@redhat.com> - 2.0.7-9.2
- Rebuilt for RHEL 6
- Related: rhbz#566527

* Mon Apr 26 2010 Dennis Gregorovic <dgregor@redhat.com> - 2.0.7-9.1
- Rebuilt for RHEL 6
Related: rhbz#566527

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat May 31 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.7-7
- Drop "|| :" from check section. It failed to build for mdomsch
  in Rawhide today.

* Fri Feb 08 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.7-6
- rebuilt for GCC 4.3 as requested by Fedora Release Engineering

* Sun Oct 21 2007 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.7-5
- Patch pth-config.
  This shall fix the multiarch conflict in pth-devel (#342961).
  It must not return -I/usr/include and -L/usr/{lib,lib64} either,
  since these are default search paths already.
- Replace the config.status CFLAGS sed expr with a patch.

* Tue Aug 21 2007 Michael Schwendt <mschwendt@fedoraproject.org>
- rebuilt

* Thu Aug  2 2007 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.7-2
- Clarify licence (LGPLv2+).

* Sat Nov 25 2006 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.7-1
- Update to 2.0.7 (very minor maintenance updates only).

* Mon Aug 28 2006 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.6-3
- rebuilt

* Mon May 22 2006 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.6-2
- Insert -g into CFLAGS after configure script removes it.
- Disable configure check for obsolete sigstack(), which segfaults.

* Thu Feb 16 2006 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.6-1
- Update to 2.0.6.

* Fri Oct  7 2005 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.5-1
- Update to 2.0.5.
- Don't build static archive.

* Fri May 13 2005 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.4-3
- rebuilt

* Thu Apr  7 2005 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.4-2
- rebuilt

* Thu Feb 24 2005 Michael Schwendt <mschwendt@fedoraproject.org> - 0:2.0.4-1
- Update to 2.0.4.
- Remove ancient changelog entries which even pre-date Fedora.

* Tue Dec 14 2004 Michael Schwendt <mschwendt@fedoraproject.org> - 0:2.0.3-1
- Update to 2.0.3, minor and common spec adjustments + LGPL, %%check,
  use URLs for official GNU companion sites.

* Thu Oct 07 2004 Adrian Reber <adrian@lisas.de> - 0:2.0.2-0.fdr.2
- iconv-ing spec to utf8

* Wed Oct 06 2004 Adrian Reber <adrian@lisas.de> - 0:2.0.2-0.fdr.1
- Update to 2.0.2 and current Fedora guidelines.
- added workaround for make -j problem

* Sat Mar 22 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.0.0-0.fdr.1
- Update to 2.0.0 and current Fedora guidelines.
- Exclude %%{_libdir}/*.la

* Fri Feb  7 2003 Ville Skyttä <ville.skytta at iki.fi> - 1.4.1-1.fedora.1
- First Fedora release, based on Ryan Weaver's work.
- Move (most of) docs to main package.

