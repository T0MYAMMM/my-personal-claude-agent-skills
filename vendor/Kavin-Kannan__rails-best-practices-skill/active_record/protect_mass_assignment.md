# Protect mass assignment

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2012/03/06/protect-mass-assignment/)

**Original Article Date**: 06 Mar 2012

**Original Author**: Richard Huang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

Rails mass assignment feature is really useful, but it may be a security issue, it allows an attacker to set any models' attributes you may not expect. To avoid this, we should add attr_accessbile or attr_protected to all models.

## Why

Last weekend github is hacked because of mass assignment issue, actually it's not rails fault, it's a "junior" develop forgot to add attr_accessible or attr_protected to model, like

class UsersController < ApplicationController
      def update
        if current_user.update_attributes(params[:user])
          # do something
        end
      end
    end

## Bad Example

[Code example - to be extracted from article content]

## Good Example

[Code example - to be extracted from article content]

## Related Practices

[Related practices - to be identified]

## Tags

model, security
