# DRY Controller (debate)

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/24/dry-controller-and-debate/)

**Original Article Date**: 24 Jul 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

For CRUD resources, we always write the same 7 actions with duplicated codes. To avoid this, you can use inherited_resources plugin. But be careful, there is DRY controller debate!! (http://www.binarylogic.com/2009/10/06/discontinuing-resourcelogic/)  1. You lose intent and readability 2. Deviating from standards makes it harder to work with other programmers 3. Upgrading rails trouble

## Why

For CRUD resources, we always write the same 7 actions with duplicated codes. To avoid this, you can use inherited_resources plugin. But be careful, there is DRY controller debate!! (http://www.binarylogic.com/2009/10/06/discontinuing-resourcelogic/)  1. You lose intent and readability 2. Deviating from standards makes it harder to work with other programmers 3. Upgrading rails trouble

## Bad Example

[Code example - to be extracted from article content]

## Good Example

```ruby
def index
        @posts = Post.all
      end

      def show
        @post = Post.find(params[:id])
      end

      def new
        @post = Post.new
      end

      def create
        @post.create(params[:post])
        redirect_to post_path(@post)
      end

      def edit
        @post = Post.find(params[:id])
      end

      def update
        @post = Post.find(params[:id])
        @post.update_attributes(params[:post])
        redirect_to post_path(@post)
      end

      def destroy
        @post = Post.find(params[:id])
        @post.destroy
        redirect_to posts_path
      end
    end

    class PostsController < InheritedResources::Base
      # magic!! nothing here!
    end
```

## Related Practices

[Related practices - to be identified]

## Tags

controller, plugin
