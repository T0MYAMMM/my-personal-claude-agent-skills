# Extract to composed class

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/24/extract-to-composed-class/)

**Original Article Date**: 24 Jul 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

If a model has some related columns, e.g. a user has an address_city and an address_street, you can extract these properties into a composed class.

## Why

You can see that a Customer model has two properties address_city and address_street, but address_city and address_street should be the property in Address class. If you don't want to create a addresses table, you can just create a composed class Address.

class Customer < ActiveRecord::Base
      composed_of :address, :mapping => [ %w(address_street street), %w(address_city city)]
    end

## Bad Example

```ruby
#  address_city        :string(255)
    #  address_street      :string(255)
    class Customer < ActiveRecord::Base
      def address_close_to?(other_customer)
        address_city == other_cutomer.address_city
      end

      def address_equal(other_customer)
        address_street == other_customer.address_street &&
          address_city == other_customer.address_city
      end
    end
```

## Good Example

```ruby
composed_of :address, :mapping => [ %w(address_street street), %w(address_city city)]
    end

    class Address
      attr_reader :street, :city

      def initialize(street, city)
        @street, @city = street, city
      end

      def close_to?(other_address)
        city == other_address.city
      end

      def ==(other_address)
        city == other_address.city && street == other_address.street
      end
    end
```

## Related Practices

[Related practices - to be identified]

## Tags

model
