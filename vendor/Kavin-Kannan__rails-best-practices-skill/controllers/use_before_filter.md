# Use before_filter

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/24/use-before_filter/)

**Original Article Date**: 24 Jul 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

Don't repeat yourself in controller, use before_filter to avoid duplicated codes.

## Why

In this example, the first code in action show, edit, update and destroy are the same, we hate the duplicated code, use before_filter  to avoid.

class PostsController < ApplicationController
      before_filter :find_post, :only => [:show, :edit, :update, :destroy]

## Bad Example

```ruby
def show
        @post = current_user.posts.find(params[:id])
      end

      def edit
        @post = current_user.posts.find(params[:id])
      end

      def update
        @post = current_user.posts.find(params[:id])
        @post.update_attributes(params[:post])
      end

      def destroy
        @post = current_user.posts.find(params[:id])
        @post.destroy
      end
    end
```

## Good Example

```ruby
before_filter :find_post, :only => [:show, :edit, :update, :destroy]

      def update
        @post.update_attributes(params[:post])
      end

      def destroy
        @post.destroy
      end

      protected
        def find_post
          @post = current_user.posts.find(params[:id])
        end
    end
```

## Related Practices

[Related practices - to be identified]

## Tags

controller
