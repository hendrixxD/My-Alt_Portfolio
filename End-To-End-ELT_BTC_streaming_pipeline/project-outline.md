# Realtime BTC ELT Data Pipeline with Python, Airbyte, Airflow, DBT, Postgress, GreatExpectations, Kafka, terraform.

# Containerized Bitcoin Data Pipeline Project Outline

## 1. Infrastructure Setup (Terraform & Docker)
- Set up GCP project
- Provision GCS buckets and BigQuery datasets
- Create Compute Engine instances for hosting Docker containers
- Configure networking and security
- Set up Vault for secrets management
- Create base Docker images for project components

## 2. Containerization (Docker & Docker Compose)
- Create Dockerfiles for each service:
  - Airbyte
  - Kafka
  - Airflow
  - dbt
  - Apache Spark
  - PostgreSQL
  - Metabase
  - Apache Superset
  - Prometheus
  - Grafana
  - DataHub
- Develop Docker Compose files for:
  - Local development environment
  - Staging environment
  - Production environment

## 3. Data Ingestion (Airbyte & Kafka)
- Configure Airbyte source connector for CoinMarketCap API
- Set up Kafka topics for streaming data
- Implement Airbyte destination to write to Kafka
- Configure Debezium for change data capture from PostgreSQL (if needed)

## 4. Data Lake (GCS)
- Configure GCS as a data lake
- Set up folder structure for raw, processed, and curated data

## 5. Data Warehouse (BigQuery)
- Design schema for Bitcoin data
- Create tables in BigQuery

## 6. Data Transformation (dbt)
- Implement dbt models for transforming raw data in BigQuery
- Create views and materialized views
- Implement dbt-expectations for in-transformation data quality checks

## 7. Advanced Data Processing (Apache Spark) [Optional]
- Set up Spark cluster using Docker containers
- Implement Spark jobs for any processing that's difficult in SQL

## 8. Orchestration (Airflow)
- Set up Airflow DAGs for:
  - Triggering Airbyte syncs
  - Running dbt transformations
  - Executing data quality checks
  - Running Spark jobs (if applicable)
- Utilize Airflow Providers for seamless GCP integration

## 9. Data Quality (Great Expectations)
- Define data quality expectations
- Implement data quality checks in the pipeline
- Set up alerts for data quality issues

## 10. Operational Database (PostgreSQL)
- Set up PostgreSQL container
- Design schema for real-time queries

## 11. Data Visualization (Metabase & Apache Superset)
- Set up Metabase and Apache Superset containers
- Connect to BigQuery and PostgreSQL
- Create dashboards for Bitcoin metrics
- Set up automated reports

## 12. Monitoring and Logging (Prometheus & Grafana)
- Set up Prometheus and Grafana containers
- Implement logging throughout the pipeline
- Create Grafana dashboards for visualizing system health and performance
- Set up alerts for system issues

## 13. Metadata Management (DataHub)
- Set up DataHub container
- Integrate with various components to automatically collect metadata

## 14. Documentation
- Document architecture and data flow
- Create runbooks for common operations and troubleshooting
- Maintain living documentation in DataHub

## 15. Testing
- Implement unit tests for custom code
- Set up integration tests for the entire pipeline
- Create a staging environment using Docker Compose

## 16. Deployment
- Set up CI/CD pipeline for building and pushing Docker images
- Implement Kubernetes for orchestrating containers in production (optional)
- Develop scripts for deploying Docker Compose stacks to production

## 17. Security
- Use Vault container for managing secrets and API keys
- Implement encryption for data at rest and in transit
- Set up IAM roles and permissions
- Conduct security audit
- Implement container security best practices

## 18. Container Orchestration (Optional)
- Evaluate need for Kubernetes based on scale and complexity
- If needed, set up Kubernetes cluster and create Kubernetes manifests

## 19. Local Development Environment
- Create a Docker Compose file for local development
- Implement volume mounts for easy code editing
- Set up environment variable files for different environments
