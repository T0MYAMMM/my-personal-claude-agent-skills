# Move code into helper

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/24/move-code-into-helper/)

**Original Article Date**: 24 Jul 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

According to MVC architecture, there should not be logic codes in view, in this practice, I will introduce you to move codes into helper.

## Why

The options for state select is a bit complex in view, let's move it into helper.

<%= select_tag :state, options_for_post_state(params[:default_state]) %>

## Bad Example

[t(:published), "published"]],
                                               params[:default_state] ) %>

## Good Example

```ruby
# app/helpers/posts_helper.rb
    def options_for_post_state(default_state)
      options_for_select( [[t(:draft), "draft"], [t(:published), "published"]],
                          default_state )
    end
```

## Related Practices

[Related practices - to be identified]

## Tags

view, helper
