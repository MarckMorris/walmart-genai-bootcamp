# Walmart GenAI Bootcamp - Day 4: API & Portfolio Project

This project demonstrates a core GenAI microservice built with FastAPI, integrated with a local Large Language Model (LLM) powered by Ollama. It's a key part of my personal bootcamp to prepare for the Staff Software Engineer, GenAI role at Walmart.

## 🚀 Features
* **FastAPI Microservice:** A high-performance Python API for serving GenAI capabilities.
* **LLM Integration:** Connects to a locally-hosted `llama3` model via Ollama.
* **Dockerized Application:** The entire service is containerized for portability and reproducibility.
* **Interactive Documentation:** Automatic API documentation via Swagger UI (`/docs`).

## 💻 Technologies Used
* **Python:** Core programming language.
* **FastAPI:** Web framework for building the API.
* **Ollama:** Open-source tool for running LLMs locally.
* **Docker:** For containerizing the application.
* **Git/GitHub:** For version control and collaboration.

## 🛠️ How to Run
**Prerequisites:**
* Docker Desktop installed and running.
* Ollama installed and the `llama3` model downloaded (`ollama pull llama3`).
* You can use the automated script from Day 2 to set up the project:
  `chmod +x setup_project.sh`
  `./setup_project.sh`

**Manual Steps:**
1. Clone the repository:
   `git clone https://github.com/MarckMorris/walmart-genai-bootcamp.git`
   `cd walmart-genai-bootcamp`
2. Build the Docker image:
   `docker build -t walmart-genai-api:latest .`
3. Run the container:
   `docker run -p 8000:8000 walmart-genai-api:latest`

## 🧪 API Endpoints
* **`GET /product/{product_id}`:** Retrieves dummy product information.
* **`POST /ask`:** Sends a prompt to the LLM and gets a generated response.
  * **Request Body:** `{ "prompt": "Your question here." }`

**Interactive Documentation:**
Access the API documentation at `http://localhost:8000/docs`.

---
*Built by MarckMorris for the Walmart GenAI Bootcamp.*