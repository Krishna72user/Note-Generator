from playwright.sync_api import sync_playwright
import markdown
from google import genai


def write_llm_to_pdf(llm_markdown_text):
    # 1. Convert the Gemini markdown output into standard HTML tags
    html_body = markdown.markdown(llm_markdown_text,extensions=["tables","fenced_code"])
    
    html_doc = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
        </head>
        <body>
        {html_body}
        </body>
        </html>
        """

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.set_content(html_doc)

        pdf_bytes = page.pdf(
            format="A4",
            print_background=True,
            margin={
                "top": "2cm",
                "right": "2cm",
                "bottom": "2cm",
                "left": "2cm"
            }
        )

        browser.close()
        return pdf_bytes
    
def llm_response(prompt):

    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )
    if response.candidates[0].finish_reason == 'STOP':
        return response.text
    else: 
        return "An error occurred"


def generate_notes(prompt,title):
    mod_prompt = """
    Act as an expert university professor in Digital Electronics and Computer Architecture. Provide comprehensive, end-to-end, and deeply technical study notes on "Sequential Circuits." 

    Structure the notes logically using clear markdown headings (H2, H3,H4), bold text for key terms, and code blocks/tables where appropriate. Avoid skipping steps or summarizing crucially technical details.

    Generate exam oriented notes.

    Please follow this exact blueprint for the notes:

    ## **Important !**
        **Do not use LaTeX.**

        Use plain text notation:
        - Q_(n+1) instead of Q_{n+1}
        - R̅ instead of \\overline{R}
        - AND instead of \\cdot
        - Don't use $ sign(strictly).
        - Use valid markdown, so that it can be parsed by wkhtmltopdf

    ---
    """+prompt  + f"\n## **Title : {title}**"
    response = llm_response(mod_prompt)
    return write_llm_to_pdf(response),response

def summarize(text):
    prompt = f"""
    # Role : You are an expert text summarizer who summarizes text and notes in plain text.
    ## **Instructions : **
        1. Generate a 2-3 line plain text summary of the given text.
        2. Strictly, don't use latex or markdown.
    ## --- The text you have to summarize is given below ---
    {text}
    """
    return llm_response(prompt)



