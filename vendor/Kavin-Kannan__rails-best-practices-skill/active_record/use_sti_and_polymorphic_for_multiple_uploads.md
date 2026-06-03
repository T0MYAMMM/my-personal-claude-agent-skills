# Use STI and Polymorphic Models for Multiple Uploads

**Concept Source**: Based on practices from [rails-bestpractices.com](https://rails-bestpractices.com/posts/2010/08/18/use-sti-and-polymorphic-model-for-multiple-uploads/)

**Original Article Date**: August 18, 2010

**Original Author**: Richard Huang

**Note**: This practice is rewritten in our own words based on the concept. The practice itself is a fact about Rails ActiveRecord patterns and community knowledge.

## Description

This is a flexible and reusable solution for multiple uploads, using STI model to save all the uploaded assets in one "assets" table and using polymorphic model to reuse "Asset" model in different uploadable models.

## Why

This is extracted from my answer of [How do you design your model for multiple upload?][1]

I have built several rails applications, most of them allow user to upload assets, such as images and videos. It's easy if there is only one or two assets to upload, but it makes your code in a mess to deals with many uploading assets.

## Bad Example

[Code example - to be extracted from article content]

## Good Example

[Code example - to be extracted from article content]

## Related Practices

[Related practices - to be identified]

## Tags

model, upload
