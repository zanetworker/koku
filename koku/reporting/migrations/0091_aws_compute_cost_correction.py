# Generated by Django 2.2.9 on 2020-01-24 20:10
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("reporting", "0090_ocpallcostlineitemdailysummary_ocpallcostlineitemprojectdailysummary")]

    operations = [
        migrations.RunSQL(
            sql="""
drop materialized view if exists reporting_aws_compute_summary;

create materialized view reporting_aws_compute_summary as(
select row_number() over(order by c.usage_start, c.instance_type) as id,
       c.usage_start,
       c.usage_start as usage_end,
       c.instance_type,
       r.resource_ids,
       cardinality(r.resource_ids) as resource_count,
       c.usage_amount,
       c.unit,
       c.unblended_cost,
       c.markup_cost,
       c.currency_code
  from (
        -- this group by gets the counts
         select date(usage_start) as usage_start,
                instance_type,
                sum(usage_amount) as usage_amount,
                max(unit) as unit,
                sum(unblended_cost) as unblended_cost,
                sum(markup_cost) as markup_cost,
                max(currency_code) as currency_code
           from reporting_awscostentrylineitem_daily_summary
          where usage_start >= date_trunc('month', now() - '1 month'::interval)
            and usage_start < date_trunc('month', now() + '1 month'::interval)
            and instance_type is not null
          group
             by date(usage_start), instance_type
       ) as c
  join (
        -- this group by gets the distinct resources running by day
         select usage_start,
                instance_type,
                array_agg(distinct resource_id order by resource_id) as resource_ids
           from (
                  select date(usage_start) as usage_start,
                         instance_type,
                         unnest(resource_ids) as resource_id
                    from reporting_awscostentrylineitem_daily_summary
                   where usage_start >= date_trunc('month', now() - '1 month'::interval)
                     and usage_start < date_trunc('month', now() + '1 month'::interval)
                     and instance_type is not null
                ) as x
          group
             by usage_start, instance_type
       ) as r
    on c.usage_start = r.usage_start
   and c.instance_type = r.instance_type
       )
  with data
       ;
-- explain analyze comes in slightly faster on average than using the lateral unnest.
-- The question is: are the numbers correct?

create unique index aws_compute_summary
    on reporting_aws_compute_summary (usage_start, instance_type)
;


drop materialized view if exists reporting_aws_compute_summary_by_service;

create materialized view reporting_aws_compute_summary_by_service as(
select row_number() over(order by c.usage_start, c.product_code, c.product_family, c.instance_type) as id,
       c.usage_start,
       c.usage_start as usage_end,
       c.product_code,
       c.product_family,
       c.instance_type,
       r.resource_ids,
       cardinality(r.resource_ids) as resource_count,
       c.usage_amount,
       c.unit,
       c.unblended_cost,
       c.markup_cost,
       c.currency_code
  from (
        -- this group by gets the counts
         select date(usage_start) as usage_start,
                product_code,
                product_family,
                instance_type,
                sum(usage_amount) as usage_amount,
                max(unit) as unit,
                sum(unblended_cost) as unblended_cost,
                sum(markup_cost) as markup_cost,
                max(currency_code) as currency_code
           from reporting_awscostentrylineitem_daily_summary
          where usage_start >= date_trunc('month', now() - '1 month'::interval)
            and usage_start < date_trunc('month', now() + '1 month'::interval)
            and instance_type is not null
          group
             by date(usage_start),
                product_code,
                product_family,
                instance_type
       ) as c
  join (
        -- this group by gets the distinct resources running by day
         select usage_start,
                product_code,
                product_family,
                instance_type,
                array_agg(distinct resource_id order by resource_id) as resource_ids
           from (
                  select date(usage_start) as usage_start,
                         product_code,
                         product_family,
                         instance_type,
                         unnest(resource_ids) as resource_id
                    from reporting_awscostentrylineitem_daily_summary
                   where usage_start >= date_trunc('month', now() - '1 month'::interval)
                     and usage_start < date_trunc('month', now() + '1 month'::interval)
                     and instance_type is not null
                ) as x
          group
             by date(usage_start),
                product_code,
                product_family,
                instance_type
       ) as r
    on c.usage_start = r.usage_start
   and c.product_code = r.product_code
   and c.product_family = r.product_family
   and c.instance_type = r.instance_type
       )
  with data
       ;


create unique index aws_compute_summary_service
    on reporting_aws_compute_summary_by_service (usage_start, product_code, product_family, instance_type)
;


drop materialized view if exists reporting_aws_compute_summary_by_account;

create materialized view reporting_aws_compute_summary_by_account as(
select row_number() over(order by c.usage_start, c.usage_account_id, c.account_alias_id, c.instance_type) as id,
       c.usage_start,
       c.usage_start as usage_end,
       c.usage_account_id,
       c.account_alias_id,
       c.instance_type,
       r.resource_ids,
       cardinality(r.resource_ids) as resource_count,
       c.usage_amount,
       c.unit,
       c.unblended_cost,
       c.markup_cost,
       c.currency_code
  from (
        -- this group by gets the counts
         select date(usage_start) as usage_start,
                usage_account_id,
                account_alias_id,
                instance_type,
                sum(usage_amount) as usage_amount,
                max(unit) as unit,
                sum(unblended_cost) as unblended_cost,
                sum(markup_cost) as markup_cost,
                max(currency_code) as currency_code
           from reporting_awscostentrylineitem_daily_summary
          where usage_start >= date_trunc('month', now() - '1 month'::interval)
            and usage_start < date_trunc('month', now() + '1 month'::interval)
            and instance_type is not null
          group
             by date(usage_start),
                usage_account_id,
                account_alias_id,
                instance_type
       ) as c
  join (
        -- this group by gets the distinct resources running by day
         select usage_start,
                usage_account_id,
                account_alias_id,
                instance_type,
                array_agg(distinct resource_id order by resource_id) as resource_ids
           from (
                  select date(usage_start) as usage_start,
                         usage_account_id,
                         account_alias_id,
                         instance_type,
                         unnest(resource_ids) as resource_id
                    from reporting_awscostentrylineitem_daily_summary
                   where usage_start >= date_trunc('month', now() - '1 month'::interval)
                     and usage_start < date_trunc('month', now() + '1 month'::interval)
                     and instance_type is not null
                ) as x
          group
             by date(usage_start),
                usage_account_id,
                account_alias_id,
                instance_type
       ) as r
    on c.usage_start = r.usage_start
   and c.usage_account_id = r.usage_account_id
   and c.account_alias_id = r.account_alias_id
   and c.instance_type = r.instance_type
       )
  with data
       ;


create unique index aws_compute_summary_account
    on reporting_aws_compute_summary_by_account (usage_start, usage_account_id, account_alias_id, instance_type)
;


drop materialized view if exists reporting_aws_compute_summary_by_region;

create materialized view reporting_aws_compute_summary_by_region as(
select row_number() over(order by c.usage_start, c.region, c.availability_zone, c.instance_type) as id,
       c.usage_start,
       c.usage_start as usage_end,
       c.region,
       c.availability_zone,
       c.instance_type,
       r.resource_ids,
       cardinality(r.resource_ids) as resource_count,
       c.usage_amount,
       c.unit,
       c.unblended_cost,
       c.markup_cost,
       c.currency_code
  from (
        -- this group by gets the counts
         select date(usage_start) as usage_start,
                region,
                availability_zone,
                instance_type,
                sum(usage_amount) as usage_amount,
                max(unit) as unit,
                sum(unblended_cost) as unblended_cost,
                sum(markup_cost) as markup_cost,
                max(currency_code) as currency_code
           from reporting_awscostentrylineitem_daily_summary
          where usage_start >= date_trunc('month', now() - '1 month'::interval)
            and usage_start < date_trunc('month', now() + '1 month'::interval)
            and instance_type is not null
          group
             by date(usage_start),
                region,
                availability_zone,
                instance_type
       ) as c
  join (
        -- this group by gets the distinct resources running by day
         select usage_start,
                region,
                availability_zone,
                instance_type,
                array_agg(distinct resource_id order by resource_id) as resource_ids
           from (
                  select date(usage_start) as usage_start,
                         region,
                         availability_zone,
                         instance_type,
                         unnest(resource_ids) as resource_id
                    from reporting_awscostentrylineitem_daily_summary
                   where usage_start >= date_trunc('month', now() - '1 month'::interval)
                     and usage_start < date_trunc('month', now() + '1 month'::interval)
                     and instance_type is not null
                ) as x
          group
             by date(usage_start),
                region,
                availability_zone,
                instance_type
       ) as r
    on c.usage_start = r.usage_start
   and c.region = r.region
   and c.availability_zone = r.availability_zone
   and c.instance_type = r.instance_type
       )
  with data
       ;


create unique index aws_compute_summary_region
    on reporting_aws_compute_summary_by_region (usage_start, region, availability_zone, instance_type)
;

            """
        )
    ]
