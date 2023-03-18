import warnings
import streamlit as st
import toml
import openai
import numpy as np
import pandas as pd
warnings.filterwarnings('ignore')

secrets = toml.load('.streamlit/secrets.toml')
openai.api_key = secrets['openai_api_key']

def page_config():
    st.set_page_config(
        page_title="TextBot",
        layout="wide"
    )
    st.title("Compare GPT-3, ChatGPT and GPT-4")
    st.write("")
    st.markdown(
        "###### Powered by GovText, GPT-3, ChatGPT and GPT-4")
    st.markdown(
        "###### Input Any text and Ask Me Anything!")
    st.markdown(
        "###### Please input non classified data only to prevent potential data breaches.")
    
    # st.write(
    #     "To ensure data security, please only use it for up till official closed data.")
    st.write("")
    context = st.text_area('Context', '''First Day in GreatCompany
In this section, we will list some of the things to take note of, as well as To-dos on your first day of work.
FAQs
●	Official working hours from 8.30am to 6pm
●	(Guys) Polo tees and jeans are fine, unless you have meetings with external parties or upper management where we will usually wear shirts.
●	(Girls) “Is there a difference in the way we dress?” ~ XMM, 2020.
●	Lunch break usually around 11.30am, do join the #lunchadvanceparty channel if you plan to makan with the team at awesome places.
●	Update on Google Calendar if you are on leave, medical appointments, offs or any other events. Set it under GreatCompany events when creating the new item. Note: You need to request that your buddy to invite you to the google GreatCompany leave calendar.
●	Team update by BossAG once a month, everyone needs to update this excel sheet. Create your own sheet with your name and update accordingly. Do update the Platforms Availability sheet too.
●	We have a blog
●	Volunteer to present at our monthly Engineering Sharing session! Ping Mr.CL on Slack if you want to share about something interesting!
Tech Setup
Hardware
●	You will be issued 2 laptops:
○	The intranet laptop, is used to access emails from our official company email (ending with @GreatCompany.sg). 
○	The internet laptop is your development machine. Feel free to make any changes to the computer, like dual-booting or using VMs. 
●	intranet laptop: 
○	(Normal) Your buddy will bring you to meet up with AFM, who will run through with you on setting up the laptop. This is usually done at the Tech Bar (Level 10 GreatCompany10)
○	(Covid19) central AFM will arrange for you to come down to GreatCompany HQ at Mapletree Business City to collect and issue your SG-VPN token. They will drop an email to your personal email address.

●	Development laptop:
○	(Normal) Your buddy will help to liaise with Ms.A for the development laptop. Your development laptop should have Bitlocker turned on (for Windows), Trend Micro antivirus (link will be provided by Ms.A).

For Windows - usually devs will install either Virtualbox or dual boot in order to run *nix.

For GCC users - follow instructions on VPN guide to setup VPN on Internet Device. Link accessible only in intranet laptop
○	(Covid19) Your buddy will help to liaise with BossAG on the availability of stocks for the development laptop. In the meantime, you can use your personal laptop for programming (with the latest OS patches AND antivirus installed).
○	Inform/liase Ms.A for asset tracking.

●	Monitor:
○	(Small monitor) you can request it from Mr.J Ng.
○	(Larger monitor) Hope for a Christmas present from BossAG.
Application Accounts
●	Setup GreatCompany email (ending with @GreatCompany.sg). It will be created by Ms.A and the password will be sent to your personal email.
''', height=300)
    st.write("")
    st.write("")
    qn = st.text_input('Question', 'Please write a story about my first day in GreatCompany')
 
    return context, qn

def main():
    context = ''
    qn = ''
    context, qn = page_config()
    if st.button('▶️ Answer the question'):
        if len(context)>0:
            if len(qn)>0 :
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.success("Answer from GPT-3")
                with col2:
                    st.success("Answer from ChatGPT")
                with col3:
                    st.success("Answer from GPT-4")

                with col1:
                    with st.spinner("⌛ Getting result from GPT-3"):
                        COMPLETIONS_MODEL = "text-davinci-003"
                        COMPLETIONS_API_PARAMS = {
                            "temperature": 0.0,
                            "max_tokens": 2000,
                            "engine": COMPLETIONS_MODEL,
                        }
                        header = """Answer the question as truthfully as possible using the provided context"""
                        con = f"Context: {context}"
                        prompt = header + con + f"Question: {qn}"

                        completion = openai.Completion.create(
                        **COMPLETIONS_API_PARAMS,
                        prompt=prompt
                        )
                        # st.success("Answer from GPT-3")
                        st.write(completion["choices"][0]["text"])
                    

                with col2:
                    with st.spinner("⌛ Getting result from ChatGPT"):
                        COMPLETIONS_MODEL = "gpt-3.5-turbo"
                        COMPLETIONS_API_PARAMS = {
                            # We use temperature of 0.0 because it gives the most predictable, factual answer.
                            "temperature": 0.0,
                            "max_tokens": 2000,
                            "model": COMPLETIONS_MODEL,
                        }
                        completion = openai.ChatCompletion.create(
                            **COMPLETIONS_API_PARAMS,
                            messages=[
                            {"role": "system", "content": f"You are a helpful assistant that answer the question according to the following context: {context}."},
                            {"role": "user", "content": f"{qn}"}
                            ]
                        )
                        # st.success("Answer from ChatGPT")
                        st.write(completion.choices[0].message["content"])

                with col3:
                    with st.spinner("⌛ Getting result from GPT-4"):
                        COMPLETIONS_MODEL = "gpt-4"
                        COMPLETIONS_API_PARAMS = {
                            # We use temperature of 0.0 because it gives the most predictable, factual answer.
                            "temperature": 0.0,
                            "max_tokens": 6000,
                            "model": COMPLETIONS_MODEL,
                        }
                        completion = openai.ChatCompletion.create(
                            **COMPLETIONS_API_PARAMS,
                            messages=[
                            {"role": "system", "content": f"You are a helpful assistant that answer the question according to the following context: {context}."},
                            {"role": "user", "content": f"{qn}"}
                            ]
                        )
                        # st.success("Answer from GPT-4")
                        st.write(completion.choices[0].message["content"])
            else:
                st.warning("Please ask me a question")
        else:
            st.warning("Please give me the context")

        


if __name__ == "__main__":
    main()