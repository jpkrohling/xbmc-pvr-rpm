xbmc-pvr-rpm
============

# RPM builders for XBMC from [opdenkamp/xbmc](https://github.com/opdenkamp/xbmc)

This is basically an environment to build a XBMC RPM based on the fork from opdenkamp, which includes the PVR Add-on. This was mostly based on the RPM Fusion's spec files for XBMC, but it differs substantially. Use it at your own risk. I hope this will be obsolete soon, as I expect opdenkamp's features to be integrated into the main XBMC's repo soon, which means that it should be picked up by RPM Fusion.

## Instructions

 * Execute the shell script on the `SOURCES` directory. This will grab the sources and build a tar.gz file, that will be used by the build.
 * Execute `$ rpmbuild -ba xbmc-pvr.spec` on the `SPECS` directory. If everything goes well, you'll find a RPM package in the `RPMS` directory.

If you never built an RPM before, take a look at [the official Fedora wiki page](http://fedoraproject.org/wiki/How_to_create_an_RPM_package), but basically, you'll need this:

    $ sudo yum install @development-tools fedora-packager rpmdevtools
