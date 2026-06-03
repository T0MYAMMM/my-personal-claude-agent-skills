# Use Batched Finders for Large Data Queries

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/09/09/use-batched-finder-for-large-data-query/)

**Original Article Date**: September 9, 2010

**Original Author**: Richard Huang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself is a fact about Rails ActiveRecord performance and community knowledge.

## Description

If you want to do a large data query such as finding all the 10,000,000 users to send email to them, you should use batched finder to avoid eating too much memory.

## Why

If you want to do a large data query such as finding all the 10,000,000 users to send email to them, you should use batched finder to avoid eating too much memory.

## Bad Example

[Code example - to be extracted from article content]

## Good Example

[Code example - to be extracted from article content]

## Related Practices

- batch_size => 5000) do |users|
      users.each { |user| NewsLetter.weekly_deliver(user) }
    end

This method is very useful for large data query, saving your memory and time.

## Tags

model, performance, task
