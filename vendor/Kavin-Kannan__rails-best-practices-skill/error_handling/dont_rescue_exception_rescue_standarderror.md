# Don't rescue Exception, rescue StandardError

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2012/11/01/don-t-rescue-exception-rescue-standarderror/)

**Original Article Date**: 01 Nov 2012

**Original Author**: Richard Bradley

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

In C# or Java, you can `catch (Exception)` to rescue all exception types. However, in Ruby you should almost never catch `Exception`, but only catch `StandardError`.

## Why

If you omit the `Exception` type qualifier, then Ruby will catch only `StandardError`, which is probably what you want:

begin
      foo
    rescue => e
      logger.warn "Unable to foo, will ignore: #{e}"
    end

## Bad Example

```ruby
begin
      foo
    rescue Exception => e
      logger.warn "Unable to foo, will ignore: #{e}"
    end
```

## Good Example

```ruby
begin
      foo
    rescue => e
      logger.warn "Unable to foo, will ignore: #{e}"
    end
```

## Related Practices

- //stackoverflow.com/questions/10048173/why-is-it-bad-style-to-rescue-exception-e-in-ruby>

## Tags

rescue, exception
