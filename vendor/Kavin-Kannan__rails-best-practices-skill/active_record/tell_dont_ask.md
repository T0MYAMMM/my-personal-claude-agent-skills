# Tell, don't ask

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2012/09/29/tell-don-t-ask/)

**Original Article Date**: 29 Sep 2012

**Original Author**: Zamith

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

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
