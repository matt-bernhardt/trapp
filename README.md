# Trapp

[![Build Status](https://travis-ci.org/matt-bernhardt/trapp.svg)](https://travis-ci.org/matt-bernhardt/trapp) [![Coverage Status](https://coveralls.io/repos/matt-bernhardt/trapp/badge.svg?branch=main&service=github)](https://coveralls.io/github/matt-bernhardt/trapp?branch=main) [![Code Climate](https://codeclimate.com/github/matt-bernhardt/trapp/badges/gpa.svg)](https://codeclimate.com/github/matt-bernhardt/trapp)

Trapp is a Python project for linking, analyzing, and extending soccer data.

Trapp provides several tools for the user to work with soccer data:

1. Importer
2. Compiler
3. Renderer

Each of these will be described in more detail as the project progresses. For now, efforts are focused on the first tool, an importer capable of harvesting spreadsheet data into the appropriate database tables.

## Installing

My hope is that this project can be installed in a comparable way to other python libraries. When I do so myself, the steps look like this:

```
git clone git@github.com:matt-bernhardt/trapp.git
cd trapp
pip install -r requirements.txt
python setup.py install
```

Following this, I establish the database credentials - which exist as four environment variables:

* TRAPP_DBHOST
* TRAPP_DBPWD
* TRAPP_DBSCHEMA
* TRAPP_DBUSER

For confirmation that everything is ready to go, the `check-db` verb is useful. The output should look something like:

```
(myvenv) $ trapp -v check-db
Checking database connection

Credentials:
dbuser:   username
dbpwd:    password
dbhost:   host
dbschema: schema

<mysql.connector.connection.MySQLConnection object at 0x7ff2988f02b0>
MySQLCursorBuffered: (Nothing executed yet)
Warnings: None
```

## For more information

More information about this project can be found on the [Massive Report Data blog](http://www.massivereportdata.com/blog). To contact the author, please email Matt Bernhardt at matt [at] massivereportdata [dot] com or on Twitter at [@BernhardtSoccer](https://twitter.com/bernhardtsoccer).