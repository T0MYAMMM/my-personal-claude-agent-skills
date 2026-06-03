# Check the return value of "save", otherwise use "save!"

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2012/11/02/check-the-return-value-of-save-otherwise-use-save/)

**Original Article Date**: 02 Nov 2012

**Original Author**: Richard Huang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

The "save" method on ActiveRecord returns "false" and does nothing if the record is invalid. You should always check the return value, otherwise you may inadvertently not save the record. If you think the record can never be invalid, or don't want to check the return value, use "save!"

## Why

This code may work at the moment, but it is fragile. If a later refactoring introduces a new required column to Posts, then the `save` call will silently start failing.

If you think the record can never be invalid, or don't want to check the return value, use "[save!][2]"

## Bad Example

```ruby
post = Posts.new do |p|
      p.title = "example"
      p.body = "An example"
    end
    post.save
```

## Good Example

```ruby
post = Posts.new do |p|
      p.title = "example"
      p.body = "An example"
    end
    post.save!
```

## Related Practices

- The [record.update_attributes][3] method will also return "false" if it failed to save changes. Just as for `save`, you should check the return value or use [update_attributes!][4].

The [RecordClass.create][5] method may fail to save the newly created method, but will not return `false` in that case. It should be avoided for this reason, and you should always use [RecordClass.create!][6].



  [1]: http://api.rubyonrails.org/classes/ActiveRecord/Persistence.html#method-i-save
  [2]: http://api.rubyonrails.org/classes/ActiveRecord/Persistence.html#method-i-save-21
  [3]: http://api.rubyonrails.org/classes/ActiveRecord/Persistence.html#method-i-update_attributes
  [4]: http://api.rubyonrails.org/classes/ActiveRecord/Persistence.html#method-i-update_attributes-21
  [5]: http://api.rubyonrails.org/classes/ActiveRecord/Persistence/ClassMethods.html#method-i-create
  [6]: http://api.rubyonrails.org/classes/ActiveRecord/Validations/ClassMethods.html#method-i-create-21

## Tags

active_record
