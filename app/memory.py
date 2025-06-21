
from __future__ import annotations
import time, math
from typing import List
import tiktoken, openai
from memgpt.agent import MemGPTAgent
from .config import IMPORTANCE_THRESHOLD, MAX_TOKENS, RECENCY_TAU

_ENCODER = tiktoken.encoding_for_model("gpt-4o-mini")

def _num_tokens(text:str)->int:
    return len(_ENCODER.encode(text))

def _summarize(text:str)->str:
    if _num_tokens(text)<=MAX_TOKENS:
        return text
    prompt=f"Summarise under {MAX_TOKENS} tokens while preserving key facts:\n{text}"
    resp=openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.2)
    return resp.choices[0].message.content.strip()

def _importance_score(text:str)->float:
    lowered=text.lower()
    score=0.0
    if any(kw in lowered for kw in ("remember","important","don't forget","note that")):
        score+=0.5
    score+=min(0.5,_num_tokens(text)/1000)
    return min(score,1.0)

class MemoryController:
    def __init__(self):
        self.agent=MemGPTAgent(archive_backend="chroma",collection="soul-memory",embedding_model="text-embedding-3-small")
        self._embedmodel="text-embedding-3-small"

    def _embed(self,text:str)->List[float]:
        resp=openai.Embedding.create(model=self._embedmodel,input=text)
        return resp.data[0].embedding

    def add(self,text:str)->bool:
        importance=_importance_score(text)
        if importance<IMPORTANCE_THRESHOLD:
            return False
        processed=_summarize(text)
        emb=self._embed(processed)
        self.agent.archive(processed,metadata={"importance":importance,"timestamp":time.time()},embedding=emb)
        return True

    def query(self,prompt:str,top_k:int=5)->List[str]:
        q_emb=self._embed(prompt)
        res=self.agent.similarity_search_with_score(q_emb,k=20)
        now=time.time()
        scored=[]
        for doc,score in res:
            meta=doc.metadata or {}
            importance=float(meta.get("importance",0.3))
            ts=float(meta.get("timestamp",now))
            recency=math.exp(-(now-ts)/RECENCY_TAU)
            hybrid=score*importance*recency
            scored.append((hybrid,doc.page_content))
        scored.sort(key=lambda x:x[0],reverse=True)
        return [t[1] for t in scored[:top_k]]

memory_controller=MemoryController()

def write_memory(text:str):
    return memory_controller.add(text)

def read_memory(query:str,top_k:int=5)->List[str]:
    return memory_controller.query(query,top_k)
