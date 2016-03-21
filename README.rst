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

Installation & Testing
^^^^^^^^^^^^^^^^^^^^^^

``pip install bragly``

OR

``$ git clone https://github.com/huntcsg/bragly.git``

``$ python setup.py install``

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


.. |Build Status| image:: https://travis-ci.org/huntcsg/bragly.svg?branch=master
   :target: https://travis-ci.org/huntcsg/bragly
.. |Develop Build Status| image:: https://api.travis-ci.org/huntcsg/bragly.svg?branch=develop
   :target: https://travis-ci.org/huntcsg/bragly/branches
.. |Coverage Status| image:: https://coveralls.io/repos/github/huntcsg/bragly/badge.svg?branch=master
   :target: https://coveralls.io/github/huntcsg/bragly?branch=master
.. |Develop Coverage Status| image:: https://coveralls.io/repos/github/huntcsg/bragly/badge.svg?branch=develop
   :target: https://coveralls.io/github/huntcsg/bragly?branch=develop

