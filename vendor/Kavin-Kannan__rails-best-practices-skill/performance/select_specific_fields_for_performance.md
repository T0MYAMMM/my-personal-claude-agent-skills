# Select specific fields for performance

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/10/19/select-specific-fields-for-performance/)

**Original Article Date**: 19 Oct 2010

**Original Author**: Richard Huang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

In a system like forum, the title and body is displayed on show page, but only title is on index page. You should use select in query to speed up the query and save memory.

## Why

In a system like forum, the title and body is displayed on show page, but only title is on index page. You should use select in query to speed up the query and save memory.

## Bad Example

```ruby
create_table "posts", :force => true do |t|
      t.string   "title"
      t.text     "body"
      t.datetime "created_at"
      t.datetime "updated_at"
      t.integer  "user_id"
      t.text     "formatted_html"
      t.text     "description"
      ...
    end

    class PostsController < ApplicationController
      def index
        @posts = Post.paginate(:page => params[:page])
      end
    end

    SELECT `posts`.* FROM `posts`  LIMIT 0, 10

    class Post < ActiveRecrod::Base
      INDEX_COLUMNS = column_names - ['body', 'formatted_html', 'updated_at']
    end

    class PostsController < ApplicationController
      def index
        @posts = Post.select(Post::INDEX_COLUMNS).paginate(:page => params[:page])
      end
    end

    SELECT id, title, created_at, user_id, description FROM `posts` LIMIT 0, 10
```

## Good Example

```ruby
class Post < ActiveRecrod::Base
      INDEX_COLUMNS = column_names - ['body', 'formatted_html', 'updated_at']
    end

    class PostsController < ApplicationController
      def index
        @posts = Post.select(Post::INDEX_COLUMNS).paginate(:page => params[:page])
      end
    end

    SELECT id, title, created_at, user_id, description FROM `posts` LIMIT 0, 10
```

## Related Practices

[Related practices - to be identified]

## Tags

performance, query
