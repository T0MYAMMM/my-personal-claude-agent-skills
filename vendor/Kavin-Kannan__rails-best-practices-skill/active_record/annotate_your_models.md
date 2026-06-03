# Annotate your models

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2011/01/23/annotate-your-models/)

**Original Article Date**: 23 Jan 2011

**Original Author**: Richard Huang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

Are you tired of going to schema.rb to find your table structures information? It would be better to list all the attributes of the model in the model itself.

## Why

Are you tired of going to schema.rb to find your table structures information? It would be better to list all the attributes of the model in the model itself.

## Bad Example

```ruby
class Post < ActiveRecord::Base
      has_many :comments
    end

    class Comment < ActiveRecord::Base
      belongs_to :post
    end

    ActiveRecord::Schema.define(:version => 20101223141603) do
      create_table "posts", :force => true do |t|
        t.string   "title"
        t.text     "body"
        t.datetime "created_at"
        t.datetime "updated_at"
        t.integer  "user_id"
      end

      create_table "comments", :force => true do |t|
        t.text     "body"
        t.integer  "post_id"
        t.integer  "user_id"
        t.datetime "created_at"
        t.datetime "updated_at"
      end
    end

    # == Schema Information
    #
    # Table name: posts
    #
    #  id             :integer(4)      not null, primary key
    #  title          :string(255)
    #  body           :text(16777215)
    #  created_at     :datetime
    #  updated_at     :datetime
    #  user_id        :integer(4)
    #
    class Post < ActiveRecord::Base
    end

    # == Schema Information
    #
    # Table name: comments
    #
    #  id               :integer(4)      not null, primary key
    #  body             :text(16777215)
    #  post_id          :integer(4)
    #  user_id          :integer(4)
    #  created_at       :datetime
    #  updated_at       :datetime
    #
    class Comment < ActiveRecord::Base
    end
```

## Good Example

[Code example - to be extracted from article content]

## Related Practices

[Related practices - to be identified]

## Tags

model, gem, comment
