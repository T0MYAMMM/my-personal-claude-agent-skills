# Use say and say_with_time in Migrations

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/08/19/use-say-and-say_with_time-in-migrations-to-make-a-useful-migration-log/)

**Original Article Date**: August 19, 2010

**Original Author**: Richard Huang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself is a fact about Rails migrations and community knowledge.

## Description

Use `say` and `say_with_time` in migrations to make useful migration logs. These methods provide descriptive output during migration execution, making it easier to understand what the migration is doing and how long operations take.

## Why

- Makes migration logs more informative and readable
- Helps debug migration issues
- Provides timing information for long-running migrations
- Makes it clear what each migration step is doing
- Improves maintainability of migration files

## Bad Example

```ruby
# Bad - no logging
class UpdateUsersNames < ActiveRecord::Migration[7.0]
  def up
    User.find_each do |user|
      parts = user.name.split(' ', 2)
      user.update_columns(first_name: parts[0], last_name: parts[1] || '')
    end
  end
end
```

## Good Example

```ruby
# Good - use say and say_with_time
class UpdateUsersNames < ActiveRecord::Migration[7.0]
  def up
    say "Splitting name to extract first and last name"
    
    say_with_time "Updating #{User.count} users" do
      User.find_each do |user|
        parts = user.name.split(' ', 2)
        user.update_columns(first_name: parts[0], last_name: parts[1] || '')
        say "Updated user #{user.id}", true
      end
    end
  end
  
  def down
    say "Reverting name changes"
    say_with_time "Reverting #{User.count} users" do
      User.find_each do |user|
        user.update_columns(name: "#{user.first_name} #{user.last_name}".strip)
      end
    end
  end
end
```

## Related Practices

- Make migrations reversible when possible
- Use batched finders for large data queries

## Tags

migrations, logging, maintenance, rails

