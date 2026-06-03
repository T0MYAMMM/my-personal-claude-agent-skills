# defer expensive job

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2011/01/12/defer-expensive-job/)

**Original Article Date**: 12 Jan 2011

**Original Author**: Richard Huang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

If you want to process something expensive as part of a web request, it will delay the response. If the job is not critical, it's wiser to move the expensive to a background queue and returns the response immediately.

## Why

Synchronous Processing
------------------------------------

If you want to process something expensive as part of a web request, it will delay the response. The most common situations include sending emails to users, posting tweets, image and video processing, and etc. It is as know as synchronous processing. The processing is as follows

## Bad Example

[Code example - to be extracted from article content]

## Good Example

[Code example - to be extracted from article content]

## Related Practices

[Related practices - to be identified]

## Tags

background job
