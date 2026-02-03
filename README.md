# 📈 Real-Time Stock Market Analysis System

![Dashboard Screenshot](Dashboard_Screenshot.png)

A high-performance, real-time stock market analysis system powered by **Apache Kafka**, **Machine Learning (LSTM)**, and a modern **Web Dashboard**.

## 🚀 Features

*   **Real-Time Data Streaming**: Ingests and processes live stock data using Apache Kafka.
*   **Machine Learning Predictions**: Uses an LSTM (Long Short-Term Memory) neural network to predict future stock prices in real-time.
*   **Interactive Dashboard**: A stunning, single-page web interface featuring:
    *   Live stock tickers with real-time updates.
    *   Dynamic price trend charts (Chart.js).
    *   ML-powered price predictions.
    *   Instant volume spike alerts.
    *   Real-time system statistics.
*   **Scalable Architecture**: Built with a decoupled microservices approach (Producer, Consumer, Predictor, Dashboard).

## 🛠️ Tech Stack

*   **Core**: Python 3.9+
*   **Streaming**: Apache Kafka, Zookeeper
*   **ML/AI**: TensorFlow/Keras (LSTM), Scikit-learn
*   **Web**: Flask, Flask-SocketIO
*   **Frontend**: HTML5, CSS3 (Glassmorphism), JavaScript, Chart.js

## 📂 Project Structure

