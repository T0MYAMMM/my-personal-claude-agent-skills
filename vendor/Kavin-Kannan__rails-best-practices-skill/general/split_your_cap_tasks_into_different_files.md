# split your cap tasks into different files

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2012/09/10/split-your-cap-tasks-into-different-files/)

**Original Article Date**: 10 Sep 2012

**Original Author**: Richard Huang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

Your capistrano deploy.rb file might become complicated with the growth of your application, contain more and more cap tasks, it would be better to split these tasks into different files according to the functionalities, which makes it easy to maintain, and they are more likely to be reused in the future.

## Why

Inspired by require external capistrano recipes (like bundler and rvm), I prefer splitting the tasks into different files according to the functionalities, like

# config/deploy/recipes/asset_pipeline.rb
    set :assets_dependencies, %w(app/assets lib/assets vendor/assets Gemfile.lock config/routes.rb)

## Bad Example

```ruby
# config/deploy.rb
    require 'capistrano_colors'
    require 'bundler/capistrano'

    set :user, 'huangzhi'
    ......
    role :web, "app.example.com"
    role :app, "app.example.com"
    role :db,  "db.example.com", :primary => true

    after "deploy", "cron:update"
    after "deploy", "sitemap:refresh"
    set :assets_dependencies, %w(app/assets lib/assets vendor/assets Gemfile.lock config/routes.rb)

    namespace :cron do
      task :update do
        update_app
        update_db
      end
      task :update_app do
        # update cron jobs on app servers
      end
      task :update_db do
        # update cron jobs on db servers
      end
    end

    namespace :sitemap do
      task :refresh, :roles => :app do
        # generate sitemap.xml for SEO
      end
    end

    namespace :deploy do
      namespace :assets do
        task :precompile, :roles => :web, :except => { :no_release => true } do
          # precompile asset only when asset changes
        end
      end
    end

    namespace :deploy do
      task :start do ; end
      task :stop do ; end
      task :restart, :roles => :app, :except => { :no_release => true } do
        # restart app servers
      end
    end
```

## Good Example

```ruby
# config/deploy/recipes/asset_pipeline.rb
    set :assets_dependencies, %w(app/assets lib/assets vendor/assets Gemfile.lock config/routes.rb)

    namespace :deploy do
      namespace :assets do
        task :precompile, :roles => :web, :except => { :no_release => true } do
          # precompile asset only when asset changes
        end
      end
    end

    # config/deploy/recipes/cron.rb
    after "deploy", "cron:update"

    namespace :cron do
      task :update do
        update_app
        update_db
      end
      task :update_app do
        # update cron jobs on app servers
      end
      task :update_db do
        # update cron jobs on db servers
      end
    end

    # config/deploy/recipes/sitemap.rb
    after "deploy", "sitemap:refresh"

    namespace :sitemap do
      task :refresh, :roles => :app do
        # generate sitemap.xml for SEO
      end
    end

    # config/deploy.rb
    require 'capistrano_colors'
    require 'bundler/capistrano'

    set :user, 'huangzhi'
    ......
    role :web, "app.example.com"
    role :app, "app.example.com"
    role :db,  "db.example.com", :primary => true

    load 'config/deploy/recipes/asset_pipeline'
    load 'config/deploy/recipes/cron'
    load 'config/deploy/recipes/sitemap'

    namespace :deploy do
      task :start do ; end
      task :stop do ; end
      task :restart, :roles => :app, :except => { :no_release => true } do
        # restart app servers
      end
    end

    Dir['vendor/plugins/*/recipes/*.rb', 'config/deploy/recipes/*.rb'].each { |plugin| load(plugin) }
```

## Related Practices

[Related practices - to be identified]

## Tags

deployment, capistrano
