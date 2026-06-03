# rolling out with feature flags

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2012/09/02/rolling-out-with-feature-flags/)

**Original Article Date**: 02 Sep 2012

**Original Author**: Richard Huang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself 
is a fact about Rails behavior and community knowledge.

## Description

Sometimes you may face the situation that some features will be released, but you are not sure if it is friendly to end user, or if it will lead to performance issues, at that time you should use what we called "feature flags"

## Why

Rolling out with feature flags means the released feature can be fully or partially turn on/off at the running time. We have a private repository named feature_flags, it allows to release some features to production, but the features are disabled by default, we can activate it after deployment, we can activate it to specific users, to user percentages (like 50% users), or to all users.

Here are some use cases we use feature flags in our product:

## Bad Example

[Code example - to be extracted from article content]

## Good Example

[Code example - to be extracted from article content]

## Related Practices

- https://github.com/jamesgolick/rollout

## Tags

performance
