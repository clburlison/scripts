
#!/bin/bash
# To use this script, simple type ./reposado-removeDeprecatedProductsFromDisk

# Place this script in the same folder as repoutil, otherwise it will not work properly.

# By default, repoutil --purge-product will print a warning and skip any products that
# are not deprecated or are in one or more branches.
# To override the warning and purge these products anyway, add '--force':


# Removes deprecated products
./repoutil --purge-product all-deprecated
