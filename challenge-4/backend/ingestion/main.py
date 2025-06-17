import functions_framework
import os
import json
from flask import Flask, request, jsonify
from google.cloud import bigquery
from google.auth import default
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Configuration
PROJECT_ID = os.environ.get('PROJECT_ID', 'qwiklabs-gcp-00-171b5867e51b')
DATASET_NAME = 'ADS'
CONNECTION_NAME = 'us.ads-connection'
EMBEDDING_MODEL_NAME = f'{DATASET_NAME}.Embeddings'
TABLE_NAME = f'{DATASET_NAME}.ads_faq'
EMBEDDINGS_TABLE_NAME = f'{DATASET_NAME}.ads_faq_embeddings'

# Initialize BigQuery client
client = bigquery.Client(project=PROJECT_ID)

def create_dataset():
    """Create the ADS dataset if it doesn't exist"""
    try:
        dataset_id = f"{PROJECT_ID}.{DATASET_NAME}"
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"
        dataset.description = "Alaska Department of Snow for embeddings and ML operations"
        
        # Create dataset, ignore if already exists
        dataset = client.create_dataset(dataset, exists_ok=True)
        logger.info(f"Dataset {dataset.dataset_id} created or already exists")
        return True
    except Exception as e:
        logger.error(f"Error creating dataset: {str(e)}")
        return False

def create_embedding_model():
    """Create the embedding model"""
    try:
        query = f"""
        CREATE OR REPLACE MODEL `{EMBEDDING_MODEL_NAME}`
        REMOTE WITH CONNECTION `{CONNECTION_NAME}`
        OPTIONS (ENDPOINT = 'text-embedding-005');
        """
        result = client.query(query)
        result.result()  # Wait for completion
        logger.info(f"Embedding model {EMBEDDING_MODEL_NAME} created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating embedding model: {str(e)}")
        return False

def create_ads_table():
    """Create the main ADS table"""
    try:
        query = f"""
        CREATE TABLE IF NOT EXISTS `{TABLE_NAME}` (
            question STRING,
            answer STRING
        );
        """
        result = client.query(query)
        result.result()
        logger.info(f"Table {TABLE_NAME} created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating ads table: {str(e)}")
        return False

def load_faq_data(csv_uri):
    """Load sample advertisement data"""
    try:
        query = f"""
        LOAD DATA OVERWRITE `{TABLE_NAME}`
        (
            question STRING,
            answer STRING
        )
        FROM FILES (
            format = 'CSV',
            uris = ['{csv_uri}']
        );
        """
        result = client.query(query)
        result.result()
        logger.info(f"ADS FAQ data loaded sucessfully!")
        return True
    except Exception as e:
        logger.error(f"Error loading FAQ data: {str(e)}")
        return False

def create_embeddings():
    """Create embeddings table for the ads data"""
    try:
        query = f"""
        CREATE OR REPLACE TABLE `{EMBEDDINGS_TABLE_NAME}` AS
        SELECT
            *
        FROM
            ML.GENERATE_TEXT_EMBEDDING(
                MODEL `{EMBEDDING_MODEL_NAME}`,
                (SELECT
                    question,
                    answer,
                    CONCAT(question, ': ', answer) AS content
                FROM
                    `{TABLE_NAME}`
                )
            );
        """
        result = client.query(query)
        result.result()
        logger.info(f"Embeddings table {EMBEDDINGS_TABLE_NAME} created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating embeddings: {str(e)}")
        return False

@functions_framework.http
def load_ads_data(request):
    """Setup & load complete ADS data"""
    results = {}
    
    try:
        request_data = request.get_json()
        csv_uri = request_data['csv_uri']
        if not csv_uri:
            return jsonify({
                    "status": "error",
                    "message": "Either 'csv_uri' or 'ads_data' must be provided"
                }), 400

        # Step 1: Create Dataset
        results['dataset'] = create_dataset()
        
        # Step 2: Create Embedding Model
        results['embedding_model'] = create_embedding_model()
        
        # Step 3: Create ADS Table
        results['ads_table'] = create_ads_table()
        
        # Step 4: Load Sample Data
        results['sample_data'] = load_faq_data(csv_uri)
        
        # Step 5: Create Embeddings
        results['embeddings'] = create_embeddings()
        
        success_count = sum(results.values())
        
        response = {
            "status": "completed",
            "results": results,
            "success_count": success_count,
            "total_steps": len(results),
            "message": f"ADS infrastructure setup completed. {success_count}/{len(results)} steps successful."
        }
        
        if success_count == len(results):
            return jsonify(response), 200
        else:
            return jsonify(response), 206  # Partial success
            
    except Exception as e:
        logger.error(f"Setup failed: {str(e)}")
        return jsonify({
            "status": "failed",
            "error": str(e),
            "results": results
        }), 500
