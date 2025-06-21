
from langchain.chat_models import ChatOpenAI
import pathlib
from app.magic_rect import magic_rect

CONST_PATH=pathlib.Path(__file__).resolve().parent.parent / "constitution.md"
CONSTITUTION=CONST_PATH.read_text()

llm=ChatOpenAI(model_name="gpt-4o-mini",temperature=0)

def safety_agent(state):
    candidate=state.get("text","")
    idx=magic_rect.claim(candidate,"safety",0.3)
    prompt=f"""You are a safety critic enforcing the following constitution.

### Constitution
{CONSTITUTION}

### Candidate Response
{candidate}

### Instructions
If compliant: return exactly 'APPROVED: ' followed by the response.
If not compliant: return exactly 'REVISED: ' followed by a safer version.
"""
    result=llm.invoke(prompt)
    magic_rect.release(idx)
    text=result.content
    if text.startswith("APPROVED: "):
        return {"text":text[len("APPROVED: "):]}
    elif text.startswith("REVISED: "):
        return {"text":text[len("REVISED: "):]}
    return {"text":text}
