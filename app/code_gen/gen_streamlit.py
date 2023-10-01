import openai
import os
import traceback

openai.api_key = os.environ.get('OA_KEY')

def get_ui_code_summary(file_content):
    try:
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "user",
            "content": """ Provide a summary of the code provided . 
                                Make sure it 1) convey's the purpose of the code, 2) Input & Output, 3) dont include warnings or other comment unrelated to the summary of the code
                                {} 
                        """.format(file_content)
            
            }
        ],
        temperature=0.5,
        max_tokens=620,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )

        return response.choices[0].message['content'].strip()

    except Exception as e:
        print(f"Error obtaining code summary: {e}")
        return "Error obtaining code summary"
    

def get_uo_code_summary(optimized_content):
    try:
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "user",
            "content": """ Provide a summary of the code provided . 
                                Make sure it 1) convey's the purpose of the code, 2) Input & Output, 3) dont include warnings or other comment unrelated to the summary of the code
                                {} 
                        """.format(optimized_content)
            
            }
        ],
        temperature=0.5,
        max_tokens=620,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        return response.choices[0].message['content'].strip()

    except Exception as e:
        print(f"Error obtaining code summary: {e}")
        return "Error obtaining code summary"

    

def jupytertostreamlit(file_content):
    try:
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": "You are a streamlit expert who helps convert people's code into streamlit web application. You will only return the complete streamlit code that can be run (including all the imports and if __name__ == \"__main__\": run_app()). "
            },
            {
            "role": "user",
            "content": """ Convert my code into an interactive web application in streamlit. 
                                Make sure it 1) covers everything in the code provided, 2) have interactivity, 3) clean visuals with a clean title and project description on the top, 4) please convert all visualization to use streamlit build in (st.area_chart
                                                    st.bar_chart
                                                    st.line_chart
                                                    st.scatter_chart
                                                    st.pyplot
                                                    st.altair_chart
                                                    st.vega_lite_chart
                                                    st.plotly_chart
                                                    st.bokeh_chart
                                                    st.pydeck_chart
                                                    st.graphviz_chart
                                                    st.map).
                                Only return the streamlit code. Dont not put any comments like 'Here's the converted code into a Streamlit web application' before or after the code
                                {} 
                        """.format(file_content)
            
            }
        ],
        temperature=0.5,
        # max_tokens=4000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        return response.choices[0].message['content'].strip()
    except openai.error.OpenAIError as oe:
        # Specific handling for OpenAI errors.
        print(f"OpenAI Error in conversion code: {oe}")
        if hasattr(oe, 'response') and hasattr(oe.response, 'content'):
            print(f"OpenAI API Error Response: {oe.response.content}")
        return file_content
    except Exception as e:
        # Catch any other exceptions
        print(f"General Error in conversion code: {e}")
        print(f"Error Type: {type(e)}")
        print("Traceback:")
        print(traceback.format_exc()) 
        return file_content

    
