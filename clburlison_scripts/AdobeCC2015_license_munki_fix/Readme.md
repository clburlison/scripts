Adobe CC 2015 license munki fix
===

This will create an OnDemand package for Munki that will license Adobe CC 2014/2015 with your enterprise serial number. This can solve two issues: 1) If you have multiple enterprise licenses that you are supporting and 2) if Adobe software becomes unserialized. You can install trial packages and serialize at a later point. 

My issue was with CC 2015 software losing the serial. Since applying this fix one time does not guarantee the software will stay serialized I have made this an OnDemand package. This means you should add the "AdobeCC2015_license_munki_fix" item to an ``optional_installs`` array inside of your Munki manifest. 

For this to work you will need to copy your license data to the "license_data" directory. This can be created from Creative Cloud Packager's "Create License File" option.

The license_data directory should have the following contents:

```bash
license_data
├── AdobeSerialization
├── RemoveVolumeSerial
├── helper.bin
└── prov.xml

0 directories, 4 files
```

# Extras
The munki_examples directory has a html descrition for the OnDemand Package. You will want to upload the "adobe-cc-signin-required.png" picture to a web server. Then modify the description.html with the URL. An example pkginfo for the license fix is also provided.

# Make Options (aka usage)

* ``make`` (all) - clean working directories and build the package
* ``make clean`` - clean working directories
* ``make build`` - build the package
* ``make import`` - clean working directories, build package, and import into munki 

# Other Options 
Tim Sutton has another solution located here: [make-adobe-cc-license-pkg](https://github.com/timsutton/make-adobe-cc-license-pkg). His project offers additional features that I didn't need. Both serve the same purpose.
