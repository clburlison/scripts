RELEASE=3.1.1
PKGVERSION=${RELEASE}
PKGID=com.clburlison.puppetdb-terminus
all: clean build

download: clean
	mkdir -p tmp/puppetdb
	curl -L -o tmp/${RELEASE}.tar.gz https://github.com/puppetlabs/puppetdb/archive/${RELEASE}.tar.gz
	tar -xf tmp/${RELEASE}.tar.gz -C tmp/puppetdb --strip-components=1
	

clean:
	rm -rf tmp
	rm -rf pkgroot
	if [ -f out/puppetdb-terminus-${PKGVERSION}.pkg ]; then rm out/puppetdb-terminus-${PKGVERSION}.pkg; fi;

build: download
	mkdir -p pkgroot/Library/Ruby/Site/2.0.0
	mkdir -p out
	mv tmp/puppetdb/puppet/lib/puppet pkgroot/Library/Ruby/Site/2.0.0/
	pkgbuild --root pkgroot --identifier ${PKGID} --version ${PKGVERSION} --scripts scripts out/puppetdb-terminus-${PKGVERSION}.pkg
	
