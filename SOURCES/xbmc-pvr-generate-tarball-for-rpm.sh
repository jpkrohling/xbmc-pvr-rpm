#!/bin/sh

if [ -d xbmc-pvr-12.0-ALPHA3 ]; then
	echo "Updating local checkout"
	cd xbmc-pvr-*
	git pull
	cd ..
else
	GITHUBURL=git://github.com/opdenkamp/xbmc.git
	git clone $GITHUBURL xbmc-pvr-clone
fi;

export VERSION_TAG=`grep VERSION_TAG xbmc-pvr-*/xbmc/GUIInfoManager.h | awk '{print $3}' | sed 's%"%%gi'`
export VERSION_MINOR=`grep VERSION_MINOR xbmc-pvr-*/xbmc/GUIInfoManager.h | awk '{print $3}' | sed 's%"%%gi'`
export VERSION_MAJOR=`grep VERSION_MAJOR xbmc-pvr-*/xbmc/GUIInfoManager.h | awk '{print $3}' | sed 's%"%%gi'`
export VERSION=$VERSION_MAJOR.$VERSION_MINOR$VERSION_TAG

if [ -d xbmc-pvr-clone ]; then
	mv xbmc-pvr-clone xbmc-pvr-$VERSION
fi; 

if [ -f xbmc-pvr-$VERSION-patched.tar.xz ]; then
	rm xbmc-pvr-$VERSION-patched.tar.xz
fi;

# repack
tar czf xbmc-pvr-$VERSION-patched.tar.gz xbmc-pvr-$VERSION
