# the Law of Demeter

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/24/the-law-of-demeter/)

**Original Article Date**: 24 Jul 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

According to the law of demeter, a model should only talk to its immediate association, don't talk to the association's association and association's property, it is a case of loose coupling.

## Why

In this example, invoice model calls the association(user)'s property(name, address and cellphone), which violates the law of demeter. We should add some wrapper methods.

class Invoice < ActiveRecord::Base
      belongs_to :user
      delegate :name, :address, :cellphone, :to => :user, :prefix => true
    end

## Bad Example

```erb
belongs_to :user
    end

    <%= @invoice.user.name %>
    <%= @invoice.user.address %>
    <%= @invoice.user.cellphone %>
```

## Good Example

```erb
belongs_to :user
      delegate :name, :address, :cellphone, :to => :user, :prefix => true
    end

    <%= @invoice.user_name %>
    <%= @invoice.user_address %>
    <%= @invoice.user_cellphone %>
```

## Related Practices

[Related practices - to be identified]

## Tags

model
