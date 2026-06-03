# Replace Complex Creation with Factory Method

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/21/replace-complex-creation-with-factory-method/)

**Original Article Date**: July 21, 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself is a fact about Rails design patterns and community knowledge.

## Description

Sometimes you will build a complex model with params, current_user and other logics in controller, but it makes your controller too big, you should move them into model with a factory method

## Why

The logic to create an invoice is too complex, it makes InvoicesController a bit difficult to read. And the controller should not know too much things about how to create a model, we should move the the logic of creating an invoice into the Invoice model.

class Invoice < ActiveRecord::Base
      def self.new_by_user(params, user)
        invoice = self.new(params)
        invoice.address = user.address
        invoice.phone = user.phone
        invoice.vip = (invoice.amount > 1000)

## Bad Example

```ruby
def create
        @invoice = Invoice.new(params[:invoice])
        @invoice.address = current_user.address
        @invoice.phone = current_user.phone
        @invoice.vip = (@invoice.amount > 1000)

        if Time.now.day > 15
          @invoice.delivery_time = Time.now + 2.month
        else
          @invoice.delivery_time = Time.now + 1.month
        end

        @invoice.save
      end
    end
```

## Good Example

```ruby
def self.new_by_user(params, user)
        invoice = self.new(params)
        invoice.address = user.address
        invoice.phone = user.phone
        invoice.vip = (invoice.amount > 1000)

        if Time.now.day > 15
          invoice.delivery_time = Time.now + 2.month
        else
          invoice.delivery_time = Time.now + 1.month
        end
      end
    end

    class InvoicesController < ApplicationController
      def create
        @invoice = Invoice.new_by_user(params[:invoice], current_user)
        @invoice.save
      end
    end
```

## Related Practices

[Related practices - to be identified]

## Tags

controller, model
