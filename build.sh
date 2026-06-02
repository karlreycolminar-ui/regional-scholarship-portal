#!/usr/bin/env bash
# Build script for Railway deployment

set -o errexit

python manage.py collectstatic --no-input
