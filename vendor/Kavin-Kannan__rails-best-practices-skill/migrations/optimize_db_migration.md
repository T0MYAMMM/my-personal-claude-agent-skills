# Optimize db migration

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2011/10/30/optimize-db-migration/)

**Original Article Date**: 30 Oct 2011

**Original Author**: Richard Huang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

rails migration provides a convenient way to alter database structure, you can easily add, change and drop column to a existing table, but when the data in existing table are huge, it will take a long time to alter existing table, you should try to merge/optimize the db alter sql statements.

## Why

Nowadays it's easy to reach millions users for a startup website due to sns success, that means the tables on production server are huge, if you want to alter table structure, like add a new column, it may takes tens of minutes or several hours to execute.

If you want to add a new column and drop an existing column to one existing table, by default rails migration will run two alter sql statements, one for add and the other for drop, so it takes double time, but if we merge/optimize the two alter sql statements into one, it saves the migration time dramatically.

## Bad Example

[Code example - to be extracted from article content]

## Good Example

[Code example - to be extracted from article content]

## Related Practices

[Related practices - to be identified]

## Tags

migration, performance
