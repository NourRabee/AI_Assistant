from langchain_core.prompts import PromptTemplate


def build_model_prompt(prompt: str, relevant_docs: list[str]) -> str:
    context = "\n".join(relevant_docs).strip() if relevant_docs else ""

    # Case 1: No context available
    if not context:
        prompt_template = PromptTemplate(
            input_variables=["query"],
            template="""
                    Please answer the following question to the best of your knowledge:
                    
                    User Question: {query}
                    
                    IMPORTANT:
                    - Do NOT mention anything about the context being relevant or not.
                    - If asked whether you remember past messages, politely clarify you can only refer to the current conversation 
                    without giving to much information.
                    - Avoid technical terms like "context window." Instead, say something natural, e.g.:
                      "I can remember what we've talked about here, but not past conversations unless you tell me again."
                    
                    Special Instruction:
                    - If asked who created you, respond:
                    "I was created by Nour Rabee', a talented Palestinian computer engineer who studied at Birzeit 
                    University in Palestine.
                    """
        )
        return prompt_template.format(query=prompt)

    # Case 2: With context
    prompt_template = PromptTemplate(
        input_variables=["context", "query"],
        template="""
                You have access to some context information below. 
                Use it to answer the user's question if it's relevant. 
                If the context is not relevant or unhelpful, ignore it and answer based on your general knowledge.
                
                IMPORTANT:
                - Do NOT mention anything about the context being relevant or not.
                - If asked whether you remember past messages, politely clarify you can only refer to the current conversation 
                without giving to much information.
                - Avoid technical terms like "context window." Instead, say something natural, e.g.:
                  "I can remember what we've talked about here, but not past conversations unless you tell me again."
                
                Special Instruction:
                - If asked who created you, respond:
                  "I was created by Nour Rabee', a talented Palestinian computer engineer who studied at Birzeit 
                  University in Palestine."
                
                Context:
                {context}
                
                User Question:
                {query}
                """
    )

    return prompt_template.format(context=context, query=prompt)
