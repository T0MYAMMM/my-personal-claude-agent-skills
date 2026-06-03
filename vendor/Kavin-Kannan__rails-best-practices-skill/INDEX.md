# Rails Best Practices Index

Complete index of all Rails best practices from [rails-bestpractices.com](https://rails-bestpractices.com/).

## Timezone

- [Avoid time_ago_in_words (Use Client-Side JavaScript)](timezone/avoid_time_ago_in_words.md)
- [Use Time.zone.now instead of Time.now](timezone/use_timezonenow_instead_of_timenow.md)

## ActiveRecord

- [Add Model Virtual Attribute](active_record/add_model_virtual_attribute.md)
- [Annotate your models](active_record/annotate_your_models.md)
- [Check the return value of "save", otherwise use "save!"](active_record/check_save_return_value.md)
- [Check the return value of "save", otherwise use "save!"](active_record/check_the_return_value_of_save_otherwise_use_save.md)
- [default_scope is evil](active_record/default_scope_is_evil.md)
- [DRY Metaprogramming](active_record/dry_metaprogramming.md)
- [Extract into Module](active_record/extract_into_module.md)
- [Extract to composed class](active_record/extract_to_composed_class.md)
- [Fetch current user in models](active_record/fetch_current_user_in_models.md)
- [Fix N+1 Queries](active_record/fix_n1_queries.md)
- [Keep code struture in models consistent](active_record/keep_code_struture_in_models_consistent.md)
- [Keep Finders on Their Own Model](active_record/keep_finders_on_their_own_model.md)
- [Move code into model](active_record/move_code_into_model.md)
- [Move finder to named_scope](active_record/move_finder_to_named_scope.md)
- [Move Model Logic into the Model](active_record/move_model_logic_into_model.md)
- [Name your model methods after their behavior, not implementation.](active_record/name_your_model_methods_after_their_behavior_not_implementation.md)
- [Namespaced models](active_record/namespaced_models.md)
- [Protect mass assignment](active_record/protect_mass_assignment.md)
- [Tell, don't ask](active_record/tell_dont_ask.md)
- [the Law of Demeter](active_record/the_law_of_demeter.md)
- [use after_commit](active_record/use_after_commit.md)
- [Use batched finder for large data query](active_record/use_batched_finder_for_large_data_query.md)
- [Use Batched Finders for Large Data Queries](active_record/use_batched_finders.md)
- [Use collection_model_ids for Many-to-Many Associations](active_record/use_collection_model_ids.md)
- [Replace Complex Creation with Factory Method](active_record/use_factory_method_for_complex_creation.md)
- [Use Model Callbacks](active_record/use_model_callbacks.md)
- [Use Nested Model Forms](active_record/use_nested_model_forms.md)
- [Use Observer](active_record/use_observer.md)
- [Use query attribute](active_record/use_query_attribute.md)
- [Use STI and Polymorphic Models for Multiple Uploads](active_record/use_sti_and_polymorphic_for_multiple_uploads.md)
- [Use STI and polymorphic model for multiple uploads](active_record/use_sti_and_polymorphic_model_for_multiple_uploads.md)

## Controllers

- [Add model virtual attribute](controllers/add_model_virtual_attribute.md)
- [Create base controller](controllers/create_base_controller.md)
- [Don't modify the params hash](controllers/dont_modify_params_hash.md)
- [Don't modify the params hash](controllers/dont_modify_the_params_hash.md)
- [DRY Controller (debate)](controllers/dry_controller_debate.md)
- [Love named_scope](controllers/love_named_scope.md)
- [Move code into controller](controllers/move_code_into_controller.md)
- [Move Model Logic into the Model](controllers/move_model_logic_into_the_model.md)
- [Nested Model Forms](controllers/nested_model_forms.md)
- [Replace Complex Creation with Factory Method](controllers/replace_complex_creation_with_factory_method.md)
- [Simplify render in controllers](controllers/simplify_render_in_controllers.md)
- [Use before_filter](controllers/use_before_filter.md)
- [Use model association](controllers/use_model_association.md)
- [Use model callback](controllers/use_model_callback.md)
- [Use Scope Access](controllers/use_scope_access.md)

## Error Handling

- [Don't rescue Exception, rescue StandardError](error_handling/dont_rescue_exception.md)
- [Don't rescue Exception, rescue StandardError](error_handling/dont_rescue_exception_rescue_standarderror.md)

## Code Organization

- [Active Record Query Interface Optimization](code_organization/active_record_query_interface_optimization.md)
- [DRY your database.yml](code_organization/dry_your_databaseyml.md)
- [Remove Empty Helpers](code_organization/remove_empty_helpers.md)
- [Tell, don't ask](code_organization/tell_dont_ask.md)
- [to_s/to_s(:short)](code_organization/to_sto_sshort.md)
- [Use Namespaced Models](code_organization/use_namespaced_models.md)

## Views

- [Generate polymorphic url](views/generate_polymorphic_url.md)
- [Move code into helper](views/move_code_into_helper.md)
- [Put scripts at the bottom](views/put_scripts_at_the_bottom.md)
- [Replace instance variable with local variable](views/replace_instance_variable_with_local_variable.md)
- [Replace Instance Variables with Local Variables in Partials](views/replace_instance_variables_with_locals.md)
- [Simplify render in views](views/simplify_render_in_views.md)
- [Use render :collection Rails when possible](views/use_render_collection_rails_when_possible.md)

## Migrations

- [Always add DB index](migrations/always_add_db_index.md)
- [Double-check your migrations](migrations/double_check_your_migrations.md)
- [Isolating Seed Data](migrations/isolating_seed_data.md)
- [Make Migrations Reversible When Possible](migrations/make_migrations_reversible.md)
- [Optimize db migration](migrations/optimize_db_migration.md)
- [Use say and say_with_time in Migrations](migrations/use_say_and_say_with_time.md)
- [Use say and say_with_time in migrations to make a useful migration log](migrations/use_say_and_say_with_time_in_migrations_to_make_a_useful_migration_log.md)

## Security

- [Pay more attentions on security](security/pay_more_attentions_on_security.md)

## Code Quality

- [Remove tab](code_quality/remove_tab.md)
- [Remove Trailing Whitespace](code_quality/remove_trailing_whitespace.md)

## Performance

- [Avoid N+1 Queries](performance/avoid_n_plus_one_queries.md)
- [rolling out with feature flags](performance/rolling_out_with_feature_flags.md)
- [Select specific fields for performance](performance/select_specific_fields_for_performance.md)
- [Use asset_host for production server](performance/use_asset_host_for_production_server.md)
- [Use caching !](performance/use_caching.md)
- [Use memoization](performance/use_memoization.md)

## Testing

- [Use 'Background' to consolidate common steps in a feature](testing/use_background_to_consolidate_common_steps_in_a_feature.md)
- [Use nested step to improve readability of ur scenario](testing/use_nested_step_to_improve_readability_of_ur_scenario.md)
- [Write ur own spec macros](testing/write_ur_own_spec_macros.md)
- [Writing specs for 3rd party declaratives](testing/writing_specs_for_3rd_party_declaratives.md)

## Routes

- [Avoid Needless Deep Nesting](routes/avoid_needless_deep_nesting.md)
- [Avoid Overuse of Route Customizations](routes/avoid_overuse_route_customizations.md)
- [Needless deep nesting](routes/needless_deep_nesting.md)
- [Don't Use Default Route if You Use RESTful Design](routes/no_default_route_with_restful.md)
- [Not use default route if you use RESTful design](routes/not_use_default_route_if_you_use_restful_design.md)
- [Overuse route customizations](routes/overuse_route_customizations.md)
- [Restrict Auto-Generated Routes](routes/restrict_auto_generated_routes.md)
- [split route namespaces into different files](routes/split_route_namespaces_into_different_files.md)

## General

- [comment your magic codes](general/comment_your_magic_codes.md)
- [defer expensive job](general/defer_expensive_job.md)
- [DRY bundler in capistrano](general/dry_bundler_in_capistrano.md)
- [monitor your backend services](general/monitor_your_backend_services.md)
- [speed up assets precompile with turbo-sprockets-rails3](general/speed_up_assets_precompile_with_turbo_sprockets_rails3.md)
- [split your cap tasks into different files](general/split_your_cap_tasks_into_different_files.md)
- [Use css sprite automatically](general/use_css_sprite_automatically.md)
- [Use I18n.localize for date/time formating](general/use_i18nlocalize_for_datetime_formating.md)
- [use OpenStruct when advance search](general/use_openstruct_when_advance_search.md)

## Source

All practices are sourced from [rails-bestpractices.com](https://rails-bestpractices.com/).

## How to Use

1. **For Development**: Reference practices when writing code
2. **For Code Review**: Check code against these practices
3. **For CI/CD**: Integrate checks into your pipeline
4. **For Team**: Use as coding standards

## Contributing

When adding new practices:
1. Create a markdown file in the appropriate category
2. Include: title, description, examples, and source link
3. Update this index
4. Follow the existing format

