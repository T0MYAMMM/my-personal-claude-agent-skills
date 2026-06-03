# Restrict Auto-Generated Routes

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2011/08/19/restrict-auto-generated-routes/)

**Original Article Date**: August 19, 2011

**Original Author**: Richard Huang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself is a fact about Rails routing conventions and community knowledge.

## Description

By default, Rails generates seven RESTful routes(new,edit,create,destroy,index,show, update) for a resource, sometime the resource only needs one or two routes, so just user :only or :except while defining routes to speedup the routing.

## Why

By default, Rails generates seven RESTful routes(new,edit,create,destroy,index,show, update) for a resource, sometime the resource only needs one or two routes, so just user :only or :except while defining routes to speedup the routing.

## Bad Example

[Code example - to be extracted from article content]

## Good Example

[Code example - to be extracted from article content]

## Related Practices

[Related practices - to be identified]

## Tags

route, rails, RESTful
