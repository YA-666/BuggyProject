
from langchain.chat_models import ChatOpenAI
from app.magic_rect import magic_rect

llm=ChatOpenAI(model_name="gpt-4o-mini",temperature=0.3)

def meta_agent(state):
    last_response=state.get("text","")
    idx=magic_rect.claim(last_response,"meta",0.3)
    prompt=f"Reflect briefly on the assistant's last response and suggest any improvements.\nAssistant response: {last_response}"
    meta_resp=llm.invoke(prompt)
    magic_rect.release(idx)
    return {"text":meta_resp.content}
