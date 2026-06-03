# DRY Metaprogramming

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/24/dry-metaprogramming/)

**Original Article Date**: 24 Jul 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

If you find some methods whose definitions are similar, only different by the method name, it may use meta programming to simplify the things.

## Why

In this example, we have the similar method definitions of all_draft, all_published, all spam and draft?, published?, spam?, their differences are dependent on the method name, more precisely, dependent on the different status. We can simplify the codes by using meta programming.

class Post < ActiveRecord::Base

## Bad Example

```ruby
validate_inclusion_of :status, :in => ['draft', 'published', 'spam']

      def self.all_draft
        find(:all, :conditions => { :status => 'draft' }
      end

      def self.all_published
        find(:all, :conditions => { :status => 'published' }
      end

      def self.all_spam
        find(:all, :conditions => { :status => 'spam' }
      end

      def draft?
        self.status == 'draft'
      end

      def published?
        self.status == 'published'
      end

      def spam?
        self.status == 'spam'
      end
    end
```

## Good Example

```ruby
STATUSES = ['draft', 'published', 'spam']
      validate_inclusion_of :status, :in => STATUSES

      class <<self
        STATUSES.each do |status_name|
          define_method "all_#{status_name}" do
            find(:all, :conditions => { :status => status_name }
          end
        end
      end

      STATUSES.each do |status_name|
        define_method "#{status_name}?" do
          self.status == status_name
        end
      end

    end
```

## Related Practices

- :Base

      STATUSES = ['draft', 'published', 'spam']
      validate_inclusion_of :status, :in => STATUSES

      class <<self
        STATUSES.each do |status_name|
          define_method "all_#{status_name}" do
            find(:all, :conditions => { :status => status_name }
          end
        end
      end

      STATUSES.each do |status_name|
        define_method "#{status_name}?" do
          self.status == status_name
        end
      end

    end

It is much cleaner to use the meta programming to dynamic define the methods, besides this, it is much easier to meet the changes, if some statuses are added, changed or removed, what you should do is to change the constants STATUSES.

Updated: thanks @funny_falcon

## Tags

model
