-- {{ config(materialized='table') }}

SELECT
    review_id,
    order_id,
    review_score,
    review_comment_title,
    review_comment_message,
    review_creation_date,
    review_answer_timestamp
FROM {{ source('ecommerce_model_transform', 'olist_order_reviews') }}