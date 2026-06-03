# Use Time.zone.now instead of Time.now

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2014/10/22/use-time-zone-now-instead-of-time-now/)

**Original Article Date**: 22 Oct 2014

**Original Author**: Dan Kohn

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

The ActiveSupport method Time.zone.now should be used in place of the Ruby method Time.now to pickup the local time zone.

## Why

These show the local time, not the time in Alaska (unless you're already in Alaska).

You should instead use ActiveSupport methods of `Time.zone` to pickup the Rails time zone.

## Bad Example

Time.zone = "Alaska"
    Time.now
    Date.today

## Good Example

Time.zone.now
    Time.zone.today

## Related Practices

[Related practices - to be identified]

## Tags

timezone
