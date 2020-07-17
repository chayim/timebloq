#!/usr/bin/env python

from optparse import OptionParser
import os
import sys
import json
import datetime


HOSTSFILE = "/etc/hosts"
HEADER = "### BEGIN TIMEBLOQ ###"


class TimeBloq:

    def __init__(self, conffile=os.path.abspath(os.path.join(os.path.expanduser("~"), ".timebloq.conf"))):
            self.CONFFILE = conffile

    def _parse_hosts(self):
        hosts = []
        with open(HOSTSFILE) as res:
            hosts = res.read().split(HEADER)[0].split("\n")
        return hosts

    def install(self, hosts=None):
        self.clear()
        if hosts is None:
            current = self._parse_hosts()
            newhosts = self._config()
            hostdata = current + ["", HEADER] + newhosts
        else:
            hostdata = hosts
        with open(HOSTSFILE, "w+") as fp:
            fp.write('\n'.join(hostdata).strip())

    def clear(self):
        hostdata = self._parse_hosts()
        with open(HOSTSFILE, "w+") as fp:
            fp.write('\n'.join(hostdata).strip())

    def show(self):
        current = self._parse_hosts()
        newhosts = self._config()
        hostdata = current + newhosts

        sys.stderr.write("The following sites would be added to %s\n\n" % HOSTSFILE)
        sys.stderr.write('\n'.join(hostdata))

    def _config(self):

        blockhosts = []
        now = datetime.datetime.now()
        with open(self.CONFFILE) as fp:
            cfg = json.loads(fp.read())

        for c in cfg:

            host = c["host"]
            if c.get("blockbetween", None) is None:
                blockhosts.append("0.0.0.0 %s" % host)
                continue

            for h in c.get("blockbetween"):
                times = h.split("-")
                start = times[0]
                end = times[1]

                start_hour = int(start[:2])
                start_minute = int(start[2:])
                end_hour = int(end[:2])
                end_minute = int(end[2:])

                if now >= now.replace(hour=start_hour, minute=start_minute) and now <= now.replace(hour=end_hour, minute=end_minute):
                    blockhosts.append("0.0.0.0 %s" % host)

        return blockhosts

if __name__ == "__main__":

    if os.getuid() != 0:
        sys.stderr.write("This application must run as root.\n")
        sys.exit(3)

    p = OptionParser()
    p.add_option("-c", "--clear", dest="CLEAR", action="store_true", default=False, help="Clear blocked sites")
    p.add_option("-i", "--install", dest="INSTALL", action="store_true", default=False, help="Install blocked sites")
    p.add_option("-s", "--show", dest="SHOW", action="store_true", default=False, help="Set to show what would be blocked")
    p.add_option("-f", "--file", dest="FILE", help="config file", default=None)

    opts, args = p.parse_args()
    if opts.CLEAR is False and opts.INSTALL is False and opts.SHOW is False:
        sys.stderr.write("Please specify an action\n")
        p.print_help()
        sys.exit(3)

    if opts.FILE is not None:
        t = TimeBloq(opts.FILE)
    else:
        t = TimeBloq()

    if opts.SHOW:
        t.show()
        sys.exit(0)

    if opts.INSTALL:
        t.install()
        sys.exit(0)

    if opts.CLEAR:
        t.clear()
        sys.exit(0)
