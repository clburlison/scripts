#!/usr/bin/python

from __future__ import print_function
import csv
import plistlib
import sys
import os
import io
import pprint
import glob

CSV_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'names.csv')
MANIFESTS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             'manifests')
pp = pprint.PrettyPrinter(indent=2)


def update_manifest_fields(manifest, row=None):
    """Takes a manifest dictionary and updates the fields. Creating blank
    entires so everything is uniform or addding data from the CSV file like
    asset tag."""
    # pp.pprint(manifest)
    installs = ['managed_installs',
                'managed_uninstalls',
                'managed_updates',
                'optional_installs']
    # Make our empty arrays if they don't exist so it's uniform
    for array in installs:
        if manifest.get(array) is None:
            manifest[array] = []

    # Birdville Speical keys
    special = ['asset', 'display_name', 'user']
    for arr in special:
        if manifest.get(arr) is None:
            try:
                if row.get(arr) is not None:
                    manifest[arr] = row[arr]
            except(AttributeError):
                manifest[arr] = ''
    return manifest


def eprint(*args, **kwargs):
    """Print to stderr http://stackoverflow.com/a/14981125/4811765"""
    print(*args, file=sys.stderr, **kwargs)


def main():
    """For all serials in CSV_FILE we will create a manifest with the proper
    munki fields and add missing data to the manifest if not present."""
    csvfile = io.open(CSV_FILE, 'rbU')
    csv_data = csv.DictReader(csvfile, delimiter=',')
    for row in csv_data:
        manifest = {}
        serial_manifest = os.path.join(MANIFESTS_DIR, row['serial'])
        if os.path.isfile(serial_manifest):
            # The manifest file does exist. We will update fields.
            manifest = plistlib.readPlist(serial_manifest)
            # Update all the fields and add meta data
            manifest = update_manifest_fields(manifest, row)
            # Write the updated manifest to disk
            plistlib.writePlist(manifest, serial_manifest)
        else:
            # The manifest file doesn't exist. We will create a blank
            # manifest and add the data from the csv file. We also want to
            # try and delete the named manifest if it exists.
            serial_manifest = os.path.join(MANIFESTS_DIR, row['serial'])
            named_manifest = os.path.join(MANIFESTS_DIR, row['name'])
            if os.path.isfile(named_manifest):
                # We have a manifest on disk as the computer name
                manifest = plistlib.readPlist(named_manifest)
                # Update all the fields and add meta data
                manifest = update_manifest_fields(manifest, row)
                # Write the updated manifest to disk
                plistlib.writePlist(manifest, serial_manifest)

                # Remove the old named manifest file from disk DANGERZONE
                os.remove(named_manifest)
                print("File '{0}' with serial '{1}' has been removed"
                      .format(
                        os.path.basename(named_manifest),
                        row['serial'])
                      )
            else:
                # We are creating a blank manifest for this machine.
                # Potentally scary town.
                manifest = {'included_manifests': []}
                # Update all the fields and add meta data
                manifest = update_manifest_fields(manifest, row)
                # Write the updated manifest to disk
                plistlib.writePlist(manifest, serial_manifest)
                eprint("WARN: This manifest was created from scratch for "
                       "serial '{0}'".format(row['serial']))

    csvfile.close()

    # Update the remainding manifest files to have the same uniform items
    for manifest_file in os.listdir(MANIFESTS_DIR):
        if not manifest_file.startswith('.'):
            try:
                manifest = plistlib.readPlist(os.path.join(MANIFESTS_DIR,
                                              manifest_file))
                # Update all the fields
                manifest = update_manifest_fields(manifest)
                # Write the updated manifest to disk
                plistlib.writePlist(manifest, os.path.join(MANIFESTS_DIR,
                                                           manifest_file))
            except(IOError):
                pass


if __name__ == '__main__':
    main()
