# Don't modify the params hash

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2013/09/18/don-t-modify-the-params-hash/)

**Original Article Date**: 18 Sep 2013

**Original Author**: David Davis

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

The params hash contains all the data that was submitted from a request. If you modify it, later code won't have access to it. Instead, copy the params hash and modify the copy.

## Why

Supposing someone later would add code to the end of this action that needed params[:action] or params[:controller], they would have to refactor your code.

def search
       filter = params.except(:action, :controller)
       @search = User.search(filter)
       render "search"
    end

## Bad Example

```ruby
def search
       params.except!(:action, :controller)
       @search = User.search(params)
       render "search"
     end
```

## Good Example

```ruby
def search
       filter = params.except(:action, :controller)
       @search = User.search(filter)
       render "search"
    end

    def search
      @search = User.search(search_params)
      render "search"
    end

    private

    def search_params
      # params.except(:action, :controller)
      params.permit(:user_id, :name)
    end
```

## Related Practices

[Related practices - to be identified]

## Tags

controller, params
