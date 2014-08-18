First, I did not create this script nor do I know who did, else I would give credit **amazing original author**.

#The Goods

When using the AD-Plugin with OSX, group members in the "Allow administration by:" field will have administrative access on their machines when they can talk to the domain controller. This is great, except for when your users take their laptop home and they no longer have admin access. (a reboot will cause this situation).

![scripts](/LocalAdminMembershipUpdater/ad-plugin.png)

Add any Custom Groups to the following variable ``CUSTOMGROUPS=()``. CustomGroups is for any group you want to have admin access without being in the "Allow administration by:" variable of the AD-Plugin.

Once the script has been ran successfully any Admin users that should have admin access with maintain admin access once off of the domain. Uncomment lines 107-108 if you wish to maintain the default behavior of OS X.


This script needs to be ran as root. To automate the process I am providing a Makefile and LaunchDaemon. The LaunchDaemon, by default, is set to run on every network change which may need modification depending on your requirements. 

_Note_: the script has a debug mode for you know...debugging issues.

##Requires

* the [luggage](https://github.com/unixorn/luggage) to build the package
* a system restart to load the LaunchDaemon
* the user that wants admin access to log in at least once at the network (allow the script to work)


Discussion related to this topic [here](https://groups.google.com/forum/?fromgroups#!topic/macenterprise/wOM_KTnLr7A). 