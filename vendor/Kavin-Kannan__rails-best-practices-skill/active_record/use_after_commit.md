# use after_commit

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2012/05/02/use-after_commit/)

**Original Article Date**: 02 May 2012

**Original Author**: Richard Huang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

Most developers use AR callbacks after_create/after_update/after_destroy to generate background job, expire cache, etc., but they don't realize these callbacks are still wrapped in database transaction, they probably got unexpected errors on production servers.

## Why

A relational database, like mysql, provides transactions to wrap several operations in one unit, make them all pass or all fail. All isolation levels except READ UNCOMMITTED don't allow read data changes until they are committed in other transaction. If you don't realize it, you probably introduce some unexpected errors.

## Bad Example

```ruby
class Notification < ActiveRecord::Base
      after_create :asyns_send_notification

      def async_send_notification
        NotificationWorker.async_send_notification({:notification_id => id})
      end
    end

    class NotificationWorker < Workling::Base
      def send_notification(params)
        notification = Notification.find(params[:notification_id])
        user = notification.user
        # send notification to user's friends by email
      end
    end

    <tr>
      <th>main process</th>
      <th>worker process</th>
    </tr>

    <tr>
      <td>BEGIN</td>
      <td></td>
    </tr>
    <tr>
      <td>INSERT INTO notifications(message, user_id) values('notification message', 1)</td>
      <td></td>
    </tr>
    <tr>
      <td># return id 10 for newly-created notification</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>SELECT * FROM notifications WHERE id = 10</td>
    </tr>
    <tr>
      <td>COMMIT</td>
      <td></td>
    </tr>

    class Notification < ActiveRecord::Base
      after_commit :asyns_send_notification, :on => :create

      def async_send_notification
        NotificationWorker.async_send_notification({:notification_id => id})
      end
    end

    <tr>
      <th>main process</th>
      <th>worker process</th>
    </tr>

    <tr>
      <td>BEGIN</td>
      <td></td>
    </tr>
    <tr>
      <td>INSERT INTO notifications(message, user_id) values('notification message', 1)</td>
      <td></td>
    </tr>
    <tr>
      <td># return id 10 for newly-created notification</td>
      <td></td>
    </tr>
    <tr>
      <td>COMMIT</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>SELECT * FROM notifications WHERE id = 10</td>
    </tr>
```

## Good Example

```ruby
class Notification < ActiveRecord::Base
      after_commit :asyns_send_notification, :on => :create

      def async_send_notification
        NotificationWorker.async_send_notification({:notification_id => id})
      end
    end

    <tr>
      <th>main process</th>
      <th>worker process</th>
    </tr>

    <tr>
      <td>BEGIN</td>
      <td></td>
    </tr>
    <tr>
      <td>INSERT INTO notifications(message, user_id) values('notification message', 1)</td>
      <td></td>
    </tr>
    <tr>
      <td># return id 10 for newly-created notification</td>
      <td></td>
    </tr>
    <tr>
      <td>COMMIT</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>SELECT * FROM notifications WHERE id = 10</td>
    </tr>
```

## Related Practices

[Related practices - to be identified]

## Tags

model
