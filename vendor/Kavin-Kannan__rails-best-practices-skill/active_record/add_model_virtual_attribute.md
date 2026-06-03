# Add Model Virtual Attribute

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/21/add-model-virtual-attribute/)

**Original Article Date**: July 21, 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself is a fact about Rails ActiveRecord attributes and community knowledge.

## Description

Do not assign the model's attributes directly in controller. Add model virtual attribute to move the assignment to model.

## Why

In this example, the user form contains a full_name attribute, but we want to save the first_name and last_name in table, so we assign the first_name an last_name for @user object in controller by splitting the full_name.

But assigning attributes for model is not the job of controller, you should let model to handle this by adding virtual attribute.

## Bad Example

```erb
<%= text_field_tag :full_name %>
    <% end %>

    class UsersController < ApplicationController
      def create
        @user = User.new(params[:user])
        @user.first_name = params([:full_name]).split(' ', 2).first
        @user.last_name = params([:full_name]).split(' ', 2).last
        @user.save
      end
    end
```

## Good Example

```erb
def full_name
        [first_name, last_name].join(' ')
      end

      def full_name=(name)
        split = name.split(' ', 2)
        self.first_name = split.first
        self.last_name = split.last
      end
    end

    <% form_for @user do |f| %>
      <%= f.text_field :full_name %>
    <% end %>

    class UsersController < ApplicationController
      def create
        @user = User.create(params[:user])
      end
    end
```

## Related Practices

[Related practices - to be identified]

## Tags

controller, model
