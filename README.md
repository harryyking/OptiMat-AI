# OptiMat-AI
Opti-Mat is a material selection AI assistant that recommends the most suitable material for your use case. It is designed to assist engineers, designers, and material scientists in selecting the optimal material for their projects. By leveraging AI algorithms, Opti-Mat analyzes various parameters and requirements to provide personalized recommendations for materials that best meet the specific needs of each project. OptiMat-AI can be integrated into CAD software systems or can be used as a standalone application to help get a user from an idea to manufacturing in seconds. 

## Features

- **AI-Powered Recommendations:** Opti-Mat uses advanced AI algorithms to analyze project requirements and recommend the most suitable materials.
- **Customizable Parameters:** Users can input specific project parameters such as functionality, cost constraints, and performance requirements to tailor the recommendations.
- **User-Friendly Interface:** The user interface is intuitive and easy to navigate, making it accessible to both experts and novices in materials science and engineering.


## Requirements

Note: this project was built on windows and the instructions are for windows and cmd terminal.
this project assumes:
1. python is installed (3.12.2)
2. virtualenv is installed

## Getting Started
1. Clone the project in your preferred directory
   
   ```
   git clone https://github.com/harryyking/OptiMat-AI.git
   ```

2. Create a virtual environment and activate
   ```
   python -m venv ./venv
   .\venv\Scripts\activate
   ```

3. Create a .env file in your root directory and add your api key
   ```
   # .env file
   
   OPENAI_API_KEY=[your-api-key] # replace with your actual api key
   ```
   
4. Navigate to the project folder

   ```
   cd Opti-mat
   ```

5. Install the libraries in requirement.txt file
   ```
   pip install -r requirements.txt
   ```
   
6. Run the following code to start the project
   
   ```
   flask --app optiMat run --debug
   ```

A video presentation on OptiMat AI 

https://github.com/harryyking/OptiMat-AI/assets/87400506/e6492637-38d3-4557-a31f-6cc63f74fb4f


