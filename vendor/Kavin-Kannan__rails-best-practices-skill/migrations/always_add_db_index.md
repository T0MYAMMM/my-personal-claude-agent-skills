# Always add DB index

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/24/always-add-db-index/)

**Original Article Date**: 24 Jul 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

Always add index for foreign key, columns that need to be sorted, lookup fields and columns that are used in a GROUP BY. This can improve the performance for sql query.  If you're not sure which column need to index , I recommend to use http://github.com/eladmeidar/rails_indexes, which provide rake tasks to find missing indexes.

## Why

By default, rails does not add indexes automatically for foreign key, you should add indexes by yourself.

class CreateComments < ActiveRecord::Migration
      def self.up
        create_table "comments" do |t|
         t.string :content
         t.integer :post_id
         t.integer :user_id
        end

## Bad Example

```ruby
def self.up
        create_table "comments" do |t|
          t.string :content
          t.integer :post_id
          t.integer :user_id
        end
      end

      def self.down
        drop_table "comments"
      end
    end
```

## Good Example

```ruby
def self.up
        create_table "comments" do |t|
         t.string :content
         t.integer :post_id
         t.integer :user_id
        end

        add_index :comments, :post_id
        add_index :comments, :user_id
      end

      def self.down
        drop_table "comments"
      end
    end
```

## Related Practices

[Related practices - to be identified]

## Tags

migration
