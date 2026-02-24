 **AI SENSOR ANALYZER**
 AI Sensor Analyzer is a web-based AI tool that analyzes industrial sensor logs to automatically detect abnormal readings and generate human-readable diagnostic explanations.

 **Live Demo:**
https://ai-sensor-analyzer-lygrectnegbdkvzs4yypea.streamlit.app/

 **Features**
* Upload CSV sensor logs
* Automatic anomaly detection using Isolation Forest
* AI-generated engineering explanation of abnormal readings
* Suggested corrective actions
* Interactive visualization dashboard
* Downloadable diagnostics report



**System Architecture**
1. User uploads CSV sensor data
2. Pandas processes and cleans dataset
3. Isolation Forest detects anomalies
4. Statistical summary sent to LLM API
5. AI generates diagnostic explanation
6. Dashboard displays results and downloadable report



**Tech Stack**
* Python
* Streamlit
* Pandas
* Scikit-learn
* OpenRouter LLM API
* Requests

 **How to Run Locally**
1. Clone the repo:
git clone https://github.com/YOURUSERNAME/AI-sensor-analyzer.git
cd AI-sensor-analyzer

2. Install dependencies:
pip install -r requirements.txt

3. Create .env file:
OPENROUTER\_API\_KEY=your\_key\_here

4. Run the app:
streamlit run app.py

 **Use Cases**
* Industrial monitoring systems
* IoT sensor networks
* Aerospace testing environments
* Smart greenhouse systems
* Predictive maintenance workflows


###  **Author**
Bhavana Priya P K

