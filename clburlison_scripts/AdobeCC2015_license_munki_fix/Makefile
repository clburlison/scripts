PKGVERSION=1.0.0
PKGID=com.github.clburlison

all: clean build

clean:
	rm -rf pkgroot
	rm -rf out

build:
	mkdir -p pkgroot/tmp/adobe_license
	mkdir -p out
	cp -R license_data/* pkgroot/tmp/adobe_license/
	pkgbuild --root pkgroot --identifier ${PKGID} --version ${PKGVERSION} --scripts scripts out/AdobeCC2015_license_munki_fix-${PKGVERSION}.pkg

import: all
	/usr/local/munki/munkiimport --OnDemand \
	--icon_path=munki_examples/AdobeCC2015_license_munki_fix.png \
	--description=munki_examples/description.html \
	--blocking_application="Adobe Application Manager" \
	--blocking_application="Adobe After Effects CC 2015" \
	--blocking_application="Adobe After Effects CC 2014" \
	--blocking_application="Adobe Audition CC 2015" \
	--blocking_application="Adobe Audition CC 2014" \
	--blocking_application="Adobe Bridge CC 2015" \
	--blocking_application="Adobe Bridge CC 2014" \
	--blocking_application="Adobe Dreamweaver CC 2015" \
	--blocking_application="Adobe Dreamweaver CC 2014" \
	--blocking_application="Adobe Flash Pro CC 2015" \
	--blocking_application="Adobe Flash Pro CC 2014" \
	--blocking_application="Adobe Illustrator CC 2015" \
	--blocking_application="Adobe Illustrator CC 2014" \
	--blocking_application="Adobe InCopy CC 2015" \
	--blocking_application="Adobe InCopy CC 2014" \
	--blocking_application="Adobe InDesign CC 2015" \
	--blocking_application="Adobe InDesign CC 2014" \
	--blocking_application="Adobe Lightroom" \
	--blocking_application="Adobe Media Encoder CC 2015" \
	--blocking_application="Adobe Media Encoder CC 2014" \
	--blocking_application="Adobe Muse CC 2015" \
	--blocking_application="Adobe Muse CC 2014" \
	--blocking_application="Adobe Photoshop CC 2015" \
	--blocking_application="Adobe Photoshop CC 2014" \
	--blocking_application="Adobe Prelude CC 2015" \
	--blocking_application="Adobe Prelude CC 2014" \
	--blocking_application="Adobe Premiere Pro CC 2015" \
	--blocking_application="Adobe Premiere Pro CC 2014" \
	--blocking_application="Adobe Scout CC 2015" \
	--blocking_application="Adobe Scout CC 2014" \
	--displayname="Adobe CC License Fix" \
	out/AdobeCC2015_license_munki_fix-${PKGVERSION}.pkg