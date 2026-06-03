# Move code into model

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/24/move-code-into-model/)

**Original Article Date**: 24 Jul 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

According to MVC architecture, there should not be logic codes in view, in this practice, I will introduce you to move codes into model.

## Why

In this example, we check the edit permission in view with a complex code, but complex logic codes should not be placed in view, we should move it to model.

<% if @post.editable_by?(current_user)) %>
      <%= link_to 'Edit this post', edit_post_url(@post) %>
    <% end %>

## Bad Example

```erb
@post.editors.include?(current_user)) %>
      <%= link_to 'Edit this post', edit_post_url(@post) %>
    <% end %>
```

## Good Example

```erb
<%= link_to 'Edit this post', edit_post_url(@post) %>
    <% end %>

    class Post < ActiveRecord::Base
      def editable_by?(user)
        user && (user == self.user || self.editors.include?(user))
      end
    end
```

## Related Practices

[Related practices - to be identified]

## Tags

model, view
