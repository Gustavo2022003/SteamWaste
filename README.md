# SteamWaste
SteamWaste is a web application that allows users to enter their SteamID to analyze their game library, showing how many games they own, how many they've never played, the dollar value of unplayed games, and the estimated total value of their collection.

[![My Skills](https://skillicons.dev/icons?i=docker,html,css,tailwind,python,fastapi,js)]()

## 🚀 Getting Started

Follow the instructions below to run SteamWaste locally on your machine.

### 📦 Prerequisites

You'll need to have [Docker](https://www.docker.com/) installed. Docker simplifies running the app by containerizing everything — no need to manually install dependencies or configure environments.

> Don’t have Docker yet? Download and install it from [here](https://www.docker.com/).

---

### 🛠️ Running the Project Locally

1. **Clone or Download the Repository**

   * Option 1: [Fork this repository](https://github.com/Gustavo2022003/SteamWaste/fork)
   * Option 2: [Download as ZIP](https://github.com/Gustavo2022003/SteamWaste/archive/refs/heads/main.zip) and extract it to your preferred location

2. **Navigate to the Project Directory**

   ```bash
   cd SteamWaste
   ```

3. **Set Up Environment Variables**

   Create a file named `.env` in the project root and add your Steam API key:

   ```env
   API_KEY=[your_key_here]
   ```

   You can obtain your API key [here](https://steamcommunity.com/dev/apikey).

4. **Build and Run with Docker**

   ```bash
   docker compose up -d --build
   ```

5. **Access the Application**

   Once running, open your browser and visit:

   ```
   http://localhost:8000
   ```

## 💡 Features

* Clean and responsive UI built with TailwindCSS
* Built with FastAPI for fast and efficient backend processing
* Dockerized for easy deployment and development
* Real-time analysis of your Steam library based on your SteamID

---


## 🤝 Contributing

Feel free to contribute! You can:

* Report bugs
* Suggest new features
* Submit pull requests

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---
