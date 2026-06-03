# Extract into Module

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/24/extract-into-module/)

**Original Article Date**: 24 Jul 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

Some codes in your model are related, they are take charge of the same things, such as logging and authorization. We can extract these codes into a module to reuse them.

## Why

It is not exactly a code smell, it is an improvement.

## Bad Example

[Code example - to be extracted from article content]

## Good Example

```ruby
validates_presence_of :cellphone
      before_save :parse_cellphone

      def parse_cellphone
        # do something
      end
    end

    module HasCellphone
      def self.included(base)
        base.validates_presence_of :cellphone
        base.before_save :parse_cellphone
      end

      def parse_cellphone
        # do something
      end
    end

    class User < ActiveRecord::Base
      include HasCellphone
    end
```

## Related Practices

- cellphone
        base.before_save :parse_cellphone
      end

      def parse_cellphone
        # do something
      end
    end

    class User < ActiveRecord::Base
      include HasCellphone
    end

Now we extract the cellphone related validation and  callback into the HasCellphone module, so we can only include HasCellphone module in User model to add the ability of validation and callback.

## Tags

model
