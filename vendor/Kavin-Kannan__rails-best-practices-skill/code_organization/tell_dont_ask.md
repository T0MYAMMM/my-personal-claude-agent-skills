# Tell, don't ask

**Source**: [rails-bestpractices.com](https://rails-bestpractices.com/posts/2012/09/29/tell-dont-ask/)

**Date**: September 29, 2012

**Author**: Zamith

## Description

Methods should focus on what you want done and not how you want it.

## Why

It should be telling the user to provide a birthday year and expect a coherent response if it has one or not.

def birth_year(user)
      user.birthday.year
    end

## Bad Example

```ruby
def birth_year(user)
      if user.birthday
        user.birthday.year
      else
        'No birthday year on file'
      end
    end
```

## Good Example

```ruby
def birth_year(user)
      user.birthday.year
    end

    class User
      def birthday
        @birthday || NullBirthday.new
      end
    end

    class NullBirthday
      def year
        'No birthday year on file'
      end
    end
```

## Related Practices

[Related practices - to be identified]

## Tags

model, refactor
