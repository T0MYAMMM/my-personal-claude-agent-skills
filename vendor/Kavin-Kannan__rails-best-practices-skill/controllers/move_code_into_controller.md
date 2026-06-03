# Move code into controller

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/24/move-code-into-controller/)

**Original Article Date**: 24 Jul 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

According to MVC architecture, there should not be logic codes in view, in this practice, I will introduce you to move codes into controller.

## Why

According to MVC architecture, there should not be logic codes in view. The posts finder should not exist in view, please move it into controller.

class PostsController < ApplicationController
      def index
        @posts = Post.find(:all)
      end
    end

## Bad Example

```erb
<% @posts.each do |post| %>
      <%=h post.title %>
      <%=h post.content %>
    <% end %>
```

## Good Example

```ruby
def index
        @posts = Post.find(:all)
      end
    end
```

## Related Practices

[Related practices - to be identified]

## Tags

controller, view
