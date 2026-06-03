# Avoid time_ago_in_words (Use Client-Side JavaScript)

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2012/02/10/not-use-time_ago_in_words/)

**Original Article Date**: February 10, 2012

**Original Author**: Richard Huang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself is a fact about Rails view helpers and performance.

## Description
## Description

It's very common for a rails developer to use time_ago_in_words to display time like "5 minutes ago", but it's too expensive to calculate the time in server side, you should utilize client cpu to calculate the time ago.

## Why

Rails provides a helper method time_ago_in_words to display the distance between one time and now, like "5 minute ago", it's very useful.

## Bad Example

[Bad example - to be extracted from article content]

## Good Example

[Good example - to be extracted from article content]

## Related Practices

[Related practices - to be identified]

## Tags

helper, javascript
