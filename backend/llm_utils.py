from dotenv import load_dotenv
import os
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq

load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.1-8b-instant"
    temperature=0.3,
    max_tokens=2048,
    groq_api_key=groq_key
)

PROMPT_TEMPLATE = """
You are a helpful medical advisor.

Symptoms: {symptoms}
Test Results: {test_results}
Prescription: {prescription}

Give:
1. Disease explanation (layman)
2. Prescription correctness
3. Allopathic treatment with dosage
4. Ayurvedic remedies
5. Precautions
"""

prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
chain = prompt | llm

last_analysis = ""  # basic global context cache

def analyze_case(symptoms, test_results, prescription):
    global last_analysis
    inputs = {
        "symptoms": symptoms,
        "test_results": test_results,
        "prescription": prescription
    }
    result = chain.invoke(inputs)
    last_analysis = result.content
    return result.content

def chat_followup(user_message):
    global last_analysis
    followup_prompt = f"""
The user previously received this analysis:

{last_analysis}

Now they ask: "{user_message}"

Please respond accordingly in a simple and friendly way.
"""
    return llm.invoke(followup_prompt).content