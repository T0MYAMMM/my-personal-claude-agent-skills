# Move Model Logic into the Model

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/21/move-model-logic-into-the-model/)

**Original Article Date**: 21 Jul 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

In MVC model, controller should be simple, the business logic is model's responsibility. So we should move logic from controller into the model.

## Why

In this example, PostsController wants to publish a post, first it finds a post, set post's attribute is_published and approved, and assigns the popular attribute according to the value of created_at, PostsController knows too much about the logic, it is not controller's responsibility, it should be handled by model.

class Post < ActiveRecord::Base
      def publish
        self.is_published = true
        self.approved_by = current_user
        if self.created_at > Time.now - 7.days
          self.popular = 100
        else
          self.popular = 0
        end
      end
    end

## Bad Example

```ruby
def publish
        @post = Post.find(params[:id])
        @post.update_attribute(:is_published, true)
        @post.approved_by = current_user
        if @post.created_at > Time.now - 7.days
          @post.popular = 100
        else
          @post.popular = 0
        end

        redirect_to post_url(@post)
      end
    end
```

## Good Example

```ruby
def publish
        self.is_published = true
        self.approved_by = current_user
        if self.created_at > Time.now - 7.days
          self.popular = 100
        else
          self.popular = 0
        end
      end
    end

    class PostsController < ApplicationController
      def publish
        @post = Post.find(params[:id])
        @post.publish

        redirect_to post_url(@post)
      end
    end
```

## Related Practices

[Related practices - to be identified]

## Tags

controller, model
