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

### 2. Chat with Ask-Moto

- **URL:** `/chatbot/`
- **Method:** POST
- **Description:** Use this endpoint to have a text-based conversation with the Ask-Moto chatbot.

#### Request

- **Query:**
  - `query` (string, required): The user's input query.

#### Response

- **Status Code:** 200 OK
- **Response Body:** A JSON object representing the chatbot's response.

---


## Usage Examples

### Example 1: Chat with Ask-Moto (Standard)

**Request:**

```http
POST /chatbot/
Content-Type: application/json

{
  "query": "what is motopay."
}
```

**Response:**

```
  "MotoPay is a digital bank providing scan-to-pay methods for bill payments, social connectivity, free calls and chats, online shopping, and access to a wide range of shops. It simplifies transactions for merchants and users through a personalized bank account and a QR code."

```

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