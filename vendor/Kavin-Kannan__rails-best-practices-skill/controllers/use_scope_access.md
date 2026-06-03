# Use Scope Access

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/20/use-scope-access/)

**Original Article Date**: July 20, 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself is a fact about Rails authorization patterns and community knowledge.

## Description

You can use scope access to avoid checking the permission by comparing the owner of object with current_user in controller.

## Why

In this example, we compare the user of post with current_user, if the condition returns false, do not allow user to edit the post. But it's too verbose to do this permission check for edit, update, destroy and etc. Let's use scope access to refactor.

class PostsController < ApplicationController
      def edit
        # raise RecordNotFound exception (404 error) if not found
        @post = current_user.posts.find(params[:id])
      end
    end

## Bad Example

```ruby
def edit
        @post = Post.find(params[:id])
        if @post.user != current_user
          flash[:warning] = 'Access denied'
          redirect_to posts_url
        end
      end
    end
```

## Good Example

```ruby
def edit
        # raise RecordNotFound exception (404 error) if not found
        @post = current_user.posts.find(params[:id])
      end
    end
```

## Related Practices

[Related practices - to be identified]

## Tags

controller
