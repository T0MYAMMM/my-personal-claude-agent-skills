# use OpenStruct when advance search

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/08/25/use-openstruct-when-advance-search/)

**Original Article Date**: 25 Aug 2010

**Original Author**: Alvin Ye

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

use OpenStruct when advance search

## Why

use OpenStruct when advance search

## Bad Example

```erb
<% form_for_tag blabal do |f| %>
      <%= f.text_field_tag :quick, params[:search][:quick] %>
     <%= select_tag("country", options_for_select([["unassigned" , "0" ]] +
                      Country.to_dropdown, region.country_id),
                      {:name => "search[country]"} ) %>
      <%= f.submit "Search" %>
    <% end %>

    require 'ostruct'

    def index
      @search = OpenStruct.new(params[:search])
    end

    <% form_for :search, :url => {:action => "index"}, :html => {:method => :get} do |f| %>
      <%= f.text_field :quick %>
      <%= f.select :quick, Country.to_dropdown %>
      <%= f.submit "Search" %>
    <% end %>
```

## Good Example

[Code example - to be extracted from article content]

## Related Practices

[Related practices - to be identified]

## Tags

search, view
