# Love named_scope

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/23/love-named_scope/)

**Original Article Date**: 23 Jul 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

named_scope is awesome, it makes your codes much more readable, you can also combine named_scope finders to do complex finders.

## Why

This is a complex finder in controller, it contains fuzzy query, order and limit, it is confused and the complex finder should not be placed in controller. We should move the complex finder to model by using named_scope.

class Post < ActiveRecord::Base
      named_scope :matching, lambda { |column , value|
        return {} if value.blank?
        { :conditions => ["#{column} like ?", "%#{value}%"] }
      }

## Bad Example

```ruby
def search
        conditions = { :title => "%#{params[:title]}%" } if params[:title]
        conditions.merge! { :content => "%#{params[:content]}%" } if params[:content]

        case params[:order]
        when "title" : order = "title desc"
        when "created_at : order = "created_at desc"
        end

        @posts = Post.find(:all, :conditions => conditions, :order => order,
                                 :limit => params[:limit])
      end
    end
```

## Good Example

```ruby
named_scope :matching, lambda { |column , value|
        return {} if value.blank?
        { :conditions => ["#{column} like ?", "%#{value}%"] }
      }

      named_scope :order, lambda { |order|
        {
          :order => case order
          when "title" : "title desc"
          when "created_at" : "created_at desc"
          end
        }
      }

      named_scope :limit, lambda { |limit|
        { :limit => limit }
      }
    end

    class PostsController < ApplicationController
      def search
        @posts = Post.matching(:title, params[:title])
                     .matching(:content, params[:content])
                     .order(params[:order]).limit(params[:limit])
      end
    end
```

## Related Practices

[Related practices - to be identified]

## Tags

rails2, controller, model
