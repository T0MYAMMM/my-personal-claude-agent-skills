# Use Observer

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/07/24/use-observer/)

**Original Article Date**: 24 Jul 2010

**Original Author**: Wen-Tien Chang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

Observer serves as a connection point between models and some other subsystem whose functionality is used by some of other classes, such as email notification. It is loose coupling in contract with model callback.

## Why

In this example, we use the model callback to send email notifications after creating a project. It would be better to use Observer because the email notification is a subsystem whose functionality is used by other classes.

class Project < ActiveRecord::Base
      # nothing here
    end

## Bad Example

```ruby
after_create :send_create_notifications

      private
        def send_create_notifications
          self.members.each do |member|
            ProjectMailer.deliver_notification(self, member)
          end
        end
    end
```

## Good Example

```ruby
# nothing here
    end

    class NotificationObserver < ActiveRecord::Observer
      observe Project

      def after_create(project)
        project.members.each do |member|
          ProjectMailer.deliver_notice(project, member)
        end
      end
    end
```

## Related Practices

[Related practices - to be identified]

## Tags

model, observer
