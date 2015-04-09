#! /bin/bash

#----------------------------------------
#
#          	sethomeperm
#
#   Reset home folder permissions to
#		   defaults values
#
#	based on an original script from
#	Zack Smith zack@irisink.com
#
# feedback to: mail@adx-consulting.com
#
#	Version 1.0b0 -- Dec. 30, 2005
#	Version 1.0b1 -- Apr.  7, 2006
#	Version 1.0b2 -- Sep.  5, 2006
#	Version 2.0b1 -- Aug.  7, 2009
#	Version 2.0b2 -- Oct.  7, 2009
#	Version 2.0b3 -- Mar. 26, 2010
#	Version 2.0b4 -- Apr. 16, 2010
#	Version 2.0b5 -- Sep. 14, 2010
#	Version 2.1b1 -- Oct. 21, 2011
#	Version 2.1b2 -- Oct.  9, 2012
#	Version 2.1b3 -- Dec.  2, 2012
#
#----------------------------------------

scriptname=$(/usr/bin/basename "${0}")
scriptpdir=$(/usr/bin/dirname "${0}")
vnumber="v2.1b3"

version="${scriptname} ${vnumber}  --  (c) 2005-2012, ADX Consulting"
feedbck="feedback to: mail@adx-consulting.com"
help="no"
dmp="no"
logf="/tmp/sethomeperm.log"
user=""
psx="yes"
acl="yes"
uset="no"
sset="no"
hdir="/Users/"
hfldr=""

#########################
###### Subroutines ######
#########################

dump ()
{
	echo
	echo -e "   version =" ${version}
	echo -e "   feedbck =" ${feedbck}
	echo -e "   --------------------"
	echo -e "      help =" ${help}
	echo -e "       dmp =" ${dmp}
	echo -e "      logf =" ${logf}
	echo -e "      psx  =" ${psx}
	echo -e "      acl  =" ${acl}
	echo -e "      uset =" ${uset}
	echo -e "      sset =" ${sset}
	echo -e "   --------------------"
	echo -e "      user =" ${user}
	echo -e "      hdir =" ${hdir}
	echo -e "     hfldr =" ${hfldr}
	echo
}

help ()
{
	echo -e "\n"${version}
	echo -e ${feedbck}
	echo -e "Usage:"
	echo -e "\tsudo ${scriptname} [-h] | [-k] [-d <homedir>] -a | -u <user> [-p] [-w] [-r] [-s]"
	echo -e "where:"
	echo -e "\t-h:           prints this help then exit"
	echo -e "\t-k:           dumps script variables then exit"
	echo -e "\t-d <homedir>: directory containing the home folders."
	echo -e "\t                 (default is '/Users/')"
	echo -e "\t-a:           all user folders in the directory."
	echo -e "\t-u <user>:    specific user folder to reset."
	echo -e "\t-p:           applies POSIX permissions only (default: POSIX+ACL)"
	echo -e "\t-w:           applies ACL only (default: POSIX+ACL)"
	echo -e "\t-r:           resets '/Users' to default mode (root:admin 755)."
	echo -e "\t-s:           resets '/Users/Shared' to default mode (root:wheel 1777)."
	echo
}

over ()
{
	exit $1
}

err ()
{
	report "*** Error: $1"
	over 1
}

report ()
{
	echo -e "${1}"
	echo -e "${1}" >> ${logf}
}

