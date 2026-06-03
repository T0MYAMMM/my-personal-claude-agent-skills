# Avoid N+1 Queries

**Source**: [rails-bestpractices.com](https://rails-bestpractices.com/)

## Description

N+1 queries occur when you fetch a collection of records and then access an association on each record, resulting in one query for the collection plus one query per record for the association.

## Why

- N+1 queries are a major performance bottleneck
- Can cause hundreds or thousands of unnecessary database queries
- Significantly slows down application response times
- Can cause database connection pool exhaustion

## Bad Example

```ruby
# Bad - causes N+1 queries
users = User.all
users.each do |user|
  puts user.posts.count  # One query per user
end
# Total: 1 query for users + N queries for posts = N+1 queries
```

## Good Example

```ruby
# Good - uses eager loading
users = User.includes(:posts).all
users.each do |user|
  puts user.posts.count  # No additional queries
end
# Total: 2 queries (one for users, one for posts)

# Or use preload for separate queries
users = User.preload(:posts).all

# Or use eager_load for LEFT OUTER JOIN
users = User.eager_load(:posts).all
```

## When to Use Each

- **includes**: Use when you'll access the association and may need to filter by it
- **preload**: Use when you'll access the association but won't filter by it (separate queries)
- **eager_load**: Use when you need to filter by the association (LEFT OUTER JOIN)

## Related Practices

- Use batched finders for large datasets
- Monitor query performance
- Use query optimization tools

## Tags

performance, active_record, query, n_plus_one, eager_loading

