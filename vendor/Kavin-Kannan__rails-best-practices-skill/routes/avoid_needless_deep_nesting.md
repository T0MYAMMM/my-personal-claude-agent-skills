# Avoid Needless Deep Nesting

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/22/needless-deep-nesting/)

**Original Article Date**: July 22, 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself is a fact about Rails routing design and community knowledge.

## Description

Some people will define 3 or more level nested routes, it's a kind of over design and not recommended.

## Why

Is it really necessary to define the 3-level nested routes? Using nested routes means the nested resources is belongs to the parent resources, as example, the resources comments belong to post. But there is no need to define the resources favorites belong to post, because favorites belong to comment.

And deep level nested routes generate too long and verbose urls.

## Bad Example

```erb
post.resources :comments do |comment|
        comment.resources :favorites
      end
    end

    <%= link_to post_comment_favorite_path(@post, @comment, @favorite) %>
```

## Good Example

```erb
post.resources :comments
    end

    map.resources :comments do |comment|
      comment.resources :favorites
    end

    <%= link_to comment_favorite_path(@comment, @favorite) %>

    map.resources :posts, :shallow => true do |post|
      post.resources :comments do |comment|
        comment.resources :favorites
      end
    end

    <%= link_to comment_favorite_path(@comment, @favorite) %>

                   posts GET    /posts(.:format)                                  {:action=>"index", :controller=>"posts"}
                         POST   /posts(.:format)                                  {:action=>"create", :controller=>"posts"}
                new_post GET    /posts/new(.:format)                              {:action=>"new", :controller=>"posts"}
               edit_post GET    /posts/:id/edit(.:format)                         {:action=>"edit", :controller=>"posts"}
                    post GET    /posts/:id(.:format)                              {:action=>"show", :controller=>"posts"}
                         PUT    /posts/:id(.:format)                              {:action=>"update", :controller=>"posts"}
                         DELETE /posts/:id(.:format)                              {:action=>"destroy", :controller=>"posts"}
           post_comments GET    /posts/:post_id/comments(.:format)                {:action=>"index", :controller=>"comments"}
                         POST   /posts/:post_id/comments(.:format)                {:action=>"create", :controller=>"comments"}
        new_post_comment GET    /posts/:post_id/comments/new(.:format)            {:action=>"new", :controller=>"comments"}
            edit_comment GET    /comments/:id/edit(.:format)                      {:action=>"edit", :controller=>"comments"}
                 comment GET    /comments/:id(.:format)                           {:action=>"show", :controller=>"comments"}
                         PUT    /comments/:id(.:format)                           {:action=>"update", :controller=>"comments"}
                         DELETE /comments/:id(.:format)                           {:action=>"destroy", :controller=>"comments"}
       comment_favorites GET    /comments/:comment_id/favorites(.:format)         {:action=>"index", :controller=>"favorites"}
                         POST   /comments/:comment_id/favorites(.:format)         {:action=>"create", :controller=>"favorites"}
    new_comment_favorite GET    /comments/:comment_id/favorites/new(.:format)     {:action=>"new", :controller=>"favorites"}
           edit_favorite GET    /favorites/:id/edit(.:format)                     {:action=>"edit", :controller=>"favorites"}
                favorite GET    /favorites/:id(.:format)                          {:action=>"show", :controller=>"favorites"}
                         PUT    /favorites/:id(.:format)                          {:action=>"update", :controller=>"favorites"}
                         DELETE /favorites/:id(.:format)                          {:action=>"destroy", :controller=>"favorites"}

    post_comment_path(1, 1)
    comment_path(1)
    comment_favorite_path(1, 1)
    favorite_path(1)
```

## Related Practices

[Related practices - to be identified]

## Tags

rails2, route
