# Use model association

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/19/use-model-association/)

**Original Article Date**: 19 Jul 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

Use model association to avoid assigning reference in controller.

## Why

In this example, user_id is assigned to @post explicitly. It's not too big problem, but we can save this line by using model association.

class PostsController < ApplicationController
      def create
        @post = current_user.posts.build(params[:post])
        @post.save
      end
    end

## Bad Example

```ruby
def create
        @post = Post.new(params[:post])
        @post.user_id = current_user.id
        @post.save
      end
    end
```

## Good Example

```ruby
def create
        @post = current_user.posts.build(params[:post])
        @post.save
      end
    end

    class User < ActiveRecord::Base
      has_many :posts
    end
```

## Related Practices

[Related practices - to be identified]

## Tags

controller, model