chg_mod_own ()
{
# Variables mapping:
#	${1} = ${i}    == user's home folder
#	${2} = ${cusr} == user's name

	report "Handling ${1}..."

# Does the current user exist?
	testuser=$(id ${2} | grep "no such user")
	if [[ -n ${testuser} ]]
	then
#		The 'id' command returned 'no such user'
		report "User ${2} unknown, not processed"
	else
		chown -R ${2}:staff "${1}"
		
		if [[ ${acl} = "yes" ]]
		then
			chmod -R -N "${1}"
			chmod +a "group:everyone deny delete" "${1}"
			chmod +a "group:everyone deny delete" "${1}"/*
			report "   ACLs fixed..."
		fi

		if [[ ${psx} = "yes" ]]
		then
			chmod 755 "${1}"
			chmod -R u+r,u+w "${1}"/*
			chmod -R g-w "${1}"/*
			chmod -R o-w "${1}"/*
			chmod -R -X "${1}"/*
			chmod 700 "${1}"/*
		
			if [[ -d "${1}"/Public ]]
			then
				chmod -R 755 "${1}"/Public
				if [[ -d "${1}/Public/Drop Box" ]]
				then
					chmod 733 "${1}/Public/Drop Box"
				fi
			fi
		
			if [[ -d "${1}"/Sites ]]
			then
				chmod -R 755 "${1}"/Sites
			fi
		
			if [[ -d "${1}"/.ssh ]]
			then
				chmod -R 600 "${1}"/.ssh/*
			fi

			report "   POSIX permissions fixed..."
		fi

		if [[ $osversion -gt 6 ]]
		then
			# 'Library' folder hidden in 10.7.x and 10.8.x
			chflags hidden "${1}/Library"
			report "   Library folder hidden..."
		fi

		report "-- Home folder for user ${2} has been reset."
	fi
}


##############################
# Parameters parsing & tests #
##############################

if [[ $# -eq 0 ]]
then
	help
	over 0
fi

#Log file initialization
touch ${logf}
report "${version}"
report "Starting at: $(date)"

while getopts ":hkad:u:pwrs" OPTION
do
	case "${OPTION}" in
		h)	help="yes"
			;;
		k)	dmp="yes"
			;;
		d)	hdir=${OPTARG}
			;;
		a)	user="-"
			;;
		u)	user=${OPTARG}
			;;
		p)	acl="no" ; psx="yes"
			;;
		w)	acl="yes" ; psx="no"
			;;
		r)	uset="yes"
			;;
		s)	sset="yes"
			;;
		:)	err "Parameter ${OPTARG} requires an argument."
			;;
		\?)	err "Parameter ${OPTARG} not yet implemented."
			;;
	esac
done

if [[ ${help} = "yes" ]]
then
	help
	over 0
fi

# Which OS version?
# returns 6 for 10.6.x, 7 for 10.7.x, etc.
osversion=$(sw_vers -productVersion | awk -F\. '{print $2}')

# Do we have enough privileges to run that script?
if [[ $(id -un) != "root" ]]
then
	err "You must be root to run this script."
fi

# Does this home directory exist?
if [[ ! -d ${hdir} ]]
then
	err "${hdir}: No such a directory"
else
#	It exists so let's remove the trailing slash, if any
	hfldr="$(echo ${hdir} | sed s/"\/$"//g)"
fi

# Is the user defined?
if [[ ${user} = "" ]]
then
	err "User undefined."
fi

# Does the user home folder exist?
if [[ ${user} != "-" ]]
then
	if [[ ! -d "${hfldr}/${user}" ]]
	then
		err "${hfldr}/${user} doesn't exist."
	fi
fi

if [[ ${dmp} = "yes" ]]
then
	dump
	over 0
fi

#####################
# ok, here we go... #
#####################

if [[ ${user} = "-" ]]
then
	# Loop thru all users
	for i in ${hfldr}/*
	do
		if [[ -d "${i}/Library/" ]]
		then
			cusr=$(echo ${i##*/})
			chg_mod_own ${i} ${cusr}
		else
			report "Skipping ${i}, as it has no Library folder."
		fi
	done
else
	chg_mod_own "${hfldr}/${user}" ${user}
fi

if [[ ${uset} = "yes" ]]
then
	# Resetting '/Users' folder
	chown root:admin "${hfldr}"
	chmod 755 "${hfldr}"
	report "${hfldr} folder reset."
else
	report "${hfldr} folder not reset."
fi

if [[ ${sset} = "yes" && -d "${hfldr}/Shared" ]]
then
	# Resetting '/Users/Shared' folder
	chown root:wheel "${hfldr}/Shared"
	chmod 1777 "${hfldr}/Shared"
	report "${hfldr}/Shared folder reset."
else
	report "${hfldr}/Shared folder not reset."
fi

report "Done at: $(date) \n"

over 0
