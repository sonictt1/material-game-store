from django.conf.urls import url
from . import views

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

urlpatterns = [
    # Store home page
    url(r'^$', views.index, name='index'),
    # Game detail page
    url(r'^(?P<game_id>[0-9]+)/$', views.game_detail, name='game details'),
    # Checkout page
    url(r'^(?P<game_id>[0-9]+)/checkout/$', views.checkout_page, name='checkout'),
    # FAQ page
    url(r'^faq/', views.faq, name='faq'),
    # Endpoint to add push notification subscriber
    url(r'^api/add_subscriber/', views.add_subscriber, name="add push notification subscriber"),
    # Endpoint to remove push notification subscriber
    url(r'^api/remove_subscriber/', views.remove_subscriber, name="remove push notification subscriber")
    url(r'^push_notifications(.*.js)$', views.push_notifications, name="push notification endpoint")
]
