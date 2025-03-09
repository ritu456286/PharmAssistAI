import os
from dotenv import load_dotenv
load_dotenv()
import getpass
import ast

from typing_extensions import TypedDict

from sqlalchemy import inspect

from src.configs.db_con import engine, db

from pydantic import BaseModel, Field

from langchain_groq import ChatGroq
from langchain import hub
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END

llm_api_key = os.getenv("GROQ_API_KEY")
if(llm_api_key is None):
    os.environ["GROQ_API_KEY"] = getpass.getpass("Enter API key for Groq: ")

query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")


class AgentState(TypedDict):
    question: str
    sql_query: str
    query_result: str
    query_rows: list
    # current_user: str
    attempts: int
    relevance: str
    sql_error: bool

class CheckRelevance(BaseModel):
    relevance: str = Field(
        description="Indicates whether the question is related to the database schema. 'relevant' or 'not_relevant'."
    )

class ConvertToSQL(BaseModel):
    sql_query: str = Field(
        description="The SQL query corresponding to the user's natural language question."
    )

class RewrittenQuestion(BaseModel):
    question: str = Field(description="The rewritten question.")



#TOOLS
def get_database_schema(engine):
    inspector = inspect(engine)
    schema = ""
    for table_name in inspector.get_table_names():
        schema += f"Table: {table_name}\n"
        for column in inspector.get_columns(table_name):
            col_name = column["name"]
            col_type = str(column["type"])
            if column.get("primary_key"):
                col_type += ", Primary Key"
            if column.get("foreign_keys"):
                fk = list(column["foreign_keys"])[0]
                col_type += f", Foreign Key to {fk.column.table.name}.{fk.column.name}"
            schema += f"- {col_name}: {col_type}\n"
        schema += "\n"
    print("Retrieved database schema.", schema)
    return schema

async def check_relevance(state: AgentState):
    question = state["question"]
    schema = get_database_schema(engine)
    print(f"Checking relevance of the question: {question}")
    system = """You are an assistant that determines whether a given question is related to the following database schema.

Schema:
{schema}

Respond with only "relevant" or "not_relevant".
""".format(schema=schema)
    human = f"Question: {question}"
    check_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", human),
        ]
    )
    llm = ChatGroq(temperature=0, model="mixtral-8x7b-32768")
    relevance_checker = check_prompt | llm | StrOutputParser() # Simple chain: prompt -> LLM -> string parser
    print("*****BEFORE INVOKE********")
    relevance_text = await relevance_checker.ainvoke({"schema":schema, "question": question}) # Get plain text output
    print("*****AFTER INVOKE********")

    if "relevant" in relevance_text.lower():
        state["relevance"] = "relevant"
    else:
        state["relevance"] = "not_relevant"

    print(f"Relevance determined: {state['relevance']}")
    return state


# async def check_relevance(state: AgentState):
    
#     question = state["question"]
#     schema = get_database_schema(engine)
#     print(f"Checking relevance of the question: {question}")
#     system = """You are an assistant that determines whether a given question is related to the following database schema.

# Schema:
# {schema}

# Respond with only "relevant" or "not_relevant".
# """.format(schema=schema)
#     human = f"Question: {question}"
#     check_prompt = ChatPromptTemplate.from_messages(
#         [
#             ("system", system),
#             ("human", human),
#         ]
#     )
#     llm = ChatGroq(temperature=0, model="mixtral-8x7b-32768")
#     structured_llm = llm.with_structured_output(CheckRelevance)
#     relevance_checker = check_prompt | structured_llm
#     print("*****BEFORE INVOKE********")
#     # print("*****HELLO********")
#     #"schema":schema, "question": question
#     relevance = await relevance_checker.ainvoke({})
#     print("*****AFTER INVOKE********")
#     state["relevance"] = relevance.relevance
#     print(f"Relevance determined: {state['relevance']}")
#     return state


