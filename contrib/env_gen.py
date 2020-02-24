#!/usr/bin/env python

"""
Simple .env generator.
"""

CONFIG_STRING = """# Basic SetUp
# Database
DATABASE_URL=postgres://postgres:postgres@localhost/postgres

# Quandl
QUANDL_KEY=
"""

# Writing our configuration file to '.env'
with open('.env', 'w') as configfile:
    configfile.write(CONFIG_STRING)
