---

# Ask-Moto API Documentation

Welcome to the Ask-Moto API documentation. This API allows you to interact with the Ask-Moto chatbot using two different endpoints: `/chatbot/` for standard interactions and `/chat_stream/` for streaming responses.

## Base URL

The base URL for all API endpoints is `http://localhost:3000` if you are running the API locally. If deployed to a server, replace `localhost` with the appropriate domain or IP address.

## Endpoints

### 1. Root Endpoint

- **URL:** `/`
- **Method:** GET
- **Description:** Root endpoint to welcome users to the Ask-Moto API.

#### Request

No request parameters are required.

#### Response

- **Status Code:** 200 OK
- **Response Body:**
  ```json
  {
    "Hello": "Welcome to the Ask-Moto API!"
  }
  ```

---

### 2. Chat with Ask-Moto (Standard)

- **URL:** `/chatbot/`
- **Method:** POST
- **Description:** Use this endpoint to have a text-based conversation with the Ask-Moto chatbot.

#### Request

- **Body:**
  - `query` (string, required): The user's input query.
  - `chat_logs` (list, optional): List of previous chat logs (default is an empty list).

#### Response

- **Status Code:** 200 OK
- **Response Body:** A JSON object representing the chatbot's response.

---

### 3. Chat with Ask-Moto (Streaming)

- **URL:** `/chat_stream/`
- **Method:** POST
- **Description:** Use this endpoint to have a streaming conversation with the Ask-Moto chatbot. Messages will be streamed as they are generated.

#### Request

- **Body:**
  - `query` (string, required): The user's input query.
  - `chat_logs` (list, optional): List of previous chat logs (default is an empty list).

#### Response

- **Status Code:** 200 OK
- **Response Body:** Messages will be streamed in real-time as they are generated.

---

## Usage Examples

### Example 1: Chat with Ask-Moto (Standard)

**Request:**

```http
POST /chatbot/
Content-Type: application/json

{
  "query": "Tell me a joke."
}
```

**Response:**

```json
{
  "message": "Why don't scientists trust atoms? Because they make up everything!"
}
```

### Example 2: Chat with Ask-Moto (Streaming)

**Request:**

```http
POST /chat_stream/
Content-Type: application/json

{
  "query": "What's the weather like today?"
}
```

**Response:**

```text/event-stream
data: "The weather is sunny with a high of 25°C."
```

---

## Error Handling

In case of errors, the API will return an appropriate HTTP status code (e.g., 400 Bad Request, 500 Internal Server Error) along with an error message in the response body.

---

<!-- ## Additional Information

- **Maintainer:** Your Name
- **Contact:** Your Email Address
- **GitHub Repository:** [Link to GitHub Repository]
- **API Version:** 1.0

Please note that this documentation provides an overview of the Ask-Moto API endpoints and their usage. Detailed information about the chatbot's capabilities and behavior may be found in the chatbot's documentation.

For any inquiries or assistance, please feel free to contact the API maintainer.

Thank you for using the Ask-Moto API! -->