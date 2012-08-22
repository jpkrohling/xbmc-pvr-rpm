%global PRERELEASE ALPHA5
# use below for pre-release
%global DIRVERSION %{version}-%{PRERELEASE}

Name: xbmc-pvr
Version: 12.0
Release: 3%{?dist}
URL: http://www.xbmc.org/

Source0: %{name}-%{DIRVERSION}-patched.tar.gz

ExcludeArch: ppc64
Buildroot: %{_tmppath}/%{name}-%{DIRVERSION}
Summary: Media center with the PVR Add-on from opdenkamp.
License: GPLv2+ and GPLv3+
Group: Applications/Multimedia
Conflicts: xbmc
BuildRequires: desktop-file-utils
BuildRequires: dbus-devel
BuildRequires: SDL-devel
BuildRequires: SDL_image-devel
BuildRequires: SDL_mixer-devel
BuildRequires: fontconfig-devel
BuildRequires: fribidi-devel
BuildRequires: glibc-devel
BuildRequires: glew-devel
BuildRequires: libstdc++-devel
BuildRequires: glib2-devel
BuildRequires: libjasper-devel
BuildRequires: libjpeg-devel
BuildRequires: libogg-devel
BuildRequires: libpng-devel
BuildRequires: libstdc++-devel
BuildRequires: e2fsprogs-devel
BuildRequires: libvorbis-devel
BuildRequires: lzo-devel
BuildRequires: pcre-devel
BuildRequires: zlib-devel
BuildRequires: tre-devel
BuildRequires: boost-devel
BuildRequires: bzip2-devel
BuildRequires: freetype-devel
BuildRequires: libXinerama-devel
BuildRequires: fontconfig-devel
BuildRequires: mysql-devel
BuildRequires: jasper-devel
BuildRequires: enca-devel
BuildRequires: cmake
BuildRequires: gperf
BuildRequires: nasm
BuildRequires: libXmu-devel
BuildRequires: pcre-devel
BuildRequires: gcc-c++
BuildRequires: sqlite-devel
BuildRequires: curl-devel
BuildRequires: libcdio-devel
BuildRequires: flex
BuildRequires: libmad-devel
BuildRequires: libsamplerate-devel
BuildRequires: libsmbclient-devel
BuildRequires: libmms-devel
BuildRequires: libXtst-devel
BuildRequires: libvdpau-devel
BuildRequires: desktop-file-utils
BuildRequires: python-devel
BuildRequires: wavpack-devel
BuildRequires: a52dec-devel
BuildRequires: libmpeg2-devel
BuildRequires: libmpcdec-devel
BuildRequires: flac-devel
BuildRequires: avahi-devel
BuildRequires: libtool
BuildRequires: libtiff-devel
BuildRequires: libvdpau-devel
BuildRequires: libdvdread-devel
BuildRequires: ffmpeg-devel
BuildRequires: faad2-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: libdca-devel
BuildRequires: libass-devel >= 0.9.7
BuildRequires: hdhomerun-devel
BuildRequires: libcrystalhd-devel
BuildRequires: libmodplug-devel
BuildRequires: libmicrohttpd-devel
BuildRequires: expat-devel
BuildRequires: zip
BuildRequires: gettext-autopoint
BuildRequires: librtmp-devel
BuildRequires: libbluray-devel
#BuildRequires: libbluray-devel >= 0.2.1
BuildRequires: yajl-devel
BuildRequires: bluez-libs-devel
BuildRequires: cwiid-devel
BuildRequires: tinyxml-devel
BuildRequires: libva-devel
BuildRequires: lame-devel

# nfs-utils-lib-devel package currently broken
#BuildRequires: nfs-utils-lib-devel
# afp build currently broken
#BuildRequires: afpfs-ng-devel
# VAAPI currently not working, comment-out
#BuildRequires: libva-freeworld-devel

# need explicit requires for these packages
# as they are dynamically loaded via XBMC's arcane 
# pseudo-DLL loading scheme (sigh)
Requires: libcrystalhd
Requires: librtmp
Requires: libbluray

# needed when doing a minimal install, see
# https://bugzilla.rpmfusion.org/show_bug.cgi?id=1844
Requires: glx-utils
Requires: xorg-x11-utils

# These are just symlinked to, but needed both at build-time
# and for installation
BuildRequires: python-imaging
Requires: python-imaging

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%description
XBMC media center is a free cross-platform media-player jukebox and
entertainment hub.  XBMC can play a spectrum of of multimedia formats,
and featuring playlist, audio visualizations, slideshow, and weather
forecast functions, together third-party plugins.

