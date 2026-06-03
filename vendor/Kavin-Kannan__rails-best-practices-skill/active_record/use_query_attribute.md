# Use query attribute

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/10/03/use-query-attribute/)

**Original Article Date**: 03 Oct 2010

**Original Author**: Richard Huang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

Do you always check if ActiveRecord's attributes exist or not by nil?, blank? or present? ? Don't do that again, rails provides a cleaner way by query attribute

## Why

It's not bad, but rails provides a cleaner way, we should use query attributes to make codes simpler

<% unless @user.login? %>
      <%= link_to 'login', new_session_path %>
    <% end %>

## Bad Example

```erb
<%= link_to 'login', new_session_path %>
    <% end %>

    <% if @user.login.present? %>
      <%= @user.login %>
    <% end %>
```

## Good Example

```erb
<%= link_to 'login', new_session_path %>
    <% end %>

    <% if @user.login? %>
      <%= @user.login %>
    <% end %>
```

## Related Practices

[Related practices - to be identified]

## Tags

model
