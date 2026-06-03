# Use Nested Model Forms

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/22/nested-model-forms/)

**Original Article Date**: July 22, 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself is a fact about Rails ActiveRecord features and community knowledge.

## Description

Use accepts_nested_attributes_for to make nested model forms much easier, this feature is provided by rails 2.3

## Why

Product and Detail models are one-to-one association, we want to create a product with a new manufacturer. In this example, we create a product and a detail object, and associate them in a transaction. But why we do the complex creation in the controller, Product model should take charge of creating a detail.

class Product < ActiveRecord::Base
      has_one :detail
      accepts_nested_attributes_for :detail
    end

## Bad Example

```erb
has_one :detail
    end

    class Detail < ActiveRecord::Base
      belongs_to :product
    end

    <% form_for :product do |f| %>
      <%= f.text_field :title %>
      <% fields_for :detail do |detail| %>
        <%= detail.text_field :manufacturer %>
      <% end %>
    <% end %>

    class ProductsController < ApplicationController
      def create
        @product = Product.new(params[:product])
        @detail = Detail.new(params[:detail])

        Product.transaction do
          @product.save!
          @detail.product = @product
          @detail.save
        end
      end
    end
```

## Good Example

```erb
has_one :detail
      accepts_nested_attributes_for :detail
    end

    <% form_for :product do |f| %>
      <%= f.text_field :title %>
      <% f.fields_for :detail do |detail| %>
        <%= detail.text_field :manufacturer %>
      <% end %>
    <% end %>

    class ProductsController < ApplicationController
      def create
        @product = Product.new(params[:product])
        @product.save
      end
    end

    class Project < ActiveRecord::Base
      has_many :tasks
      accepts_nested_attributes_for :tasks
    end

    class Task < ActiveRecord::Base
      belongs_to :project
    end

    <% form_for @project do |f| %>
      <%= f.text_field :name %>
      <% f.fields_for :tasks do |tasks_form| %>
        <%= tasks_form.text_field :name %>
      <% end %>
    <% end %>
```

## Related Practices

[Related practices - to be identified]

## Tags

controller, model, view
