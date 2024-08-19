```mermaid
graph TD
    A[CSV Files] -->|Loaded via Docker| B[PostgreSQL]
    B -->|Postgres to GCS| C[GCS]
    C -->|GCS to BigQuery| D[BigQuery]
    D -->|dbt Transformation| E[OlistAnalytics Project]
    E --> F[ecommerce_model_transform (Normalization)]
    F --> G[stg_models]
    G --> H[int_models]
    H --> I[fct_models]

    subgraph stg_models
        G1[stg_orders.sql]
        G2[stg_customers.sql]
        G3[stg_cities.sql]
        G4[stg_zip_codes.sql]
        G5[stg_order_items.sql]
        G6[stg_products.sql]
    end

    subgraph int_models
        H1[int_avg_delivery_time.sql]
        H2[int_orders_by_state.sql]
        H3[int_sales_by_category.sql]
    end

    subgraph fct_models
        I1[fct_sales_by_category.sql]
        I2[fct_avg_delivery_time.sql]
        I3[fct_orders_by_state.sql]
    end
```