# Make Migrations Reversible When Possible

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/)

**Original Article Date**: Various

**Original Author**: Various

**Note**: This practice is rewritten in our own words based on the concept. The practice itself is a fact about Rails migrations and community knowledge.

## Description

Make migrations reversible when possible by implementing both `up` and `down` methods, or by using `change` with reversible operations. This allows you to rollback migrations safely and makes database changes more manageable.

## Why

- Allows safe rollback of migrations
- Makes database changes more predictable
- Helps with development and testing
- Follows Rails conventions
- Makes it easier to fix mistakes

## Bad Example

```ruby
# Bad - not reversible
class AddStatusToUsers < ActiveRecord::Migration[7.0]
  def up
    add_column :users, :status, :string
    User.update_all(status: 'active')
  end
  
  # Missing down method - migration cannot be rolled back
end
```

## Good Example

```ruby
# Good - reversible migration
class AddStatusToUsers < ActiveRecord::Migration[7.0]
  def change
    add_column :users, :status, :string, default: 'active', null: false
  end
end

# Or with explicit up/down
class AddStatusToUsers < ActiveRecord::Migration[7.0]
  def up
    add_column :users, :status, :string, default: 'active', null: false
    User.update_all(status: 'active')
  end
  
  def down
    remove_column :users, :status
  end
end

# Or with reversible blocks
class AddStatusToUsers < ActiveRecord::Migration[7.0]
  def change
    reversible do |dir|
      dir.up do
        add_column :users, :status, :string, default: 'active', null: false
        User.update_all(status: 'active')
      end
      
      dir.down do
        remove_column :users, :status
      end
    end
  end
end
```

## Related Practices

- Use say and say_with_time in migrations
- Test migrations in development

## Tags

migrations, reversible, database, rails

