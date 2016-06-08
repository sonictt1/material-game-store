from __future__ import unicode_literals
from django.db import models
import datetime
import encryption
# Create your models here.

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

# Game SQL Object
class Game(models.Model):
    name = models.CharField(max_length=128, null=False)
    description = models.TextField()
    img_name = models.CharField(max_length=128)
    rating = models.CharField(max_length=1)
    price = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

# Keys for Games. key_text is the actual key for the game.
# game is a foreign key that relates the game the key unlocks back to the key
class Key(models.Model):
    key_text = encryption.EncryptedCharField(max_length=50, null=False, unique=True)
    claimed = models.BooleanField(default=False)
    game = models.ForeignKey(Game, null=False)
    service = models.CharField(max_length=10, null=False)
    claimed_by = encryption.EncryptedCharField(max_length=128, null=True, blank=True)
    date_added = models.DateField(default=datetime.date.today, null=False)
    hidden = models.BooleanField(default=False, null=False)

# FAQ for the FAQ page
class Faq(models.Model):
    question = models.TextField()
    answer = models.TextField()

# User email for mailing list
class Email(models.Model):
    email = models.CharField(null=False, max_length=254, unique=True)

class PushSubscriber(models.Model):
    sub_id = models.CharField(null=False, unique=True, max_length=170)
