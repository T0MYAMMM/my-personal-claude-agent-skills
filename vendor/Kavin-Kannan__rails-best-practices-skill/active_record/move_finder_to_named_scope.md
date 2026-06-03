# Move finder to named_scope

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/14/move-finder-to-named_scope/)

**Original Article Date**: 14 Jul 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

Complex finders in controller make application hard to maintain. Move them into the model as named_scope can make the controller simple and the complex find logics are all in models.

## Why

In this example, PostsController uses two complex finders to get the published_posts and draft_posts. There are 2 bad smells:

1. The controller method contains complex finders is always too long, which make it difficult to read.
 2. The same complex finders may be existed in different controllers, if you change the logic, you have to change the complex finders in different place, which adds the possibilities to create bugs.

## Bad Example

```ruby
def index
        @published_posts = Post.find(:all, :conditions => { :state => 'published' },
                                           :limit => 10,
                                           :order => 'created_at desc')

        @draft_posts = Post.find(:all, :conditions => { :state => 'draft' },
                                       :limit => 10,
                                       :order => 'created_at desc')
      end
    end
```

## Good Example

```ruby
def index
        @published_posts = Post.published
        @draft_posts = Post.draft
      end
    end

    class Post < ActiveRecord::Base
      named_scope :published, :conditions => { :state => 'published' },
                              :limit => 10,
                              :order => 'created_at desc'
      named_scope :draft, :conditions => { :state => 'draft' },
                          :limit => 10,
                          :order => 'created_at desc'
    end
```

## Related Practices

[Related practices - to be identified]

## Tags

rails2, controller, model
