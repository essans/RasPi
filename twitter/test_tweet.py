#!/usr/bin/env python

import os
import subprocess

from twython import Twython

from auth import(
	api_key,
	api_secret_key,
	access_token,
	access_token_secret
)

twitter = Twython(
	api_key,
	api_secret_key,
	access_token,
	access_token_secret
)


message = "Test tweet from RasPi"

twitter.update_status(status=message)
