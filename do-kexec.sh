#!/bin/sh

KEXEC=/sbin/kexec
usage()
{
	echo "Usage: do-kexec.sh /boot/bzImage [commandline options]"
	exit 1
}

if [ $# -lt 1 ]
then
	usage
fi

IMAGE=$1
shift
$KEXEC -l $IMAGE --command-line="$(cat /proc/cmdline) $*"
$KEXEC -e --command-line="$(cat /proc/cmdline) $*"
