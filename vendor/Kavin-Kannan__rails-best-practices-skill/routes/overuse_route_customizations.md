# Overuse route customizations

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/22/overuse-route-customizations/)

**Original Article Date**: 22 Jul 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

According to Roy Fieldingâ€™s doctoral thesis, we should use restful routes to represent the resource and its state. Use the default 7 actions without overusing route customizations.

## Why

According to Roy Fieldingâ€™s doctoral thesis, we should use restful routes to represent the resource and its state. Use the default 7 actions(index, show, new, edit, create, update and destroy) without overusing route customizations. The solution to solve the overuse route customizations is to find another resources

map.resources :posts do |post|
      post.resources :comments
    end

## Bad Example

:create_comment => :post,
                                       :update_comment => :put,
                                       :delete_comment => :delete }

## Good Example

```ruby
post.resources :comments
    end
```

## Related Practices

[Related practices - to be identified]

## Tags

rails2, route
