r10k_payload
===

This payload is a hacky way of installing Ruby Gems for 'r10k', 'CFPropertyList', 'sqlite3', and 'hiera-eyaml'. This creates a payload package with means client computers in a masterless setup do not need to download and compile the gems locally saving LOTS of time when re-imaging/first time setup.

The r10k file that is being copied to ``/usr/local/bin/r10k`` is due to SIP in El Capitan. Puppet 4.0 with the new puppet agent resolves this properly however at this time I am unable to upgrade from Puppet 3. 