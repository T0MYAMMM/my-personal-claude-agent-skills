# Not use default route if you use RESTful design

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/22/not-use-default-route-if-you-use-restful-design/)

**Original Article Date**: 22 Jul 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

If you use RESTful design, you should NOT use default route. It will cause a security problem. I explain at http://ihower.tw/blog/archives/3265 too.

## Why

Why do not use the default route? In this example, you define the resources posts, that means user can only create a post by HTTP POST, update a post by PUT and destroy a post by DELETE. If this is what you expect, default route will be a security problem, because user can create, update or destroy a post by HTTP GET if you define the default route.

map.resources :posts, :member => { :push => :post }

## Bad Example

map.connect ':controller/:action/:id'
    map.connect ':controller/:action/:id.:format'

## Good Example

#map.connect ':controller/:action/:id'
    #map.connect ':controller/:action/:id.:format'

    map.connect 'special/:action/:id', :controller => 'special'

## Related Practices

[Related practices - to be identified]

## Tags

rails2, route
