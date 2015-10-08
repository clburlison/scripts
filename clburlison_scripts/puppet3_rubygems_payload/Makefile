PKGTITLE=puppet3_rubygems_payload
PKGVERSION=2.0.1
PKGID=com.github.clburlison.puppet3_rubygems_payload
# SIGN=--sign "Developer ID Installer: Clayton Burlison"

all: clean build

clean:
	sudo rm -rf pkgroot
	rm -rf out

build: install
	mkdir -p pkgroot/Library/Ruby/Gems/2.0.0
	mkdir -p pkgroot/usr/local/bin
	mkdir -p out
	sudo cp -R /Library/Ruby/Gems/2.0.0/* pkgroot/Library/Ruby/Gems/2.0.0/
	sudo cp -R /usr/local/bin/{eyaml,facter,hiera,minitar,puppet,r10k} pkgroot/usr/local/bin
	# chmod -R 755 pkgroot/*
	# chown -R root:wheel pkgroot/*
	pkgbuild --root pkgroot --identifier ${PKGID} --version ${PKGVERSION} ${SIGN} --ownership recommended out/${PKGTITLE}-${PKGVERSION}.pkg

install:
	sudo gem install -N -v '<4.0' puppet -n /usr/local/bin
	sudo gem install -N r10k sqlite3 hiera-eyaml -n /usr/local/bin