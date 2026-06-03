# Keep Finders on Their Own Model

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/23/keep-finders-on-their-own-model/)

**Original Article Date**: 23 Jul 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

According to the decoupling principle, model should do finders by itself, a model should not know too much about associations finders logic.

## Why

According to the decoupling principle, model should do finders by itself, a model should not know too much about associations finders logic. In here, Post model handle the complex finder of comments, but this is not its job, we should move valid comments finder to the Comment model.

class Post < ActiveRecord::Base
      has_many :comments
    end

## Bad Example

```ruby
has_many :comments

      def find_valid_comments
        self.comment.find(:all, :conditions => {:is_spam => false},
                                :limit => 10)
      end
    end

    class Comment < ActiveRecord::Base
      belongs_to :post
    end

    class CommentsController < ApplicationController
      def index
        @comments = @post.find_valid_comments
      end
    end
```

## Good Example

```ruby
has_many :comments
    end

    class Comment < ActiveRecord::Base
      belongs_to :post

      named_scope :only_valid, :conditions => { :is_spam => false }
      named_scope :limit, lambda { |size| { :limit => size } }
    end

    class CommentsController < ApplicationController
      def index
        @comments = @post.comments.only_valid.limit(10)
      end
    end
```

## Related Practices

[Related practices - to be identified]

## Tags

rails2, model
