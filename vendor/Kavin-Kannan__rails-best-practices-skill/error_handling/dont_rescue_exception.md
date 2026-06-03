# Don't rescue Exception, rescue StandardError

**Source**: [rails-bestpractices.com](https://rails-bestpractices.com/posts/2012/11/01/dont-rescue-exception-rescue-standarderror/)

**Date**: November 1, 2012

**Author**: Richard Bradley

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