```
├── src/
│   ├── producer.py          # Simulates/Fetches live stock data -> Kafka
│   ├── consumer_storage.py  # Consumes data -> Storage (Data Lake simulation)
│   ├── alert_system.py      # Monitors for anomalies -> Triggers Alerts
│   ├── model_train.py       # Trains the LSTM model on historical data
│   ├── predictor.py         # Real-time inference engine
│   ├── dashboard.py         # Flask web server & Socket.IO backend
│   ├── static/              # CSS, JS, Assets
│   └── templates/           # HTML Templates
├── setup_local_kafka.ps1    # Script to download & setup Kafka locally
├── run_project.ps1          # One-click script to run the entire system
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

## ⚡ Quick Start

### 1. Prerequisites
*   Python 3.8+ installed.
*   Java (JDK 8 or 11) installed (required for Kafka).

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/real-time-stock-analysis.git
cd real-time-stock-analysis

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Setup Kafka
Run the setup script to download and configure Kafka automatically:
```powershell
.\setup_local_kafka.ps1
```

### 4. Run the System
We provide a single script to launch Zookeeper, Kafka, and all Python components:

```powershell
.\run_project.ps1
```

**Alternatively, run components manually in separate terminals:**
1.  `.\start_zookeeper.ps1`
2.  `.\start_kafka.ps1`
3.  `python src/producer.py`
4.  `python src/predictor.py`
5.  `python src/dashboard.py`

### 5. Access Dashboard
Open your browser and navigate to:
**[http://localhost:5001](http://localhost:5001)**

## 🧠 Machine Learning Model
The system uses a Long Short-Term Memory (LSTM) network, trained on historical stock data, to predict the next price point based on the last sequence of prices.
*   **Training**: Run `python src/model_train.py` to retrain the model.
*   **Inference**: The `predictor.py` service loads the saved model and performs real-time inference on streaming Kafka data.

## 📷 Screenshots

### Live Dashboard
The dashboard provides a comprehensive view of the market state, including live feeds, predictions, and system health.

*(See header image)*

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

**Ratnesh Kumar**

*   **GitHub**: [Ratnesh-181998](https://github.com/Ratnesh-181998)
*   **LinkedIn**: [Ratnesh Kumar](https://www.linkedin.com/in/ratneshkumar1998/)
*   **Email**: [rattudacsit2021gate@gmail.com](mailto:rattudacsit2021gate@gmail.com)

---
*Built with ❤️ by Ratnesh Kumar*

---


<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=24,20,12,6&height=3" width="100%">


## 📜 **License**

![License](https://img.shields.io/badge/License-MIT-success?style=for-the-badge&logo=opensourceinitiative&logoColor=white)

**Licensed under the MIT License** - Feel free to fork and build upon this innovation! 🚀

---

# 📞 **CONTACT & NETWORKING** 📞


### 💼 Professional Networks

[![LinkedIn](https://img.shields.io/badge/💼_LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ratneshkumar1998/)
[![GitHub](https://img.shields.io/badge/🐙_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Ratnesh-181998)
[![X](https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/RatneshS16497)
[![Portfolio](https://img.shields.io/badge/🌐_Portfolio-FF6B6B?style=for-the-badge&logo=google-chrome&logoColor=white)](https://share.streamlit.io/user/ratnesh-181998)
[![Email](https://img.shields.io/badge/✉️_Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:rattudacsit2021gate@gmail.com)
[![Medium](https://img.shields.io/badge/Medium-000000?style=for-the-badge&logo=medium&logoColor=white)](https://medium.com/@rattudacsit2021gate)
[![Stack Overflow](https://img.shields.io/badge/Stack_Overflow-F58025?style=for-the-badge&logo=stack-overflow&logoColor=white)](https://stackoverflow.com/users/32068937/ratnesh-kumar)

### 🚀 AI/ML & Data Science
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://share.streamlit.io/user/ratnesh-181998)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/RattuDa98)
[![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/rattuda)

### 💻 Competitive Programming (Including all coding plateform's 5000+ Problems/Questions solved )
[![LeetCode](https://img.shields.io/badge/LeetCode-FFA116?style=for-the-badge&logo=leetcode&logoColor=black)](https://leetcode.com/u/Ratnesh_1998/)
[![HackerRank](https://img.shields.io/badge/HackerRank-00EA64?style=for-the-badge&logo=hackerrank&logoColor=black)](https://www.hackerrank.com/profile/rattudacsit20211)
[![CodeChef](https://img.shields.io/badge/CodeChef-5B4638?style=for-the-badge&logo=codechef&logoColor=white)](https://www.codechef.com/users/ratnesh_181998)
[![Codeforces](https://img.shields.io/badge/Codeforces-1F8ACB?style=for-the-badge&logo=codeforces&logoColor=white)](https://codeforces.com/profile/Ratnesh_181998)
[![GeeksforGeeks](https://img.shields.io/badge/GeeksforGeeks-2F8D46?style=for-the-badge&logo=geeksforgeeks&logoColor=white)](https://www.geeksforgeeks.org/profile/ratnesh1998)
[![HackerEarth](https://img.shields.io/badge/HackerEarth-323754?style=for-the-badge&logo=hackerearth&logoColor=white)](https://www.hackerearth.com/@ratnesh138/)
[![InterviewBit](https://img.shields.io/badge/InterviewBit-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://www.interviewbit.com/profile/rattudacsit2021gate_d9a25bc44230/)


---

## 📊 **GitHub Stats & Metrics** 📊



![Profile Views](https://komarev.com/ghpvc/?username=Ratnesh-181998&color=blueviolet&style=for-the-badge&label=PROFILE+VIEWS)





<img src="https://github-readme-streak-stats.herokuapp.com/?user=Ratnesh-181998&theme=radical&hide_border=true&background=0D1117&stroke=4ECDC4&ring=F38181&fire=FF6B6B&currStreakLabel=4ECDC4" width="48%" />




<img src="https://github-readme-activity-graph.vercel.app/graph?username=Ratnesh-181998&theme=react-dark&hide_border=true&bg_color=0D1117&color=4ECDC4&line=F38181&point=FF6B6B" width="48%" />

---

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=24&duration=3000&pause=1000&color=4ECDC4&center=true&vCenter=true&width=600&lines=Ratnesh+Kumar+Singh;Data+Scientist+%7C+AI%2FML+Engineer;4%2B+Years+Building+Production+AI+Systems" alt="Typing SVG" />

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=18&duration=2000&pause=1000&color=F38181&center=true&vCenter=true&width=600&lines=Built+with+passion+for+the+AI+Community+🚀;Innovating+the+Future+of+AI+%26+ML;MLOps+%7C+LLMOps+%7C+AIOps+%7C+GenAI+%7C+AgenticAI+Excellence" alt="Footer Typing SVG" />


<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=120&section=footer" width="100%">


