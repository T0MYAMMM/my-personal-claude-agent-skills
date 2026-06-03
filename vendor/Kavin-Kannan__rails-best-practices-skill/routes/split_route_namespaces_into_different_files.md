# split route namespaces into different files

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2011/05/04/split-route-namespaces-into-different-files/)

**Original Article Date**: 04 May 2011

**Original Author**: Richard Huang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

the routes will become complicated with the growth of your application, contain different namespaces, each with a lot of resources and custom routes, it would be better to split routes into different files according to the namespaces, which makes it easy to maintain the complicated routes.

## Why

I experienced that with the growth of application, the routes becomes very complicated. The following is a simple example

## Bad Example

[Code example - to be extracted from article content]

## Good Example

[Code example - to be extracted from article content]

## Related Practices

- :Routing::Routes.draw do |map|
      map.resources :posts
      map.resources :comments
      map.logout '/logout', :controller => 'sessions', :action => 'destroy'
      map.login '/login', :controller => 'sessions', :action => 'create'
    end

    # config/routes/developer.rb
    ActionController::Routing::Routes.draw do |map|
      map.namespace :developer do |dev|
        dev.resources :posts
        dev.resources :comments
        dev.logout '/logout', :controller => 'sessions', :action => 'destroy'
        dev.login '/login', :controller => 'sessions', :action => 'create'
      end
    end

    # config/routes/admin.rb
    ActionController::Routing::Routes.draw do |map|
      map.namespace :admin do |admin|
        admin.resources :posts
        admin.resources :comments
        admin.logout '/logout', :controller => 'sessions', :action => 'destroy'
        admin.login '/login', :controller => 'sessions', :action => 'create'
      end
    end

    # config/routes/api.rb
    ActionController::Routing::Routes.draw do |map|
      map.namespace :api do |api|
        api.resources :posts
        api.resources :comments
        api.logout '/logout', :controller => 'sessions', :action => 'destroy'
        api.login '/login', :controller => 'sessions', :action => 'create'
      end
    end

Then you should tell rails there are 3 additional route files.

In Rails2, you can create an initializer

    # config/initializers/load_custom_routes.rb
    ActionController::Routing::Routes.add_configuration_file(Rails.root.join('config/routes/developer.rb'))
    ActionController::Routing::Routes.add_configuration_file(Rails.root.join('config/routes/admin.rb'))
    ActionController::Routing::Routes.add_configuration_file(Rails.root.join('config/routes/api.rb'))

In Rails3, you can set the configs in config/application.rb

    config.paths.config.routes.concat Dir[Rails.root.join("config/routes/*.rb")]

Now routes in different namespaces are split into different files, it is easier to maintain, I only change the developer related routes in config/routes/developer.rb, without any possible to change the rotues in admin or api namespace. Besides, rails will only reload the developer routes if you only change the config/routes/developer.rb, instead of reloading the whole routes, which may be expensive when your routes are complicated.

## Tags

route
