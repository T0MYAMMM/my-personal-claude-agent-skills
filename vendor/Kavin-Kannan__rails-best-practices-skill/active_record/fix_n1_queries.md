# Fix N+1 Queries

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/25/fix-n-1-queries/)

**Original Article Date**: 25 Jul 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

N+1 Queries is a serious database performance problem. Be careful of that situation! If you're not sure, I recommend you install http://github.com/flyerhzm/bullet plugin, which helps you reduce the number of queries with alerts (and growl).

## Why

When @users.each in view, it cause N+1 queries. (N is 20 in this case)

# your controller
    def index
      @users = User.paginate( :include => :car, :page => params[:page], :per_page => 20 )
    end

## Bad Example

```erb
def index
      @users = User.paginate( :page => params[:page], :per_page => 20 )
    end

    # view
    <% @users.each do |user| %>
       <%= user.car.name %>
    <% end %>
```

## Good Example

```ruby
def index
      @users = User.paginate( :include => :car, :page => params[:page], :per_page => 20 )
    end
```

## Related Practices

[Related practices - to be identified]

## Tags

model, plugin
