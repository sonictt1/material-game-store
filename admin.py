from django.contrib import admin
from actions import export_as_csv_action
from actions import notify_users_new_games_action
from models import Game
from models import Key
from models import Faq
from models import Email
from models import PushSubscriber
# Register your models here.

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

# Below admin clases make the admin page more readable.

class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

admin.site.register(Game, GameAdmin)


class KeyAdmin(admin.ModelAdmin):
    list_display = ('game', 'claimed', 'claimed_by')


admin.site.register(Key, KeyAdmin)


class FaqAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')


admin.site.register(Faq, FaqAdmin)

# Includes action to export emails as CSV for easy emailing.
class EmailAdmin(admin.ModelAdmin):
    list_display = ['email']
    actions = [export_as_csv_action("Export Emails as CSV", fields=['email'])]


admin.site.register(Email, EmailAdmin)

class PushSubscriberAdmin(admin.ModelAdmin):
    actions = [notify_users_new_games_action()]

admin.site.register(PushSubscriber, PushSubscriberAdmin)
