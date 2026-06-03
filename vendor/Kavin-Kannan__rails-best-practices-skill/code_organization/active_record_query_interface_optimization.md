# Active Record Query Interface Optimization

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2011/06/23/active-record-query-interface-optimization/)

**Original Article Date**: 23 Jun 2011

**Original Author**: Angelo Capilleri

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

Use  select  with  has_many and belongs_to on Active Record Associations

## Why

Using the `select` parameter in Active Record association, you can speed up your application about 50% and more.
The following example is only focused on the optimization of the association using select, so there are further optimizations for the following examples.

class Patient < ActiveRecord::Base
      belongs_to :physician
    end
    class Physician < ActiveRecord::Base
      has_many :patients
    end

## Bad Example

[Code example - to be extracted from article content]

## Good Example

[Code example - to be extracted from article content]

## Related Practices

[Related practices - to be identified]

## Tags

refactor, model, performance
