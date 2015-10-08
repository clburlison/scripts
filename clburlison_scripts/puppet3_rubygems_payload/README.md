puppet3_rubygems_payload
===

This will repackage the latest Puppet3, Facter, Hiera, r10k, CFPropertyList, sqlite3, and hiera-eyaml ruby gems for easy deployment. With El Capitan, SIP has made changes to where software can and can't be installed. Puppet 3 has always installed into `/usr/bin` and it will still work (along with facter). However, hiera along with r10k are not allowed to save their executable inside of `/usr/bin` as such I am moving all executables to `/usr/local/bin/`. 

This creates a payload package, meaning client computers no longer need to download and compile the gems locally. This saves time when re-imaging and first time setup. The downside to how I am creating this package is crud can be added in quite easily. Make sure and run this on a clean Virtual Machine that doesn't have ruby gems or other files inside of `/usr/local/bin`.

Puppet 4.0 with the new puppet agent resolves all issues this package addresses properly however, at this time I am unable to upgrade from Puppet 3. 

See reference link [SIP exceptions](https://derflounder.wordpress.com/2015/10/01/system-integrity-protection-adding-another-layer-to-apples-security-model/)