%prep

%setup -q -n %{name}-%{DIRVERSION}

%build

chmod +x bootstrap
./bootstrap
# Can't use export nor %%configure (implies using export), because
# the Makefile pile up *FLAGS in this case.

./configure \
--prefix=%{_prefix} --bindir=%{_bindir} --includedir=%{_includedir} \
--libdir=%{_libdir} --datadir=%{_datadir} \
--with-lirc-device=/var/run/lirc/lircd \
--enable-external-libraries \
--enable-vdpau \
--enable-pulse \
--disable-dvdcss \
--disable-optimizations --disable-debug \
CPPFLAGS="-I/usr/include/ffmpeg" \
CFLAGS="$RPM_OPT_FLAGS -fPIC -I/usr/include/ffmpeg -D__STDC_CONSTANT_MACROS" \
CXXFLAGS="$RPM_OPT_FLAGS -fPIC -I/usr/include/ffmpeg -D__STDC_CONSTANT_MACROS" \
LDFLAGS="-fPIC" \
LIBS="-L%{_libdir}/mysql -lhdhomerun $LIBS" \
ASFLAGS=-fPIC

make %{?_smp_mflags} VERBOSE=1

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
#make -C tools/EventClients DESTDIR=$RPM_BUILD_ROOT install 
# remove the doc files from unversioned /usr/share/doc/xbmc, they should be in versioned docdir
rm -r $RPM_BUILD_ROOT/%{_datadir}/doc/

desktop-file-install \
 --dir=${RPM_BUILD_ROOT}%{_datadir}/applications \
 $RPM_BUILD_ROOT%{_datadir}/applications/xbmc.desktop

# Normally we are expected to build these manually. But since we are using
# the system Python interpreter, we also want to use the system libraries
install -d $RPM_BUILD_ROOT%{_libdir}/xbmc/addons/script.module.pil/lib
ln -s %{python_sitearch}/PIL $RPM_BUILD_ROOT%{_libdir}/xbmc/addons/script.module.pil/lib/PIL
#install -d $RPM_BUILD_ROOT%{_libdir}/xbmc/addons/script.module.pysqlite/lib
#ln -s %{python_sitearch}/pysqlite2 $RPM_BUILD_ROOT%{_libdir}/xbmc/addons/script.module.pysqlite/lib/pysqlite2


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc copying.txt keymapping.txt LICENSE.GPL docs/README.linux
%{_bindir}/xbmc
%{_bindir}/xbmc-standalone
%{_libdir}/xbmc
%{_datadir}/xbmc
%{_datadir}/xsessions/XBMC.desktop
%{_datadir}/applications/xbmc.desktop
%{_datadir}/icons/hicolor/*/*/*.png

%changelog
* Sun Mar 25 2012 Alex Lancaster <alexlan[AT]fedoraproject org> - 11.0-1
- Update to Eden final 11.0
- Drop libpng 1.5 patches, applied upstream

* Fri Mar  9 2012 Alex Lancaster <alexlan[AT]fedoraproject org> - 11.0-0.10.Eden_rc2
- Update to Eden release candidate 2 (rc2)

* Fri Mar  9 2012 Alex Lancaster <alexlan[AT]fedoraproject org> - 11.0-0.9.Eden_beta2
- Temporarily drop clientevents package (currently fails to build) to
  fix overall FTBFS.

