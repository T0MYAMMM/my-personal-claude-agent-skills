# Name your model methods after their behavior, not implementation.

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2011/12/05/name-your-model-methods-after-their-behavior-not-implementation/)

**Original Article Date**: 05 Dec 2011

**Original Author**: Brasten Sager

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

Business model methods should be named after the logic / business value they provide, not the implementation details. Violations to this practice tend to show up on ActiveRecord models.

## Why

Business model methods should be named after the logic / business value they provide, not the implementation details. Violations to this practice tend to show up on ActiveRecord models.

## Bad Example

```ruby
class Device

      class << self
        # provisions a new device for the user
        #
        def find_and_update_or_reassign_or_create( user, attributes )
          # ...
        end
      end
    end

    class Device

      class << self
        # provisions a new device for the user
        #
        def provision( user, attributes )
          # ...
        end
      end
    end
```

## Good Example

```ruby
class Device

      class << self
        # provisions a new device for the user
        #
        def provision( user, attributes )
          # ...
        end
      end
    end
```

## Related Practices

[Related practices - to be identified]

## Tags

model
