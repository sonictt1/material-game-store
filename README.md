# material_game_store

A material design Django 1.9 app sell extra/duplicate keys from bundle deals. Please read the ToS on the sites where the keys originated before selling, unless you live in a jurisdiction where selling pre-owned software in protected by law. *Somes sites prohibit the resale of game keys.*

[Provided under the Apache 2.0 license](https://tldrlegal.com/license/apache-license-2.0-(apache-2.0)).

## Features

- Stripe integration (all you need are your Stripe API keys)
- Open Source! Don't use Stripe? Fork my project and put in your own!
- Encrypts your keys using Google's Keyczar
- Material Design
- Responsive (tested on screens down to iPhone 5s size)
- Integrates into your already-existing Django website.
- Games are searchable and may be filtered by service ([Steam](http://store.steampowered.com/), [Origin](https://www.origin.com/en-us/store/), and [UPlay](https://uplay.ubi.com/#!/en-US/))
- Comes with some images for games.

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

After installation you'll want to create a file in the app root named `secret_data.py` and put your Stripe keys in there. `STRIPE_KEY_SECRET` and `STRIPE_KEY_PUBLISHABLE` for your secret and publishable keys, respectively. Test keys should be used for development and production keys on your server. If done correctly, Stripe should work after this is done.

## Add Keys for Sale

- First, find an image for the game you want to sell and put it in `static/game_img/` directory (remember the file name and don't forget to `python manage.py collectstatic`)
- Second, add the game your key is for in Django's admin panel (Game object, you'll put that file name from step one here).
- Last, add the key for the game in the first step in the admin panel (Key object, leave `claimed` unchecked and `claimed_by` blank).
- It should now be visible on your store's front page.

## Demo

Interested to see what it looks like? Check it out on my personal website https://tthompson.me/store.
