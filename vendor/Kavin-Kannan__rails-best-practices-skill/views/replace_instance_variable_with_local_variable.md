# Replace instance variable with local variable

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/24/replace-instance-variable-with-local-variable/)

**Original Article Date**: 24 Jul 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

In partial view, we can use the instance variable directly, but it may be confused and make it hard to reuse anywhere, because we don't know exactly which instance variable can be used, so use the local variable in partial with explicitly assignment.

## Why

In this example, the partial sidebar can use the instance variable @post, but we can't know what's the instance variable @post without checking the controller codes. Let's use the local variable instead.

<%= render :partial => "sidebar", :locals => { :post => @post } %>

## Bad Example

```erb
def show
        @post = Post.find(params[:id])
      end
    end

    <%= render :partial => "sidebar" %>
```

## Good Example

```erb
<%= render "sidebar", :post => @post %>
```

## Related Practices

[Related practices - to be identified]

## Tags

view
