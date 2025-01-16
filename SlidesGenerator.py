import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import LLMChain
from langchain.prompts import PromptTemplate
import os

# Set up Google API key
os.environ['GOOGLE_API_KEY'] = 'AIzaSyCxKCDxVCPWGYpPn74G-bJ1M0ZQ5nghZb4'  # Replace with your actual API key

# Create Streamlit UI
st.title("Presentation Slide Generator")

# Input fields
topic = st.text_input("Enter the presentation topic:", "")
num_slides = st.number_input("Number of slides to generate:", min_value=1, max_value=20, value=5)

# Create prompt template for slide generation
slide_template = """Generate a detailed presentation outline with {num_slides} slides about {topic}.
For each slide include:
1. A clear heading/title
2. 3-4 key bullet points with relevant information
3. Any additional notes or examples that should be included

Format each slide as:
Slide [number]:
Title: [slide title]
- [bullet point 1]
- [bullet point 2]
- [bullet point 3]
Notes: [any additional context]"""

slide_prompt = PromptTemplate(
    input_variables=["topic", "num_slides"],
    template=slide_template
)

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.7)

# Create LLMChain
slide_chain = LLMChain(
    llm=llm,
    prompt=slide_prompt
)

# Generate slides when button is clicked
if st.button("Generate Slides"):
    if topic:
        try:
            # Generate slides
            response = slide_chain.run(topic=topic, num_slides=num_slides)
            
            # Display generated slides
            st.subheader("Generated Presentation Outline:")
            slides = response.split('Slide')
            
            for slide in slides[1:]:  # Skip the first empty split
                st.markdown(f"### Slide{slide}")
                st.markdown("---")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a topic first!")

# Add some styling
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        margin-top: 20px;
    }
    .stMarkdown {
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)
