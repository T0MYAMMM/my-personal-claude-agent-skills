# Isolating Seed Data

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/24/isolating-seed-data/)

**Original Article Date**: 24 Jul 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

Rails 2.3.4 provides db:seed task that is the best way to insert seed data for set up a new application.

## Why

Before, we always insert data in migrations, which is not a good approach, it clutters up the migrations. The better way is to move all the data creations from migration files into seed.rb

# db/seeds.rb (Rails 2.3.4)
    ["admin", "author", "editor", "account"].each do |name|
      Role.create!(:name => name)
    end

## Bad Example

```ruby
def self.up
        create_table "roles", :force => true do |t|
          t.string :name
        end

        ["admin", "author", "editor", "account"].each do |name|
          Role.create!(:name => name)
        end
      end

      def self.down
        drop_table "roles"
      end
    end
```

## Good Example

```ruby
["admin", "author", "editor", "account"].each do |name|
      Role.create!(:name => name)
    end

    rake db:seed

    # lib/tasks/dev.rake (before Rails 2.3.4)
    namespace :dev do

      desc "Setup seed data"
      task :setup => :environment do
        ["admin", "author", "editor", "account"].each do |name|
          Role.create!(:name => name)
        end
      end
    end

    rake dev:setup
```

## Related Practices

[Related practices - to be identified]

## Tags

migration
