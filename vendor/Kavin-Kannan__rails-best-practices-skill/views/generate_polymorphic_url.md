# Generate polymorphic url

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/09/23/generate-polymorphic-url/)

**Original Article Date**: 23 Sep 2010

**Original Author**: Richard Huang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

If you want to generate different urls according to different objects, you should use the polymorphic_path/polymorphic_url to simplify the url generation.

## Why

Imagine that we have three models, Post, News and Comment. It's common that a post has many comments and a news has many comments, so we define them as

class Post < ActiveRecord::Base
      has_many :comments
    end
    class News < ActiveRecord::Base
      has_many :comments
    end
    class Comment < ActiveRecord::Base
      belongs_to :commentable, :polymorphic => true
    end

## Bad Example

```ruby
# parent may be a post or a news
    if Post === parent
      post_comments_path(parent)
    elsif News === parent
      news_comments_path(parent)
    end

    if Post === parent
      post_path(parent)
    elsif News === parent
      news_path(parent)
    end
```

## Good Example

polymorphic_path([parent, Comment])    # "/posts/1/comments" or "'news/1/comments"

    polymorphic_path(parent)    # "http://example.com/posts/1/comments" or "http://example.com/news/1/comments"

    new_polymorphic_path(Post)    # "/posts/new"
    new_polymorphic_url(Post)    # "http://example.com/posts/new"
    edit_polymorphic_path(post)    # "/posts/1/edit"
    edit_polymorphic_url(post)    # "http://example.com/posts/1/edit"

## Related Practices

[Related practices - to be identified]

## Tags

view, helper
