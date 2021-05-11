#!/bin/bash

/usr/local/bin/celery -A tasks worker --loglevel=info
