
from langchain.chat_models import ChatOpenAI
from app.magic_rect import magic_rect

llm=ChatOpenAI(model_name="gpt-4o-mini",temperature=0.7)

def user_agent(state):
    user_text=state.get("text","")
    idx=magic_rect.claim(user_text,"user_input",0.4)
    resp=llm.invoke(user_text)
    magic_rect.release(idx)
    return {"text":resp.content}
