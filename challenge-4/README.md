# Challenge 4: Alaska Department of Snow Chatbot Implementation

This challenge implements a comprehensive chatbot system for the Alaska Department of Snow with three main components: a frontend web interface, a chatbot service, and a data ingestion service. The system is designed to provide intelligent responses to queries about snow conditions, road status, and other winter-related information in Alaska.

## System Components

### 1. Frontend Web Interface
<img width="1512" alt="ads-chatbox" src="https://github.com/user-attachments/assets/c1cdfb89-a6f3-4725-b1be-4891080e3d6f" />

- **URL**: [https://storage.googleapis.com/vishnu-ads-chatbot/index.html](https://storage.googleapis.com/vishnu-ads-chatbot/index.html)
- A modern web interface that allows users to interact with the chatbot
- Built with React and styled with modern CSS frameworks
- Provides a user-friendly chat interface for querying snow-related information
- Features real-time updates on snow conditions and road status

### 2. Chatbot Service

- **URL**: [https://ads-chat-bot-479971105418.europe-west1.run.app](https://ads-chat-bot-479971105418.europe-west1.run.app)
- Handles user queries about snow conditions and winter services
- Implemented using Python and deployed on Google Cloud Run
- Processes natural language queries about:
  - Current snow conditions
  - Road status and closures
  - Weather forecasts
  - Winter safety information
  - Emergency services
- Integrates with a vector database for efficient information retrieval

### 3. Data Ingestion Service

- **URL**: [https://ads-data-ingestion-479971105418.europe-west1.run.app](https://ads-data-ingestion-479971105418.europe-west1.run.app)
- Manages the ingestion and processing of snow-related data
- Processes and stores information about:
  - Snow depth measurements
  - Road conditions
  - Weather forecasts
  - Emergency alerts
  - Historical snow data
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

- Response accuracy for snow-related queries
- Response relevance to winter conditions
- Response time for emergency information
- System performance metrics
- User interaction patterns
- Accuracy of snow condition reporting

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
- Weather API integration
- Snow condition monitoring systems

## Deployment

The services are deployed on Google Cloud Run in the europe-west1 region. Each service is containerized and can be scaled independently based on demand, with special consideration for handling increased traffic during severe weather conditions.

## Contributing

Please refer to the project's contribution guidelines for more information on how to contribute to this project.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
