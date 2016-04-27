PKGTITLE=python-tinys3
PKGVERSION=0.1.7
PKGID=com.github.clburlison.python-tinys3
# SIGN=--sign "Developer ID Installer: Clayton Burlison"

all: clean build

clean:
	rm -rf pkgroot
	rm -rf out

build: install
	mkdir -p out
	pkgbuild --root pkgroot --identifier ${PKGID} --version ${PKGVERSION} ${SIGN} --ownership recommended out/${PKGTITLE}-${PKGVERSION}.pkg

install:
	mkdir -p pkgroot/Library/Python/2.7/site-packages/
	pip install --target="pkgroot/Library/Python/2.7/site-packages" tinys3