/*
*
*  Push Notifications codelab
*  Copyright 2015 Google Inc. All rights reserved.
*
*  Licensed under the Apache License, Version 2.0 (the "License");
*  you may not use this file except in compliance with the License.
*  You may obtain a copy of the License at
*
*      https://www.apache.org/licenses/LICENSE-2.0
*
*  Unless required by applicable law or agreed to in writing, software
*  distributed under the License is distributed on an "AS IS" BASIS,
*  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
*  See the License for the specific language governing permissions and
*  limitations under the License
*
*/

'use strict';

var reg;
var sub;
var isSubscribed = false;
var subscribeButton = document.getElementById('toggle_notifications');

if ('serviceWorker' in navigator) {
  console.log('Service Worker is supported');
  navigator.serviceWorker.register('/store/push_notifications.js').then(function() {
    return navigator.serviceWorker.ready;
  }).then(function(serviceWorkerRegistration) {
    reg = serviceWorkerRegistration;
    subscribeButton.disabled = false;
    console.log('Service Worker is ready :^)', reg);
  }).catch(function(error) {
    console.log('Service Worker Error :^(', error);
  });
}

subscribeButton.addEventListener('click', function() {
  if (isSubscribed) {
    unsubscribe();
  } else {
    subscribe();
  }
});

function subscribe() {
  reg.pushManager.subscribe({userVisibleOnly: true}).
  then(function(pushSubscription) {
    sub = pushSubscription;
    console.log('Subscribed! Endpoint:', sub.endpoint);
    subscribeButton.checked = true;
    isSubscribed = true;
    var subscriberId = sub.endpoint.split("/").slice(-1);
    $.get('/store/api/add_subscriber/', {"subscriberId": subscriberId});
  });
}

function unsubscribe() {
  sub.unsubscribe().then(function(event) {
    subscribeButton.textContent = 'Subscribe';
    console.log('Unsubscribed!', event);
    isSubscribed = false;
    var subscriberId = sub.endpoint.split("/").slice(-1);
    $.get('/store/api/remove_subscriber/', {"subscriberId": subscriberId});
  }).catch(function(error) {
    console.log('Error unsubscribing', error);
    subscribeButton.checked = false
    ;
  });
}

function checkSubscription(serviceWorkerRegistration) {
    // Do we already have a push message subscription?
   serviceWorkerRegistration.pushManager.getSubscription()
     .then(function(subscription) {
       // Enable any UI which subscribes / unsubscribes from
       // push messages.
       subscribeButton.disabled = false;

       if(!subscription) {
         subscriptButton.checked = false;
         console.log("Note Subscribed", subscription);
         return;
       }
       console.log("Subscribed", subscription);
       subscribeButton.checked = true;
     })
 }
