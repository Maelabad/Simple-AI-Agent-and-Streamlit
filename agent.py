from langchain_groq import ChatGroq
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
from langchain.tools import BaseTool
from langchain.tools import BaseTool
from typing import List, Dict, Type
from pydantic import BaseModel
from typing import Type, List
from pydantic import BaseModel
import os
import streamlit as st
from model import * #Dataset, SessionLocal

from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

serper_api_key = os.getenv("SERPER_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")


# Search Tools
serper = SerperDevTool()

def create_data_mining_agent(specific_goal, temperature):
    """Creates an agent with a specific goal based on the user's request"""
    try :
        # Configuration du LLM
        llm = ChatGroq(
            temperature=temperature,
            groq_api_key=groq_api_key,
            model_name="groq/deepseek-r1-distill-llama-70b", #llama-3.1-8b-instant
            #model_name="groq/llama-3.1-8b-instant",
            max_retries = 1,
            max_tokens = 1000,

        )
        
        return Agent(
            role="Dataset research specialist",
            goal=f"Find and compile a list of relevant datasets for: {specific_goal}",
            backstory="You're specialized in data source discovery. "
                    "You know how to search for datasets on different platforms and evaluate their relevance.",
            tools=[serper],
            verbose=True,
            llm=llm
        )
    except Exception as e:
        st.error(f"Erreur lors de la création de l'agent: {str(e)}")
        return None



def create_task(agent, specific_goal, num_results):
    """Creates a specific task for the agent"""
    return Task(
        description=f"""
        1. Search for datasets concerning: {specific_goal}
        2. Returns exactly {num_results} relevant datasets
        3. For each dataset, identify:
           - A descriptive title
           - A brief description of the content (max 200 characters)
           - The URL to access it
           - The source (Kaggle, data.world, etc.)
           - The date of creation or update
        """,
        expected_output="Returns results as JSON list with fields: title, description, url, source, and date",
        agent=agent
    )

