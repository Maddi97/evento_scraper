import os
from dotenv import load_dotenv
from langchain.output_parsers import PydanticOutputParser
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.messages import SystemMessage, HumanMessage

from app.models.event_models import EventSchema

load_dotenv()

# Use GPT-4o-mini
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
pydantic_parser = PydanticOutputParser(pydantic_object=EventSchema)
format_instructions = pydantic_parser.get_format_instructions()


def extract_event_data(input_text: str) -> EventSchema:
    EVENT_EXTRACT_PROMPT = """
                                Dein Ziel ist es, aus dem gegebenen Text Informationen über ein Event zu extrahieren.
                            
                                {format_instructions}

                                Text, der das Event enthält
                                {input_text}
                            """

    prompt = ChatPromptTemplate.from_template(
        template=EVENT_EXTRACT_PROMPT,
        partial_variables={"format_instructions": format_instructions},
    )

    full_chain = (
        {"input_text": lambda x: x["input_text"]} | prompt | model | pydantic_parser
    )

    result = full_chain.invoke({"input_text": input_text})

    return result
