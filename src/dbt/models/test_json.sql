{{
    config(
        materialized='table'
    )
}}

-- Test JSON parsing in each deduped table
SELECT 
    'people' as table_name,
    uuid,
    external_ids,
    source_uuids,
    CASE 
        WHEN external_ids IS NOT NULL THEN TRY_PARSE_JSON(external_ids::string)
        ELSE NULL 
    END as parsed_external_ids,
    CASE 
        WHEN source_uuids IS NOT NULL THEN TRY_PARSE_JSON(source_uuids::string)
        ELSE NULL 
    END as parsed_source_uuids
FROM {{ ref('claymore_core', 'deduped_people') }}
WHERE external_ids IS NOT NULL OR source_uuids IS NOT NULL
LIMIT 10

UNION ALL

SELECT 
    'deals' as table_name,
    uuid,
    external_ids,
    source_uuids,
    CASE 
        WHEN external_ids IS NOT NULL THEN TRY_PARSE_JSON(external_ids::string)
        ELSE NULL 
    END as parsed_external_ids,
    CASE 
        WHEN source_uuids IS NOT NULL THEN TRY_PARSE_JSON(source_uuids::string)
        ELSE NULL 
    END as parsed_source_uuids
FROM {{ ref('claymore_crm', 'deduped_deals') }}
WHERE external_ids IS NOT NULL OR source_uuids IS NOT NULL
LIMIT 10

UNION ALL

SELECT 
    'loans' as table_name,
    uuid,
    external_ids,
    source_uuids,
    CASE 
        WHEN external_ids IS NOT NULL THEN TRY_PARSE_JSON(external_ids::string)
        ELSE NULL 
    END as parsed_external_ids,
    CASE 
        WHEN source_uuids IS NOT NULL THEN TRY_PARSE_JSON(source_uuids::string)
        ELSE NULL 
    END as parsed_source_uuids
FROM {{ ref('claymore_lending', 'deduped_loans') }}
WHERE external_ids IS NOT NULL OR source_uuids IS NOT NULL
LIMIT 10

UNION ALL

SELECT 
    'payments' as table_name,
    uuid,
    external_ids,
    source_uuids,
    CASE 
        WHEN external_ids IS NOT NULL THEN TRY_PARSE_JSON(external_ids::string)
        ELSE NULL 
    END as parsed_external_ids,
    CASE 
        WHEN source_uuids IS NOT NULL THEN TRY_PARSE_JSON(source_uuids::string)
        ELSE NULL 
    END as parsed_source_uuids
FROM {{ ref('claymore_lending', 'deduped_payments') }}
WHERE external_ids IS NOT NULL OR source_uuids IS NOT NULL
LIMIT 10 