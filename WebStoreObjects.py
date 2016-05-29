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


class GameWithKeys:
    def __init__(self, game, is_steam, is_uplay, is_origin):
        self.id = game.pk
        self.name = game.name
        self.price = game.price
        self.description = game.description
        self.img_location = game.img_name
        self.rating = game.rating
        self.has_steam = is_steam
        self.has_uplay = is_uplay
        self.has_origin = is_origin

    def name(self):
        return self.name

    def price(self):
        return self.price

    def id(self):
        return self.id

    def img_location(self):
        return self.img_location

    def description(self):
        return self.img_location

    def rating(self):
        return self.rating

    def has_steam(self):
        return self.has_steam

    def has_origin(self):
        return self.has_origin

    def has_uplay(self):
        return self.has_uplay

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __cmp__(self, other):
        return cmp(self.name, other.name)
