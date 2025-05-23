"""
Tests for OpenLIT resource attributes functionality.

This module tests the resource_attributes parameter added to openlit.init()
by creating spans and verifying the resource attributes are properly set.
"""

import openlit
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, TELEMETRY_SDK_NAME, DEPLOYMENT_ENVIRONMENT


def test_resource_attributes_basic():
    """Test that resource_attributes parameter works correctly."""
    custom_attributes = {
        "service.version": "1.0.0",
        "team": "test-team",
        "region": "us-west-1",
        "deployment.environment": "production" # override default
    }
    
    openlit.init(
        application_name="resource-test-app",
        environment="development",
        resource_attributes=custom_attributes,
        disabled_instrumentors=["ollama"]
    )
    
    @openlit.trace
    def test_function():
        return "success"
    
    result = test_function()
    
    assert result == "success"
    
    tracer_provider = trace.get_tracer_provider()
    if hasattr(tracer_provider, '_resource'):
        attributes = tracer_provider._resource.attributes
        
        assert attributes[SERVICE_NAME] == "resource-test-app"
        assert attributes[TELEMETRY_SDK_NAME] == "openlit"
        
        assert "service.version" in attributes
        assert attributes["service.version"] == "1.0.0"
        assert attributes["team"] == "test-team"
        assert attributes["region"] == "us-west-1"
        
        assert attributes[DEPLOYMENT_ENVIRONMENT] == "production"
        
        print("Resource attributes test passed successfully!")
        print(f"Service name: {attributes[SERVICE_NAME]}")
        print(f"Environment: {attributes[DEPLOYMENT_ENVIRONMENT]}")
        print(f"Custom attributes: service.version={attributes.get('service.version')}, team={attributes.get('team')}")

