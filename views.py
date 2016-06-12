from django.template import loader
from django.http import HttpResponse
from django.core.mail import send_mail
from django.db import transaction
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from WebStoreObjects import GameWithKeys
from models import Game
from models import Key
from models import Faq
from models import Email
from models import PushSubscriber
import stripe
# Below secret_data.py file is not provided, you must make this yourself.
# Put your secret and publishable Stripe keys in that file.
# secret_data.py is in the .gitignore file so you won't accidentally commit it.
import secret_data

# APACHE 2.0 LICENSE
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# Create your views here.

# Front page, which displays a list of games.
# First page a user will see.
def index(request):
    email = request.GET.get('email', False)
    operation = request.GET.get('op', 'add')
    order = request.GET.get('order', False)

    if email:
        if operation == 'add':
            try:
                email_model = Email(email=email)
                email_model.save()
                email = True
            except IntegrityError:
                pass
        elif operation == 'remove':
            try:
                email_model = Email.objects.get(email=email)
                email_model.delete()
                email = True
            except ObjectDoesNotExist:
                pass

    template = loader.get_template('store/game_list.html')
    drm = request.GET.get('drm', None)
    query = request.GET.get('query', None)

    if order == 'new':
        games = sorted(get_games_with_keys(drm=drm, query=query, new=True))
    else:
        games = sorted(get_games_with_keys(drm=drm, query=query))


    context = {
        'game_list': games,
        'drm': drm,
        'query': query,
        'email_added': email,
        'email_op': operation
    }
    return HttpResponse(template.render(context, request))

# Page that shows details about the game and allows user to purchase the game.
# The second page in the key purchasing process.
def game_detail(request, game_id):
    template = loader.get_template('store/game_details.html')
    game = Game.objects.get(pk=game_id)
    context = {
        'game_title': game.name,
        'game_description': game.description,
        'game_image': game.img_name,
        'game_price': '${:.2f} USD'.format(get_adjusted_price(game.price)),
        'game_price_num': get_adjusted_price(game.price),
        'game_price_num_int': int(round(get_adjusted_price(game.price)*100)),
        'game_with_keys': get_game_with_keys_for_game(game),
        # Set this in a file called secret_data.py. secret_data.py is in the .gitignore so you won't accidentally commit it to a db.
        # STRIPE_KEY_PUBLISHABLE should be the test key on your machine, and the production key on your server
        'stripe_key': secret_data.STRIPE_KEY_PUBLISHABLE,
    }
    return HttpResponse(template.render(context, request))

# Page that displays after purchase and shows error or success.
# Last page the user will see before being prompted to go back home.
# game_id is the primary key of a Game object.
def checkout_page(request, game_id):
    template = loader.get_template('store/post_purchase.html')
    drm = request.POST["drm"]
    add_to_list = request.POST.get('email-list', False)
    email = 'no email'
    game = get_game_with_keys_for_game(Game.objects.get(pk=game_id))

    # Make sure nobody has taken the key while the user was looking at the
    # game detail page.
    key = get_first_unclaimed_key(game, drm)
    has_key = True
    if key == -1:
        has_key = False
    code = None


    if has_key:
        # Set your secret key: remember to change this to your live secret key in production
        # See your keys here https://dashboard.stripe.com/account/apikeys
        # Set this in a file called secret_data.py. secret_data.py is in the .gitignore so you won't accidentally commit it to a db.
        # STRIPE_KEY_SECRET should be the test key on your machine, and the production key on your server
        stripe.api_key = secret_data.STRIPE_KEY_SECRET
        # Get the token generated by stripe.js
        token = request.POST['stripeToken']

        # Try to create the charge on Stripe's servers - this will charge the user's card
        try:
            charge = stripe.Charge.create(
                amount=int(round(get_adjusted_price(game.price)*100)),  # amount in cents, again
                currency="usd",
                source=token,
                description=game.name
            )
            # User email is retrieved from Stripe.
            email = get_email_from_transaction(token)

            # Follow the instructions at:
            #
            # https://docs.djangoproject.com/en/1.9/topics/email/
            #
            # to properly set up Django's email capabilities.
            #
            # Email is required for users to get their keys, although it will display
            # in plain text if email fails for some reason.
            #
            # Replace email@example.com with your email after you've properly
            # gotten Django's email service set up. You might consider putting
            # this email in your secret_data.py file as well.
            #
            # Change fail_silently to False for debugging.
            email_succeeded = send_mail('Your game key', 'You ordered ' + game.name + ' for ' + drm + '. Your key is: ' + key.key_text,
                                        secret_data.EMAIL_ADDRESS, [email], fail_silently=True)

            # Remember who claimed a key. Useful if a user needs you to re-send keys.
            key.claimed_by = email
            key.save()

            # Fallback if email fails.
            if email_succeeded < 1:
                code = key.key_text
            status = True
            message = None
        except stripe.error.CardError, e:
            # The card has been declined
            status = False
            message = e.args
            email_succeeded = -1
            # IMPORTANT: This marks the key as available again.
            key.claimed = False
            key.save()
            pass
        except stripe.error.StripeError, e:
            # Some other Stripe error.
            status = False
            message = e.args
            email_succeeded = -1
            # IMPORTANT: This marks the key as available again.
            key.claimed = False
            key.save()
            pass
    else:
        # Somebody else got the key first, or something else unexpected happened.
        status = False
        email_succeeded = -1
        message = 'Sorry but the key seems to have been taken. You have not been charged.'

    # If user indicated that they'd like to be added to the emailing list, add them.
    if add_to_list and status and email_succeeded > -1:
        try:
            model_email = Email(email=email)
            model_email.save()
        except IntegrityError:
            pass

    context = {
        'errors': message,
        'transaction_status': status,
        'game_price_num': '{:.2f}'.format(get_adjusted_price(game.price)),
        'game_title': game.name,
        'game_description': game.description,
        'game_price': '${:.2f} USD'.format(get_adjusted_price(game.price)),
        'drm': drm,
        'email': email_succeeded,
        'attempted_email': email,
        'code': code,
        'list': add_to_list,
        # Below key should be "pk_test_xxxxxxxxxx" for test,
        # or "pk_live_xxxxxxxxx" for production. Save it in a
        # secret_data file to prevent accidental committing to
        # a repo.
        'stripe_key': secret_data.STRIPE_KEY_PUBLISHABLE,
    }
    return HttpResponse(template.render(context, request))