* Fri Mar  9 2012 Alex Lancaster <alexlan[AT]fedoraproject org> - 11.0-0.8.Eden_beta2
- Drop python-sqlite2 BR (obsoleted package), should use internal sqlite3 (#2217)

* Fri Mar 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 11.0-0.7.Eden_beta2
- Rebuilt for FFmpeg/x264

* Sun Jan 29 2012 Alex Lancaster <alexlan[AT]fedoraproject org> - 11.0-0.6.Eden_beta2
- Update to Eden beta2

* Fri Dec 30 2011 Alex Lancaster <alexlan[AT]fedoraproject org> - 11.0-0.5.Eden_beta1
- Add additional patch from http://trac.xbmc.org/ticket/12001 to
  fix uninitialised pointer with libpng 1.5
- Remove upstreamed, or otherwise obsoleted patches 

* Thu Dec 29 2011 Alex Lancaster <alexlan[AT] fedoraproject org> - 11.0-0.4.Eden_beta1
- Enable libpng 1.5 patch, still needed, upstream bug is at: 
  http://trac.xbmc.org/ticket/12001

* Wed Dec 28 2011 Alex Lancaster <alexlan[AT] fedoraproject org> - 11.0-0.3.Eden_beta1
- Added glx-utils and xorg-x11-utils as Requires, so selecting
  minimal install works out of the box (#1844)

* Wed Dec 28 2011 Alex Lancaster <alexlan[AT]fedoraproject org> - 11.0-0.2.Eden_beta1
- Re-enable external ffmpeg
- Add EventClients sub-package (patch thanks to Ben Konrath <ben@bagu.org>)
- More spec cleaning

* Wed Dec 28 2011 Alex Lancaster <alexlan[AT]fedoraproject org> - 11.0-0.1.Eden_beta1
- Update to 11.0 beta1
- Disable patches that are obsolete (keep around while testing)
- Update icon cache (#2097)

* Tue Dec 20 2011 Alex Lancaster <alexlan[AT] fedoraproject org> - 10.1-9
- Add patch from OpenElec distribution to fix broken YouTube plugin
  (should fix #1905)

* Wed Dec 14 2011 Xavier Bachelot <xavier@bachelot.org> - 10.1-8
- Add patch for newer libbluray support.
- Add patch for libpng 1.5 support.

* Wed Nov 23 2011 Nicolas Chauvet <kwizart@gmail.com> - 10.1-7
- Rebuilt for libcdio

* Sat Nov  5 2011 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.1-6
- Disable using external ffmpeg for the moment, until such time as
  either we backport a fix for 0.8 ffmpeg or we build XBMC Eden (11.x)
  (see #1962)

* Mon Sep 26 2011 Nicolas Chauvet <kwizart@gmail.com> - 10.1-5
- Rebuilt for FFmpeg-0.8

* Fri Sep  2 2011 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.1-4
- Remove hal-devel as BuildRequires, dropped in f16 and later:
  http://fedoraproject.org/wiki/Features/HalRemoval
  replaced by udisks, upower, libudev, but not clear if xbmc
  can use those packages yet (fixes #1915).  
- Add dbus-devel, since hal-devel no longer automatically pulls
  package in.

* Tue Apr 05 2011 Nicolas Chauvet <kwizart@gmail.com> - 10.1-3
- Rebuilt for libmysqlclient bump (was built with previous version).

* Wed Mar 30 2011 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.1-2
- Patch from upstream to fix builds for GCC 4.6.x, slightly modified
  to handle previous patches for Makefile.in
  http://trac.xbmc.org/ticket/11383

* Tue Mar 29 2011 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.1-1
- Update to 10.1
- Add support for using system python-imaging and pysqlite modules, thanks to Pierre 
  Ossman for patch (#1575)
- Drop most references to SVNVERSION, upstream now uses git

* Sun Mar 27 2011 Nicolas Chauvet <kwizart@gmail.com> - 10.0-2
- Rebuild for libmysqlclient

* Thu Dec 23 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.0-1
- Update to 10.0 (Dharma final)

* Sun Dec 12 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.0-0.23.Dharma_rc2
- Rebase to Dharma rc2 (SVN r35567)
- Update Python 2.7 patch, to fix DLL search patch problems (#1532).  Thanks to
  Richard Guest for patch.

* Sun Nov 21 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.0-0.22.Dharma_rc1
- Need explicit requires for librtmp and libbluray: loaded dynamically
  via XBMC's DLL mechanism which is missed by autodeps

* Fri Nov 19 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.0-0.21.Dharma_rc1
- Rebase to Dharma rc1 (SVN r35326)
- Remove conditionals on {librtmp,libbluray}-devel: now present in all
  currently supported releases (f13+)

* Thu Nov 18 2010 Nicolas Chauvet <kwizart@gmail.com> - 10.0-0.20.Dharma_beta4.1
- Rebuilt for libmicrohttpd - ABI bump
 https://admin.fedoraproject.org/updates/libmicrohttpd-0.9.2-3.fc14

* Sun Nov  7 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.0-0.20.Dharma_beta4
- Rebase to Dharma beta 4 (SVN r35068)
- Enable libbluray (currently only available for f15+)
- Drop patch disabling SNES (fixed in nasm)

* Thu Oct 14 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.0-0.19.Dharma_beta3
- Rebase to Dharma beta3 (SVN r34731)
- Disable VAAPI: crashes XBMC when playing back rtmp streams

* Thu Oct 14 2010 Nicolas Chauvet <kwizart@gmail.com> - 10.0-0.18.Dharma_beta2
- Rebuilt for gcc bug

* Sat Sep 18 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.0-0.17.Dharma_beta2
- Enable librtmp support on in F-14 and later (until librtmp is build on F-13)

* Thu Sep 16 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.0-0.16.Dharma_beta2
- Enable VAAPI: add BR: libva-freeworld-devel

* Thu Sep 16 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.0-0.15.Dharma_beta2
- Add BuildRequires for librtmp-devel, used for various plugins

* Tue Sep 14 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.0-0.14.Dharma_beta2
- Rebase to Dharma beta 2 (SVN r33778)

* Tue Sep 14 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.0-0.13.Dharma_beta1
- Disable SNES codec (Nintendo sound files) on f14 as nasm >=2.09 has
  trouble compiling with that version on f14 (rhbz#633646)

* Mon Sep 13 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.0-0.12.Dharma_beta1
- Upstream is dropping month from version, using 10.0 as Dharma release version.
- Add explicit Requires for libcrystalhd

* Wed Sep  1 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.9-0.11.Dharma_beta1
- Drop libmodplug/microhttpd patch, no longer needed 

* Wed Sep  1 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.9-0.10.Dharma_beta1
- Rebase to Dharma beta1 release

* Sun Aug 29 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.5-0.9.20100820svn32970
- Add -D__STDC_CONSTANT_MACROS for building with ffmpeg > 0.6

* Wed Aug 25 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.5-0.8.20100820svn32970
- Default to using /var/run/lirc/lircd (#1325)

* Fri Aug 20 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.5-0.7.20100820svn32970
- Rebase patches to r32970 on Dharma branch

* Thu Jul 29 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.5-0.7.20100728svn32266
- Add patch from upstream trac ticket 9584 to find Python 2.7
  (needed for F-14+)
- Add BuildRequires: zip

* Thu Jul 29 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.5-0.6.20100728svn32266
- Need to conditionally enable gettext-autopoint in BuildRequires
  for F-14+ and gettext otherwise

* Thu Jul 29 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.5-0.5.20100728svn32266
- Add gettext-devel to BuildRequires for autopoint

* Wed Jul 28 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.5-0.4.20100728svn32266
- Sync with latest Dharma branch (r32266)

* Mon Jul 19 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.5-0.3.20100719svn31991
- Remove 24 patches which have been applied upstream, yay!
- Rebased 2 patches: libdvd patch and hdhomerun patch for Dharma
- Add some new patches, some of which have upstream trac tickets,
  others need to
- Renumber patches

* Mon Jul 19 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.5-0.2.20100719svn31991
- Sync with Dharma branch

* Mon Jul 19 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 10.5-0.1.20100719svn31977
- Major overhaul for 10.x version of XBMC
- Fix file section for better FHS-compliance
- Drop a lot of patches that have been upstreamed, and rebase others

* Fri May 21 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 9.11-19
- Add new BR for libmodplug-devel, expat-devel, libmicrohttpd-devel
  in preparation for 10.x

* Fri Mar 26 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 9.11-18
- Exclude ppc64 (not available for F-13+ in any case)

* Fri Mar 26 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 9.11-17
- Fixed license tag to include GPLv3+

* Wed Mar 24 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 9.11-16
- Add BuildRequires: hdhomerun-devel

* Sun Mar  7 2010 Rolf Fokkens <rolf fokkens[AT]wanadoo nl> - 9.11-15
- Add patch for force using hdhomerun external, had to create a
  hdhomerun-devel package first

* Sat Mar  6 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 9.11-14
- Add patch that removes all webserver GoAhead functionality due to
  problematic license
- Drop BR: faac-devel since it was moved to nonfree

* Fri Mar  5 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 9.11-13
- Patches to add -lXext to LIBS (thanks Ralf Corsepius)
- Hack to work around ffmpeg sws_scale() incompatibility (thanks Ralf)
- Remove bundled boost, libportaudio, libglew and extra unused zlib
  header from tarball
- Call desktop-file-install as per review guidelines
- Make spyce files executable, quiets rpmlint

* Mon Feb  8 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 9.11-12
- More patches from Ralf Corsepius
- Update configure line, specify *FLAGS directly in configure line
  (thanks Ralf)
- Touch rsxs Makefiles to prevent rerunning the autotools (thanks Ralf)
- Add missing %%clean (thanks Ralf)
- Remove even more unused library copies in generate tarball script

* Tue Jan 26 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 9.11-11
- Add another patch to ensure Makefile's pass compiler flags properly
  (thanks Ralf C)
- Remove commands no longer needed in install

* Mon Jan 25 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 9.11-10
- Patches for RPM_OPT_FLAGS being recognised throughout (thanks
  Ralf C)
- Patch for goom (Ralf C)
- Patch for using external zlib (Ralf C)
- Pass CPPFLAGS to configure (Ralf C)

* Thu Jan 21 2010 Rolf Fokkens <rolf fokkens[AT]wanadoo nl> - 9.11-9
- increase compression ratio of tarball by compressing with cx
  the src.rpm is now about 20% smaller
- remove patch0 and patch1, they are obsolete now
- rename patch2 and patch10 to more meaningful name

* Thu Jan 21 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 9.11-8
- Update xbmc script patch (thanks Ralf C)
- Reorder patches, add upstream tickets where possible
- Drop SVN_REV from line until exact version clarified

* Mon Jan 18 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 9.11-7
- Remove bundled copies of libraries, and code that we can't
  distribute from upstream tarball with script
- Drop patch against ffmpeg which we removed from tarball
- Trim description

* Sun Jan 17 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 9.11-6
- Add patch for web server segfaults on 64-bit (thanks Ralf Corsepius)
- Drop patch backup for .spyce, causes packaging problems (thanks Ralf
  Corsepius)
- Remove bogus header from install (thanks Ralf Corsepius)
- More comprehensive pre-built Win32 binary removal (thanks Ralf
  Corsepius)
- Add SVN_REV to configure line for plugins (thanks Graeme Gillies)

* Tue Jan  5 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 9.11-5
- Remove unnecessary BR: mysql-libs
- Prune out unneeded stuff from build (thanks Rolf Fokkens)
- Remove libraries not compiled (thanks Rolf Fokkens)
- Patch to some nasty GCC warnings (thanks Ralf Corsepius)

* Thu Dec 31 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 9.11-4
- Patches to fix installation paths to /usr/lib/ (thanks Ralf Corsepius)
- Patch to fix other issues: random number library (thanks Ralf Corsepius)

* Wed Dec 30 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 9.11-3
- Cleanup spec for submission to RPM Fusion
- Fix changelog entries to use standard numbering to quiet rpmlint
- Use standard URL for sourceforge tarballs
- Add BR: pulseaudio-libs-devel and others
- Add patch that removes comments in rules in Makefile.in that
  prevented install target working

* Tue Dec 29 2009 Rolf Fokkens <rolf fokkens wanadoo nl> - 9.11-2
- use external libcdio again, patch by MaestroDD

* Fri Dec 25 2009 Rolf Fokkens <rolf fokkens wanadoo nl> - 9.11-1
- Update to 9.11

* Fri Dec 18 2009 Rolf Fokkens <rolf fokkens wanadoo nl> - 9.11-0.5.rc1
- Update to 9.11 rc1

* Fri Dec 11 2009 Rolf Fokkens <rolf fokkens wanadoo nl> - 9.11-0.4.beta2
- Update to 9.11 beta2

* Tue Dec 1 2009  Rolf Fokkens <rolf fokkens wanadoo nl> - 9.11-0.3.beta1
- Force using external libdvdread and libdvdcss. libdvdnav is stil internal
  as xbmc needs its internals.

* Sat Nov 28 2009  Rolf Fokkens <rolf fokkens wanadoo nl> - 9.11-0.2.beta1
- replaced dependency on libdts by libdca
- removed dependency on external libcdio, use included one instead
  now detection of CD's and DVD's works again
- Compiles and runs on Fedora 11
- Update to 9.11 beta1

* Sun Nov 15 2009  Rolf Fokkens <rolf fokkens wanadoo nl> - 9.11-0.1.alpha2
- Compiles and runs on Fedora 11
- Update to 9.11 alpha2

* Fri May 15 2009 Scott Harvanek <scotth@login.com> - 9.04-1
- Update to 9.04

* Wed Jan 28 2009 Scott Harvanek <scotth@login.com> - 8.10-3
- Added requires for
- alsa-plugins-pulseaudio, libogg, libmad, libvorbis

* Fri Jan 2 2009 Scott Harvanek <scotth@login.com> - 8.10-2
- Patch for English language strings.xml

* Thu Nov 27 2008 Scott Harvanek <scotth@login.com> - 8.10-1
- v8.10
- Fedora 10 RPM
