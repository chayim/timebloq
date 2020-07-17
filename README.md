# timebloq

Focusing can be difficult, and every little bit helps; enter timebloq. timebloq is a python script that helps you allow and deny individual hosts for periods of time. The idea is that you might want to block certain websites during work hours, our others whilst at home.  Either way, timebloq is designed to be a lightweight way to do it.

## How It Works

timebloq edits your /etc/hosts to add and remove entries. Entries are added one per line, and point to 0.0.0.0.  timebloq assumes it has control of the end of your hosts file.  Simply edit the sample.json file and you're good to go.

## Requirements

Python 3. No libraries.

## Running manually

python timebloq.py -h is your friend:


    Usage: timebloq.py [options]

    Options:
      -h, --help            show this help message and exit
      -c, --clear           Clear blocked sites
      -i, --install         Install blocked sites
      -s, --show            Set to show what would be blocked
      -f FILE, --file=FILE  config file

## Installation

1. Clone the repository - there are no dependencies.
2. Edit the sample file
3. Add a cronjob to run as root. eg: ("*/5 * * * * python timebloq.py -f /path/to/your.config -i")
