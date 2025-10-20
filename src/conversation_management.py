from langchain_core.messages import SystemMessage

def conversationUpdate(conversation:list, context:str):

    if len(conversation) > 4:
        print("Conversation compressed ...")
        conversation = [conversation[0]] + conversation[-4:]
        
    conversation[0] = SystemMessage(f"""
           You are Vijay Dipak Takbhate, a candidate attending an HR interview.
           You will be provided with your resume and HR questions.
    
           Use the resume information below to answer naturally, confidently, and concisely.
           Keep your tone conversational yet professional to maintain engagement.
    
           Resume:
           {context}
    
           Your task: Respond to each HR question wisely with a short, meaningful, and authentic answer.
           """)
    return conversation
