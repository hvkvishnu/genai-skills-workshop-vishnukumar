import os
import json
import logging
import unittest
import requests
import datetime
import pandas as pd
from typing import Dict
from vertexai import init
from vertexai.evaluation import (
    EvalTask,
    MetricPromptTemplateExamples
)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Vertex AI
init(project=os.getenv("qwiklabs-gcp-00-171b5867e51b"), location=os.getenv("VERTEX_AI_LOCATION", "us-central1"))

class TestADSChatBot(unittest.TestCase):
    def setUp(self):
        self.chatbot_url = "https://ads-chat-bot-479971105418.europe-west1.run.app"
        self.validation_prompt = """
        You are a response validation assistant. Your task is to compare the chatbot's response with the expected response and determine if they are semantically equivalent.

        Consider the following criteria:
        1. Key information matches
        2. Intent is preserved
        3. Tone and formality level are appropriate
        4. No critical information is missing
        5. No misleading or incorrect information is added

        Respond with a JSON object in this format:
        {
            "is_valid": true/false,
            "score": 0-1 (where 1 is perfect match),
            "reason": "Brief explanation of why the response is valid/invalid"
        }
        """

    def test_refund_for_property_damage(self):
        self._run_case(
            "How do I request a refund if a private contractor damaged my property?",
            "ADS is not responsible for private contractor damages. Contact the contractor directly or your local municipality for guidance on claims."
        )

    def test_financial_assistance_snow_removal(self):
        self._run_case(
            "Does ADS offer financial assistance for snow removal equipment?",
            "ADS does not provide direct financial assistance. However, some state grants may be available to local governments for purchasing snow removal equipment."
        )

    def test_plows_for_private_property(self):
        self._run_case(
            "Are ADS plows available for hire for private property?",
            "No. ADS resources are dedicated to public roads and infrastructure. Private snow removal must be arranged through local contractors."
        )

    def test_check_road_conditions(self):
        self._run_case(
            "How can I check current road conditions statewide?",
            "Use the ADS “SnowLine” app or visit the official ADS website’s road conditions dashboard, which is updated hourly with closures and warnings."
        )

    def test_avalanche_control(self):
        self._run_case(
            "Does ADS handle avalanche control?",
            "Yes. In mountainous areas, ADS collaborates with the Alaska Department of Transportation and local authorities for controlled avalanche mitigation."
        )

    def _run_case(self, query: str, expected_response: str):
        response = self._make_request(query)
        validation_result = self._validate_response(response, expected_response)
        self.assertTrue(validation_result["is_valid"], f"Validation failed: {validation_result['reason']}")
        self.assertGreaterEqual(validation_result["score"], 0.7)

    def _make_request(self, query: str) -> str:
        """Make a request to the chatbot API"""
        try:
            response = requests.post(
                self.chatbot_url,
                json={"query": query},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()["answer"] or response.json()["response"]
        except Exception as e:
            self.fail(f"Failed to make request to chatbot: {str(e)}")

    def _validate_response(self, actual_response: str, expected_response: str) -> Dict:
        """Validate the chatbot's response against the expected response"""
        try:
            eval_dataset = pd.DataFrame([{
                "instruction": self.validation_prompt,
                "context": f"Expected response: {expected_response}",
                "response": f"Actual response: {actual_response}"
            }])

            run_ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            eval_task = EvalTask(
                dataset=eval_dataset,
                metrics=[
                    MetricPromptTemplateExamples.Pointwise.GROUNDEDNESS,
                    MetricPromptTemplateExamples.Pointwise.SAFETY
                ],
                experiment=f"response-validation-{run_ts}"
            )

            result = eval_task.evaluate(
                prompt_template="Instruction: {instruction}. Context: {context}. Response: {response}",
                experiment_run_name="response-validation"
            )
            print(f"results: {result}")
            metrics = result.metrics_table
            score = (metrics["groundedness/score"].mean() + metrics["safety/score"].mean()) / 2
            
            return {
                "is_valid": score >= 0.7,
                "score": float(score),
                "reason": f"Response matches expected content with score {score:.2f}"
            }

        except Exception as e:
            logger.error(f"Error during response validation: {str(e)}")
            return {
                "is_valid": False,
                "score": 0.0,
                "reason": f"Validation failed: {str(e)}"
            }

if __name__ == '__main__':
    unittest.main()
