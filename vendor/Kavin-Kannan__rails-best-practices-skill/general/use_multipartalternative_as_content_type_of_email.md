# Use multipart/alternative as content_type of email

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/08/05/use-multipart-alternative-as-content_type-of-email/)

**Original Article Date**: 05 Aug 2010

**Original Author**: Richard Huang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

Rails uses plain/text as the default content_type for sending email, you should change it to multipart/alternative that email clients can display html formatted email if they support and display plain text email if they don't support html format.

## Why

Rails uses plain/text as the default content_type for sending email, you should change it to multipart/alternative that email clients can display html formatted email if they support and display plain text email if they don't support html format.

## Bad Example

[Code example - to be extracted from article content]

## Good Example

[Code example - to be extracted from article content]

## Related Practices

[Related practices - to be identified]

## Tags

mailer
