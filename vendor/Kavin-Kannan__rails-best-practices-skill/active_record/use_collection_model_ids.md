# Use collection_model_ids for Many-to-Many Associations

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/22/model-collection-model-ids-many-to-many/)

**Original Article Date**: July 22, 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself is a fact about Rails ActiveRecord associations and community knowledge.

## Description

When you want to associate a model to many associated models by checkbox on a view, you should take advantage of `model.collection_model_ids` to reduce the code in the controller. This Rails feature automatically handles the assignment of associated records through their IDs.

## Why

- Simplifies controller code for many-to-many associations
- Reduces boilerplate code
- Automatically handles association updates
- Works seamlessly with form helpers
- Follows Rails conventions

## Bad Example

```ruby
# Bad - manually handling associations
class UsersController < ApplicationController
  def update
    @user = User.find(params[:id])
    @user.update(user_params)
    
    # Manually handling role associations
    if params[:user][:role_ids].present?
      @user.roles.clear
      params[:user][:role_ids].each do |role_id|
        @user.roles << Role.find(role_id)
      end
    end
    
    redirect_to @user
  end
end
```

## Good Example

```ruby
# Good - use collection_model_ids
class User < ApplicationRecord
  has_and_belongs_to_many :roles
end

class UsersController < ApplicationController
  def update
    @user = User.find(params[:id])
    if @user.update(user_params)
      redirect_to @user
    else
      render :edit
    end
  end
  
  private
  
  def user_params
    params.require(:user).permit(:name, :email, role_ids: [])
  end
end

# In the view
<%= form_with model: @user do |f| %>
  <%= f.collection_check_boxes :role_ids, Role.all, :id, :name %>
<% end %>
```

## Related Practices

- Use strong parameters
- Keep controllers thin
- Move model logic into the model

## Tags

controller, model, view, associations, many_to_many, has_and_belongs_to_many