async def convert_nl_to_sql(state: AgentState):
    """Generate SQL query from natural language question."""
    question = state["question"]
    schema = get_database_schema(engine)
    print(f"Converting question to SQL: {question}")
    prompt = query_prompt_template.invoke(
        {
            "dialect": db.dialect,
            "top_k": 10,
            "table_info": db.get_table_info(),
            "input": state["question"],
        }
    )
    print(f"Type of prompt: {type(prompt)}") # Debug print for prompt type

    llm = ChatGroq(temperature=0, model="mixtral-8x7b-32768")
    
    structured_llm = llm.with_structured_output(ConvertToSQL)
    print(f"Type of structured_llm: {type(structured_llm)}") # Debug print for structured_llm type

    print("*****BEFORE INVOKE structured_llm********")
    # result = await structured_llm.invoke(prompt)
    result = await structured_llm.ainvoke(prompt)

    print("*****AFTER INVOKE structured_llm********") 
    state["sql_query"] = result.sql_query
    print(f"Generated SQL query: {state['sql_query']}")
    return state
    

async def execute_query(state: AgentState):
    """Execute SQL query."""
    
    sql_query = state["sql_query"].strip()
    print(f"Executing SQL query: {sql_query}")
    execute_query_tool = QuerySQLDatabaseTool(db=db)
    try:
        result = await execute_query_tool.ainvoke(sql_query)
        if sql_query.lower().startswith("select"):
            if len(result) != 0:
                state["query_rows"] = ast.literal_eval(result)
                formatted_result = result
            else:
                state["query_rows"] = []
                formatted_result = "No results found."
            state["query_result"] = formatted_result
            state["sql_error"] = False
            print("SQL SELECT query executed successfully.")
        else:
            state["query_result"] = "The action has been successfully completed."
            state["sql_error"] = False
            print("SQL command executed successfully.")
    except Exception as e:
        state["query_result"] = f"Error executing SQL query: {str(e)}"
        state["sql_error"] = True
        print(f"Error executing SQL query: {str(e)}")

    return state


async def generate_human_readable_answer(state: AgentState):
    """Answer question using retrieved information as context."""
    question = state["question"]
    sql_query = state["sql_query"]
    result = state["query_result"]
    query_rows = state.get("query_rows", [])
    sql_error = state.get("sql_error", False)
    
    current_user = "Ritu"
    
    print("Generating a human-readable answer.")
    
    system = """You are an assistant that converts SQL query results into clear, natural language responses without including any identifiers like medicine IDs. Start the response with a friendly greeting that includes the user's name.
    """
    
    if sql_error:
        # Directly relay the error message
        generate_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system),
                (
                    "human",
                    f"""SQL Query:
{sql_query}

Result:
{result}

Formulate a clear and understandable error message in a single sentence, starting with 'Hello {current_user},' informing them about the issue."""
                ),
            ]
        )
    elif sql_query.lower().startswith("select"):
        if not query_rows:
            # Handle cases with no medicines found
            generate_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system),
                    (
                        "human",
                        f"""SQL Query:
{sql_query}

Result:
{result}

Formulate a clear and understandable answer to the original question in a single sentence, starting with 'Hello {current_user},' and mention that there are no medicines found."""
                    ),
                ]
            )
        else:
            # Handle cases with medicines found
            generate_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system),
                    (
                        "human",
                        f"""SQL Query:
{sql_query}

Result:
{result}
Given the following user question, corresponding SQL query, 
and SQL result, answer the user question starting with 'Hello {current_user},'.\n\n
Question: {question}\n'
SQL Query: {sql_query}\n'
SQL Result: {result}\n'
"""
                    ),
                ]
            )
    else:
        # Handle non-select queries
        generate_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system),
                (
                    "human",
                    f"""SQL Query:
{sql_query}

Result:
{result}

Formulate a clear and understandable confirmation message in a single sentence, starting with 'Hello {current_user},' confirming that your request has been successfully processed."""
                ),
            ]
        )

    llm = ChatGroq(temperature=0, model="mixtral-8x7b-32768")
    human_response = generate_prompt | llm | StrOutputParser()
    answer = await human_response.ainvoke({})
    state["query_result"] = answer
    print("Generated human-readable answer.")
    return state


