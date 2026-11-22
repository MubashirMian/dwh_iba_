{% macro clean_null(col) %}
    NULLIF(NULLIF(NULLIF(TRIM({{ col }}), ''), '\N'), 'NULL')
{% endmacro %}
