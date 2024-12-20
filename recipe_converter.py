from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from models.recipe_doc import RecipeDoc

def process_recipe(recipe_text: str):
    # Initialize model and parser
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    structured_model = model.with_structured_output(RecipeDoc)

    # Create prompt template with chaining syntax
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that converts recipe text into structured data. Please convert the following recipes into a structured format."),
        ("human", "Recipe text: {recipe_text}")
    ])

    # Create chain using the | operator
    chain = prompt | structured_model
    return chain.invoke({"recipe_text": recipe_text})