async def regenerate_query(state: AgentState):
    question = state["question"]
    print("Regenerating the SQL query by rewriting the question.")
    system = """You are an assistant that reformulates an original question to enable more precise SQL queries. Ensure that all necessary details, such as table joins, are preserved to retrieve complete and accurate data.
    """
    rewrite_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            (
                "human",
                f"Original Question: {question}\nReformulate the question to enable more precise SQL queries, ensuring all necessary details are preserved.",
            ),
        ]
    )
    llm = ChatGroq(temperature=0, model="mixtral-8x7b-32768")
    structured_llm = llm.with_structured_output(RewrittenQuestion)
    rewriter = rewrite_prompt | structured_llm
    rewritten = await rewriter.ainvoke({})
    state["question"] = rewritten.question
    state["attempts"] += 1
    print(f"Rewritten question: {state['question']}")
    return state

async def generate_funny_response(state: AgentState):
    print("Generating a funny response for an unrelated question.")
    system = """You are a charming and funny assistant who responds in a playful manner.
    """
    human_message = "Sorry, I can not help with that, but doesn't asking questions make you sick? You can always find some home remedies from my friend, Sam."
    funny_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", human_message),
        ]
    )
    llm = ChatGroq(temperature=0.7,model="mixtral-8x7b-32768")
    funny_response = funny_prompt | llm | StrOutputParser()
    message = await funny_response.ainvoke({})
    state["query_result"] = message
    print("Generated funny response.")
    return state

def end_max_iterations(state: AgentState):
    state["query_result"] = "Please try again."
    print("Maximum attempts reached. Ending the workflow.")
    return state

def relevance_router(state: AgentState):
    if state["relevance"].lower() == "relevant":
        return "convert_to_sql"
    else:
        return "generate_funny_response"

def check_attempts_router(state: AgentState):
    if state["attempts"] < 3:
        return "convert_to_sql"
    else:
        return "end_max_iterations"

def execute_sql_router(state: AgentState):
    if not state.get("sql_error", False):
        return "generate_human_readable_answer"
    else:
        return "regenerate_query"
    
#CREATING THE WORKFLOW GRAPH

def initialize_agent():

    workflow = StateGraph(AgentState)

    # workflow.add_node("get_current_user", get_current_user)
    workflow.add_node("check_relevance", check_relevance)
    workflow.add_node("convert_to_sql", convert_nl_to_sql)
    workflow.add_node("execute_sql", execute_query)
    workflow.add_node("generate_human_readable_answer", generate_human_readable_answer)
    workflow.add_node("regenerate_query", regenerate_query)
    workflow.add_node("generate_funny_response", generate_funny_response)
    workflow.add_node("end_max_iterations", end_max_iterations)

    # workflow.add_edge("get_current_user", "check_relevance")

    workflow.add_conditional_edges(
        "check_relevance",
        relevance_router,
        {
            "convert_to_sql": "convert_to_sql",
            "generate_funny_response": "generate_funny_response",
        },
    )

    workflow.add_edge("convert_to_sql", "execute_sql")

    workflow.add_conditional_edges(
        "execute_sql",
        execute_sql_router,
        {
            "generate_human_readable_answer": "generate_human_readable_answer",
            "regenerate_query": "regenerate_query",
        },
    )

    workflow.add_conditional_edges(
        "regenerate_query",
        check_attempts_router,
        {
            "convert_to_sql": "convert_to_sql",
            "max_iterations": "end_max_iterations",
        },
    )

    workflow.add_edge("generate_human_readable_answer", END)
    workflow.add_edge("generate_funny_response", END)
    workflow.add_edge("end_max_iterations", END)

    workflow.set_entry_point("check_relevance")

    print("[STARTUP] Compiling Agent Workflow...")
    
    app = workflow.compile()
    
    print("[STARTUP] Agent Workflow compiled successfully.")
    
    return app


agent = initialize_agent()