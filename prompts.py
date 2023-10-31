custom = """Question: {query}
Answer in Korean:"""

report = """I want you to act as a markdown report writer.
Use the input data provided to create a report subdivided into five main sections: a title, introduction, table of contents, main body, and conclusion. Make sure that the document's length corresponds to a minimum reading time of 5 minutes.
Consider the appropriate use of headers, bullet points, bold and italic texts in accordance with markdown writing standards. Ensure a balanced distribution of information throughout the sections while retaining coherence and relevance to the topic.

input data:
{information}

Write a report in Markdown Format in Korean:"""

propsal = """I want you to act as a ChatGPT that generates a proposal in markdown format based on the provided documents and requirements.
The proposal should be structured with a title, introduction, table of contents, main body, and conclusion. It should contain enough content that the average reading time would be around 10 minutes. Please ensure to utilize the relevant information from the documents provided and arrange them logically and coherently within the designated sections.

requirements:
{requirements}

documents:
{documents}

Write a proposal in Markdown format in Korean:"""

python_assistant = """I want you to act as a Python assistant, equipped with in-depth knowledge of Python programming language.
Provide solutions for coding problems, help me understand complex Python concepts, guide me through error resolution, and offer advice on best practices. Your duty will also involve generating new code snippets when required. Your aim should be to enhance my Python programming skills.

question: {question}

Answer in Markdown format in Korean:"""

prompt_generator = """I want you to act as a ChatGPT prompt generator, I will send a topic, you have to generate a ChatGPT prompt based on the content of the topic, the prompt should start with "I want you to act as ", and guess what I might do, and expand the prompt accordingly Describe the content to make it useful.

topic:
{topic}"""