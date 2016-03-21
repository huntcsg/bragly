bragly
======

+--------------+-----------------+-------------+
| Branch       | Build Status    | Coverage    |
+==============+=================+=============+
| master       | |Build Status|  | |Coverage   |
|              |                 | Status|     |
+--------------+-----------------+-------------+
| develop      | |Develop Build  | |Develop    |
|              | Status|         | Coverage    |
|              |                 | Status|     |
+--------------+-----------------+-------------+

A command line tool to help remind you of your accomplishments

Limitations
^^^^^^^^^^^
Currently, only the "files" persistence mechanism is implemented. Any other
method will raise a NotImplemented exception.

Installation
^^^^^^^^^^^^

``pip install bragly``

OR

``$ git clone https://github.com/huntcsg/bragly.git``

``$ python setup.py install``

After installation be sure to run the following command so that your file/s will
be in the right place.

``$ brag-util init``

Base executable
^^^^^^^^^^^^^^^

::

    $ brag --help
    usage: brag [-h] {w,r,s} ...

    positional arguments:
      {w,r,s}     sub command help
        w         Write a new brag entry
        r         Read a group of brag entries
        s         Search for a group of brag entries

    optional arguments:
      -h, --help  show this help message and exit

Write
^^^^^

e.g. -
``brag w Went to seminar, taught mini class to co-workers --tags help teach``
-
``brag w Found bug in caching code, let relevant team know --tags network help debug``

::

    $ brag w --help
    usage: brag w [-h] [-t [TAGS [TAGS ...]]] [-d TIMESTAMP] message [message ...]

    positional arguments:
      message               The brag message

    optional arguments:
      -h, --help            show this help message and exit
      -t [TAGS [TAGS ...]], --tags [TAGS [TAGS ...]]
                            The tags associated with this brag message
      -d TIMESTAMP, --timestamp TIMESTAMP
                            The time stamp to use for this entry, in ISO-8601
                            format

Read
^^^^

::

    $ brag r --help
    usage: brag r [-h] [-s START] [-p PERIOD | -e END] [-f FORM]

    optional arguments:
      -h, --help            show this help message and exit
      -s START, --start START
                            The start time for getting entries
      -p PERIOD, --period PERIOD
                            The time period after the start datetime to get
                            entires. One of hour, day, week, month, year
      -e END, --end END     The end time for getting entries
      -f FORM, --form FORM  The format to display the results in. One of json,
                            json-pretty, log. Default: json

Search
^^^^^^

::

    $ brag s --help
    usage: brag s [-h] [-s START] [-p PERIOD | -e END] [-t [TAGS [TAGS ...]]]
                  [-x [TEXT [TEXT ...]]] [-f FORM]

    optional arguments:
      -h, --help            show this help message and exit
      -s START, --start START
                            The start time for getting entries
      -p PERIOD, --period PERIOD
                            The time period after the start datetime to get
                            entires. One of hour, day, week, month, year
      -e END, --end END     The end time for getting entries
      -t [TAGS [TAGS ...]], --tags [TAGS [TAGS ...]]
                            Tags you want to search for
      -x [TEXT [TEXT ...]], --text [TEXT [TEXT ...]]
                            Keywords you want to search for
      -f FORM, --form FORM  The format to display the results in. One of json,
                            json-pretty, log. Default: json


Utility Script
^^^^^^^^^^^^^^

::

   $ brag-util --help
   usage: brag-util [-h] {init} ...

   positional arguments:
     {init}      sub command help
       init      Initialize brag. If you want a different location for brag than
                 /home/hunter/.brag than be sure to set BRAG_DIR environmental
                 variable. If you want a different location for the configuration
                 file then be sure to set BRAG_CONFIG_PATH to something other
                 than /home/hunter/.brag/config.ini

   optional arguments:
     -h, --help  show this help message and exit


brag-util init
^^^^^^^^^^^^^^

::

   $ brag-util init --help
   usage: brag-util init [-h] [-m {reldb,files,mongodb}] [-c]

   optional arguments:
     -h, --help            show this help message and exit
     -m {reldb,files,mongodb}, --mechanism {reldb,files,mongodb}
                           Select the persistence mechanism. Default: files.
     -c, --clobber         If set, overwrites existing configuration files.



.. |Build Status| image:: https://travis-ci.org/huntcsg/bragly.svg?branch=master
   :target: https://travis-ci.org/huntcsg/bragly
.. |Develop Build Status| image:: https://api.travis-ci.org/huntcsg/bragly.svg?branch=develop
   :target: https://travis-ci.org/huntcsg/bragly/branches
.. |Coverage Status| image:: https://coveralls.io/repos/github/huntcsg/bragly/badge.svg?branch=master
   :target: https://coveralls.io/github/huntcsg/bragly?branch=master
.. |Develop Coverage Status| image:: https://coveralls.io/repos/github/huntcsg/bragly/badge.svg?branch=develop
   :target: https://coveralls.io/github/huntcsg/bragly?branch=develop

