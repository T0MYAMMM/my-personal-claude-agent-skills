# Fetch current user in models

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/08/23/fetch-current-user-in-models/)

**Original Article Date**: 23 Aug 2010

**Original Author**: Richard Huang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

I don't remember how many times I need to fetch current user in models, such as audit log. Here is a flexible way to set the current user in and fetch the current user from User model.

## Why

I don't remember how many times I need to fetch the current user in models, for example, I want to log who creates, updates or destroys a post in the Audit model. There is no default way to fetch the current user in models, current_user object is always assigned in controllers (thanks to authentication plugins, restful_authentication, authlogic and devise), we can pass the current user object from controllers to models, but it is too ugly. I think the better way is to add the current user to User model by Thread.current hash.

class User < ActiveRecord::Base
      def self.current
        Thread.current[:user]
      end
      def self.current=(user)
        Thread.current[:user] = user
      end
    end

## Bad Example

[Code example - to be extracted from article content]

## Good Example

[Code example - to be extracted from article content]

## Related Practices

[Related practices - to be identified]

## Tags

model
