import re
from math import ceil
import time
import streamlit as st
from crewai import Agent, Task, Crew
import json
from litellm.exceptions import RateLimitError
from agent import create_data_mining_agent, create_task
from model import init_db, insert

import logging
logging.basicConfig(level=logging.DEBUG)

DB_URL = "sqlite:///datasets.db"


def get_retry_time(error: RateLimitError):
    
    retry_time_string = error.message.split("Please try again in")[-1].split('. Visit')[0]

    minute = re.search(  r'\d+m', retry_time_string )
    
    retry_time = 1
     
    if minute and minute.group()[:-1]: # Checks if the match exists and is not empty
        retry_time +=  int(minute.group()[:-1]) * 60
    
    sec = re.search(  r'\d+\.\d+s', retry_time_string )
    
    if sec and sec.group()[:-1]:  # Checks if the match exists and is not empty
        retry_time +=  ceil(float(sec.group()[:-1])) + 1

    return retry_time



# Interface Streamlit
def main():
    st.set_page_config(layout="centered", page_title="Data Scout")
    
    st.title("Data Scout - Find Data Everywhere")
    

    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        query = st.text_input("Describe the dataset you're looking for: ")
    
    with col2:
        num_results = st.number_input("Number of results : ", min_value=1, max_value=20, value=5)
    
    with col3:
        temperature = st.slider("Temperature : ", min_value=0.0, max_value=1.0, value=0.0, step=0.1)
        
    # Visualisation de la température avec une couleur
    temp_color = f"rgb({int(255 * temperature)}, {int(255 * (1-temperature))}, 0)"
    st.markdown(f"""
        <div style="background-color: {temp_color}; padding: 5px; border-radius: 5px;">
            <span style="color: white; font-weight: bold;">Température: {temperature}</span>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Search"):
        if query:
            engine = init_db(DB_URL)
                   
            with st.spinner("Search in progress..."):
                
                agent = create_data_mining_agent(query, temperature)
                task = create_task(agent, query, num_results)
                
                crew = Crew(
                    agents=[agent],
                    tasks=[task],
                    verbose=True
                )
                
                try :
                
                    # Exécuter la recherche
                    result = crew.kickoff()
                    if not result:
                        st.error("Aucun résultat obtenu")
                        st.stop()
                         
                
                    try:
                        # Parsing du résultat
                        import re
                        json_match = re.search(r"\[\s*\{.*\}\s*\]", result.raw, re.DOTALL)
                        
                        if json_match:
                            json_text = json_match.group(0)  # Extraction du JSON
                            datasets = json.loads(json_text)  # Parsing JSON
                        
                        # Afficher les résultats
                        st.subheader(f"{len(datasets)} jeux de données trouvés")
                        
                        cols = st.columns(1)
                        for i, dataset in enumerate(datasets):
                            with cols[i % 1]:
                                with st.container(border=True):
                                    st.markdown(f"### {dataset['title']}")
                                    st.write(dataset['description'])
                                    st.markdown(f"[Accéder au jeu de données]({dataset['url']})")
                                    st.caption(f"Source: {dataset['source']}")
                                    st.write(f"Date: {dataset['date']}")
                        insert(datasets, engine)
                    
                    except json.JSONDecodeError:
                        st.error("Les résultats ne sont pas au format JSON attendu")
                        st.text(result.raw)  # Afficher le résultat brut
                       
                except  RateLimitError as error:    
                    retry_time = get_retry_time(error)                                    
                    #print(f"*****************************************retry_time : {retry_time}********************")
                    time.sleep(retry_time)
                except json.JSONDecodeError:
                    st.error("The results could not be formatted correctly. Here is the raw result : ")
                    st.text(result)
    
if __name__ == "__main__":
    main()