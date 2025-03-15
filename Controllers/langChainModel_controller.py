from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
import logging
from Utils.CommonExceptions import CommonException
from dotenv import load_dotenv
load_dotenv()
import os


class LlmModelChatBotController():
    def ConfigureAIModel(prompt_template,model):
        try:
            if model == 'Gemini':
                response = LlmModelChatBotController.GeminiModel(prompt_template)
            else:
                response = LlmModelChatBotController.OpenAiModel(prompt_template)

            return response

        except Exception as e:
            logging.error(f"Error in ConfigureModel: {str(e)}")
            return CommonException.handleException(e)

    def GeminiModel(message):
        try:
            
            gemini_llm = ChatGoogleGenerativeAI(
                model='gemini-2.0-flash',
                google_api_key=os.getenv('GEMINI_AI_API_KEY'),
                temperature=0.7
            )
            gemini_response = gemini_llm.invoke(message)
            return gemini_response.content
        except Exception as e:
            logging.error(f"Error in GeminiModel: {str(e)}")
            return {"Error":str(e)}

    def OpenAiModel(message):
        try:
            openai_llm = ChatOpenAI(
                model='gpt-4o-mini',
                api_key=os.getenv('OPEN_AI_API_KEY'),
                temperature=0.7
            )
            openai_response = openai_llm.invoke(message)

            return openai_response.content

        except Exception as e:
            logging.error(f"Error in OpenAiModel: {str(e)}")
            return {"Error": str(e)}

   