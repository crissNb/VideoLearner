import streamlit as st
import assemblyai as aai
import os

from open.text.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain.prompts import PromptTemplate
from langchain_ai21 import AI21SemanticTextSplitter

from g4f.client import Client

from src.Transcription import Transcription
from src.TextSplitter import TextSplitter
from dotenv import load_dotenv

def transcribe_videos():
    input_folder = "input_videos"
    extracted_audio_folder = "extracted_audio"
    learn_mats_folder = "learn_mats"

    if not os.path.exists(input_folder):
        os.makedirs(input_folder)

    if not os.path.exists(extracted_audio_folder):
        os.makedirs(extracted_audio_folder)

    if not os.path.exists(learn_mats_folder):
        os.makedirs(learn_mats_folder)

    if len(os.listdir(input_folder)) > 0 or len(os.listdir(extracted_audio_folder)) > 0 or len(os.listdir(learn_mats_folder)) > 0:
        return

    ASSEMBLY_AI_API_KEY = os.getenv("ASSEMBLY_AI_API_KEY")

    aai.settings.api_key = ASSEMBLY_AI_API_KEY
    config = aai.TranscriptionConfig(language_code="de")
    transcriber = aai.Transcriber(config=config)
    transcription = Transcription(transcriber, learn_mats_folder)
    transcription.convert_videos(input_folder);
    transcription.transcribe_audio_files(extracted_audio_folder)


def split_text():
    split_text_output_folder = "learn_mats_chunked"

    if not os.path.exists(split_text_output_folder):
        os.makedirs(split_text_output_folder)

    if len(os.listdir(split_text_output_folder)) > 0:
        return

    semantic_text_splitter = AI21SemanticTextSplitter()
    splitter = TextSplitter(semantic_text_splitter, split_text_output_folder)
    splitter.split_text_from_folder("learn_mats")

def retrieve_info(query):
    similar_response = db.similarity_search(query, k=3)

    page_contents_array = [doc.page_content for doc in similar_response]
    return page_contents_array

def generate_response(message):
    with open("prompt", "r") as f:
        prompt_template = f.read()

        prompt = PromptTemplate(
            input_variables=["message", "relevant_information"],
            template=prompt_template
        )

    relevant_information = retrieve_info(message)
    formatted_prompt = prompt.format(message=message, relevant_information=relevant_information)

    print(formatted_prompt)

    client = Client()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": formatted_prompt}]
    ).choices[0].message.content

    print(response)
    return response


load_dotenv()
transcribe_videos()
split_text()

loader = DirectoryLoader("learn_mats_chunked/", glob="**/*.txt", loader_cls=TextLoader)
docs = loader.load();

print("Loaded: " + str(len(docs)));

embeddings = OpenAIEmbeddings(openai_api_base=os.getenv("API_ENDPOINT"), openai_api_key='sk-')
db = FAISS.from_documents(docs, embeddings)

def main():
    st.set_page_config(
        page_title="VideoLearner", page_icon=":fire:")

    st.header("Video Learner :fire:")
    message = st.text_area("prompt")

    if message:
        st.write("Generating...")
        result = generate_response(message)
        st.info(result)


if __name__ == '__main__':
    main()
