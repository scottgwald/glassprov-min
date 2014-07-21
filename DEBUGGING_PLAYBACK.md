# Debugging glassprov_playback.py

* connected callback gets called over and over

Hypotheses:

1. There's bouncing back and forth between the python client
   and the javascript client

2. There is something goofy about how the passing back and forth of 
   subscription messages causes the wearscript callback to fire
   repeatedly.

Ruled out reconnecting-websocket because the problem happens without
it. 

Strategy:

In `viewer.html` figure out all the ways that the anonymous "function (connected)"
argument to `myWearScriptConnectionFactory` can be called. Here goes:

* It's called `glassConnectedCallback` in myWearScriptConnectionFactory
* In that function it is hooked into the "subscriptions" callback
  `subscriptions_cb`, which we subscribe to in `myWearScriptConnectionFactory.onopen`.