# Page that displays FAQs for the web store.
def faq(request):
    template = loader.get_template('store/faq.html')
    faqs = Faq.objects.all()
    context = {'faq_list': faqs}
    return HttpResponse(template.render(context, request))

def push_notifications(request, js):
    template = loader.get_template('store/push_notifications.js')
    html = template.render()
    return HttpResponse(html, content_type="application/x-javascript")

def add_subscriber(request):
    subscriberId = request.GET['subscriberId[]']
    newSubscriber = PushSubscriber(sub_id=subscriberId)
    newSubscriber.save()
    return HttpResponse('{"status": "success"}')

def remove_subscriber(request):
    subscriberId = request.GET['subscriberId[]']
    currentSubscriber = PushSubscriber.objects.get(sub_id=subscriberId)
    currentSubscriber.delete()
    return HttpResponse('{"status": "success"}')

# Gets keys from DB.
# drm filters by service (ex. "steam", "origin", "uplay")
# query filters by name (ex. query="co" could return "Counter-Strike: Global Offensive" but not "Far Cry 3")
def get_games_with_keys(drm=None, query=None, new=False):
    games_with_keys = list()

    if new:
        games = get_new_games_from_db()
    else:
        games = get_games_from_db()

    #TODO replace giant conditional tree with clever ORM line instead
    for game in games:
        game_with_key = get_game_with_keys_for_game(game)
        if game_with_key.has_steam or game_with_key.has_origin or game_with_key.has_uplay:
            if drm is None or drm == 'all':
                if query is None or query == '':
                    games_with_keys.append(game_with_key)
                elif query.lower() in game_with_key.name.lower():
                    games_with_keys.append(game_with_key)
            elif drm == 'steam' and game_with_key.has_steam:
                if query is None or query == '':
                    games_with_keys.append(game_with_key)
                elif query.lower() in game_with_key.name.lower():
                    games_with_keys.append(game_with_key)
            elif drm == 'origin' and game_with_key.has_origin:
                if query is None or query == '':
                    games_with_keys.append(game_with_key)
                elif query.lower() in game_with_key.name.lower():
                    games_with_keys.append(game_with_key)
            elif drm == 'uplay' and game_with_key.has_uplay:
                if query is None:
                    games_with_keys.append(game_with_key)
                elif query.lower() in game_with_key.name.lower():
                    games_with_keys.append(game_with_key)
    return games_with_keys

# Returns an object that tells you for what services you have unclaimed keys.
def get_game_with_keys_for_game(game):
    is_steam = False
    is_uplay = False
    is_origin = False
    keys = Key.objects.filter(game_id=game.pk, claimed=False, hidden=False)
    for key in keys:
        if key.service == 'steam':
            is_steam = True
        elif key.service == 'uplay':
            is_uplay = True
        elif key.service == 'origin':
            is_origin = True
    return GameWithKeys(game, is_steam, is_uplay, is_origin)


# Gets the customer email from the Stripe transaction.
# token is the transaction token from Stripe
def get_email_from_transaction(token):
    try:
        return stripe.Token.retrieve(token)['email']
    except stripe.error.InvalidRequestError, e:
        return stripe.BitcoinReceiver.retrieve(token)['email']

# Returns the first key unclaimed for the given service.
# game_with_keys is the game object that we want a key for.
# drm is the service we want the key for. (ex. "steam", "origin", "uplay")
def get_first_unclaimed_key(game_with_keys, drm):
    with transaction.atomic():
        keys = Key.objects.select_for_update().filter(game_id=game_with_keys.id, service=drm)
        for key in keys:
            if key.claimed is False:
                if key.service == drm:
                    key.claimed = True
                    key.save()
                    return key
        keys.update()
    return -1

# Quick convienience method that retuns list of all games from db.
def get_games_from_db():
    games = Game.objects.filter()
    return games

def get_new_games_from_db():
    ref_key = Key.objects.latest('date_added')
    keys = Key.objects.filter(date_added=ref_key.date_added)
    games = list()

    for key in keys:
        games.append(key.game)

    return games

# Method to DRY out price conversions.
def get_adjusted_price(price):
    return price * 1.029 + .3
