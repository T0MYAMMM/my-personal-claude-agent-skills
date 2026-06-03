# Use Model Callbacks

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/21/use-model-callback/)

**Original Article Date**: July 21, 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself is a fact about Rails ActiveRecord callbacks and community knowledge.

## Description

Use model callback can avoid writing some logic codes in controller before or after creating, updating and destroying a model.

## Why

In this example, if user clicks the checkbox auto_tagging, we will generate tags according to the content of post, then assign the tags to the post before saving the post. We can move the tags assignment codes into the model by using model callback.

class Post < ActiveRecord::Base
      attr_accessor :auto_tagging
      before_save :generate_tagging

## Bad Example

```erb
<%= f.text_field :content %>
      <%= check_box_tag 'auto_tagging' %>
    <% end %>

    class PostsController < ApplicationController
      def create
        @post = Post.new(params[:post])

        if params[:auto_tagging] == '1'
          @post.tags = AsiaSearch.generate_tags(@post.content)
        else
          @post.tags = ""
        end

        @post.save
      end
    end
```

## Good Example

```erb
attr_accessor :auto_tagging
      before_save :generate_tagging

      private
      def generate_taggings
        return unless auto_tagging == '1'
        self.tags = Asia.search(self.content)
      end
    end

    <% form_for @post do |f| %>
      <%= f.text_field :content %>
      <%= f.check_box :auto_tagging %>
    <% end %>

    class PostsController < ApplicationController
      def create
        @post = Post.new(params[:post])
        @post.save
      end
    end
```

## Related Practices

[Related practices - to be identified]

## Tags

controller, model
