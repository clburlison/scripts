PKGTITLE=puppet4
PKGVERSION=4.3.2
PKGID=com.github.clburlison.puppet4
# SIGN=--sign "Developer ID Installer: Clayton Burlison"

all: clean build

clean:
	rm -rf pkgroot
	rm -rf out
	rm -rf repo

build: install
	mkdir -p pkgroot/Library/Ruby/Gems/2.0.0
	mkdir -p pkgroot/usr/local/bin
	mkdir -p out
	cp -R repo/* pkgroot/Library/Ruby/Gems/2.0.0/
	cp -R repo/bin/* pkgroot/usr/local/bin
	pkgbuild --root pkgroot --identifier ${PKGID} --version ${PKGVERSION} ${SIGN} --ownership recommended out/${PKGTITLE}-${PKGVERSION}.pkg

install:
	sudo /opt/puppetlabs/puppet/bin/gem install puppet --platform 'Darwin' -i repo -N --install-dir /opt/puppetlabs/puppet/lib/ruby/gems/2.1.0 --bindir /opt/puppetlabs/puppet/bin