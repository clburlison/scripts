First, I did not create this script nor do I know who did, else I would give credit **amazing original author**.

#The Goods

When using the AD-Plugin with OSX, group members in the "Allow administration by:" field will have administrative access on their machines when they can talk to the domain server. This is great except for when your users take their laptop home and they no longer have admin access. (a reboot will cause this situation).

![scripts](/ad-plugin.png)

This script requires you to change the ``DCSERVER="dccentral1.bisd.k12"`` variable to a valid domain controller and optionally add any ``CUSTOMGROUPS=()``. CustomGroups is for any group you want to have admin access but do not have in the "Allow administration by:" setting of the AD-Plugin.

This script needs to be ran as root. To automate the process I am providing a Makefile and LaunchDaemon. One discussion related to this topic [here](https://groups.google.com/forum/?fromgroups#!topic/macenterprise/wOM_KTnLr7A). 

_Note_: the script has a debug mode for you know...debugging issues.

##Requires

* the [luggage](https://github.com/unixorn/luggage) to build the package
* a system restart to load the LaunchDaemon
* the user that wants admin access to log in at least once at the network (allow the script to work)