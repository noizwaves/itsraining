itsraining
==========

Push weather notifications for rain in Melbourne, Australia

Installation instructions for OSX
----------

1. Open misc/org.itsraining.tweet_alerts.example.plist, adjust paths and save as org.itsraining.tweet_alerts.plist
2. cp misc/org.itsraining.tweet_alerts.plist /Library/LaunchDaemons/
3. launchctl load -w /Library/LaunchDaemons/org.itsraining.tweet_alerts.plist
4. launchctl start org.itsraining.tweet_alerts