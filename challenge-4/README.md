# Challenge 4: Alaska Department of Snow (ADS) FAQ Chatbot

This challenge implements a comprehensive FAQ chatbot system for the Alaska Department of Snow (ADS) with three main components: a frontend web interface, a chatbot service, and a data ingestion service. The system is designed to handle routine inquiries about snow-related services, helping to reduce call volume during peak periods.

## Use Case

The Alaska Department of Snow (ADS) serves 750,000 people across 650,000 square miles and relies on interagency communication to deliver services. During snow forecasts, regional offices face high call volumes with questions about:

- Snow plowing schedules
- School closures
- Road conditions
- Service disruptions
- Emergency services

ADS is exploring an online agent or chatbot to offload routine inquiries, addressing concerns about:

- Cloud service security
- Cost efficiency
- Service reliability
- Data privacy

## System Components

### 1. Frontend Web Interface

<img width="1512" alt="ads-chatbox" src="https://github.com/user-attachments/assets/c1cdfb89-a6f3-4725-b1be-4891080e3d6f" />

- **URL**: [https://storage.googleapis.com/vishnu-ads-chatbot/index.html](https://storage.googleapis.com/vishnu-ads-chatbot/index.html)
- A modern web interface that allows users to interact with the chatbot
- Built with React and styled with modern CSS frameworks
- Provides a user-friendly chat interface for querying ADS services
- Features real-time updates on service status and disruptions

### 2. Chatbot Service

- **URL**: [https://ads-chat-bot-479971105418.europe-west1.run.app](https://ads-chat-bot-479971105418.europe-west1.run.app)
- Handles routine inquiries about ADS services
- Implemented using Python and deployed on Google Cloud Run
- Processes natural language queries about:
  - Snow plowing schedules
  - School closure information
  - Road conditions and closures
  - Service disruptions
  - Emergency services
- Integrates with a vector database for efficient FAQ retrieval

### 3. Data Ingestion Service

- **URL**: [https://ads-data-ingestion-479971105418.europe-west1.run.app](https://ads-data-ingestion-479971105418.europe-west1.run.app)
- Manages the ingestion and processing of ADS service data
- Processes and stores information about:
  - Service schedules
  - Road conditions
  - School closure announcements
  - Emergency alerts
  - Historical service data
- Creates embeddings for efficient semantic search
- Ensures data is properly indexed for the chatbot service

## Project Structure

```
challenge-4/
├── frontend/          # React-based web interface
├── backend/
│   ├── chatbot/      # Chatbot service implementation
│   ├── ingestion/    # Data ingestion service
│   └── evaluation/   # Evaluation notebooks and metrics
```

## Evaluation

The project includes comprehensive evaluation notebooks that assess:

- Response accuracy for routine inquiries
- Response relevance to service queries
- Response time for emergency information
- System performance metrics
- User interaction patterns
- Cost efficiency metrics
- Cloud service reliability

The evaluation notebooks can be found in the `backend/evaluation` directory.

## Getting Started

1. Clone the repository
2. Set up the required environment variables
3. Install dependencies for both frontend and backend services
4. Run the services locally or deploy to cloud infrastructure

## Dependencies

- Python 3.8+
- Node.js 14+
- React
- Vector database (e.g., Pinecone, Weaviate)
- Cloud infrastructure (Google Cloud Run)
- Interagency communication APIs
- Service status monitoring systems

## Deployment

The services are deployed on Google Cloud Run in the europe-west1 region. Each service is containerized and can be scaled independently based on demand, with special consideration for handling increased traffic during peak service periods.

## Contributing

Please refer to the project's contribution guidelines for more information on how to contribute to this project.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
