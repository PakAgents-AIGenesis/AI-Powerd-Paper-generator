from qdrant_client import QdrantClient

qdrant_client = QdrantClient(
    url="https://90671045-6a1d-4441-847a-ad1f48e28418.europe-west3-0.gcp.cloud.qdrant.io:6333", 
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.P-XxGdbJ0Bmsfouh_8u-XOVzETDNzSpVm9dPCvoyptI",
)

print(qdrant_client.get_collections())