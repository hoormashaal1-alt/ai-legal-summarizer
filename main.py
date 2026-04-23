import os
from dotenv import load_dotenv
from IPython.display import Markdown
import requests
from openai import OpenAI
from scraper import fetch_website_contents
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')
# Check the key
if not api_key:
    print("No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
elif not api_key.startswith("sk-proj-"):
    print("An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook")
elif api_key.strip() != api_key:
    print("An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook")
else:
    print("API key found and looks good so far!")


requests.get("http://localhost:11434").content
system_prompt = """You are a Legal Analyst. Your task is to summarize legal contracts that is
 provided by the user. I want you to focus on extracting key points,
 financial terms, termination clauses, and potential risks. Present the summary
  in concise, numbered bullet points. Conclude with recommendations for related 
  legal documents the user should study for broader context. Maintain a professional yet friendly tone. Do not wrap the markdown in a code
   block - respond just with the markdown"""
user_prompt = """
   I will provide you with a url or the text of legal agreement. And ou, as a legal analyst, pleasse give
   me the following:
   1-Core Purpose: Do summarize the primary objective of thhis contract in one sentence.
   2-Key responsibilities:List the most important and critical responsibilities
   and what is required from me.
   3-Critical Clauses:Recommend specific types of legal document or templates
   that would complement this agreement for better legel protection.
   For formar: pleaase use very concise, numbered bullet points. Keep the tone formal.
"""
message=[{"role":"system","content":system_prompt},{"role":"user","content":system_prompt}]
def summarize(url):
    The_feched_content=fetch_website_contents(url)
    message=[{"role":"system","content":system_prompt},{"role":"user","content":user_prompt+ The_feched_content}]
    ollama=OpenAI(base_url="http://localhost:11434/v1",api_key="ollama")
    response= ollama.chat.completions.create(model="deepseek-r1:1.5b",messages=message)
    return response.choices[0].message.content


def summarize2(url):
   summary=summarize(url)
   display(Markdown(summary))
print(summarize2("https://www.lawinsider.com/contracts/1Yr9baZLxHq"))