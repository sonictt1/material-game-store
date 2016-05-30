# material_game_store

A material design Django 1.9 app sell extra/duplicate keys from bundle deals. Please read the ToS on the sites where the keys originated before selling, unless you live in a jurisdiction where selling pre-owned software in protected by law. *Somes sites prohibit the resale of game keys.*

Uses the Apache 2.0 open source license.

## Features

- Stripe integration (all you need are your Stripe API keys)
- Open Source! Don't use Stripe? Fork my project and put in your own!
- Encrypts your keys using Google's Keyczar
- Material Design
- Responsive (tested on screens down to iPhone 5s size)
- Integrates into your already-existing Django website.

## Prerequisites
 
This app is intended to go into an already-existing *Django 1.9 project*. It is not yet installable with `pip install`, but I'm working on that.

For more info on how to start a Django project, [go here](https://docs.djangoproject.com/en/1.9/intro/tutorial01/).

You'll need the following set up for this app to work.
- [Keyczar for Python](https://github.com/google/keyczar) - [Instructions for Django](http://gpiot.com/blog/encrypted-fields-pythondjango-keyczar/)
- [Django Email (django.core.email)](https://docs.djangoproject.com/en/1.9/topics/email/)
- [Stripe Checkout](https://stripe.com/checkout) - Server API installable with `pip install stripe` or `easy_install stripe` - [More info about the Stripe API here](https://stripe.com/docs/libraries)


## To Install

After all of the prerequisites have been installed and configured, clone the repo into your Django project.
Add `material_game_store.apps.MaterialGameStoreConfig` to your `INSTALLED APPS`, then run `makemigrations` and `migrate` on your `manage.py`.

## Demo

Interested to see what it looks like? Check it out on my personal website https://tthompson.me/store.
