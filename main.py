from langchain_openai import ChatOpenAI
import pyperclip
import pytesseract
from PIL import ImageGrab
from langchain_core.messages import SystemMessage,HumanMessage
from viewer import show_output
import cv2
import numpy as np


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
model = ChatOpenAI(model="gpt-5-mini", temperature=0.4)


def preprocess_image(img):
    img_cv=cv2.cvtColor(np.array(img),cv2.COLOR_RGB2BGR)
    gray=cv2.cvtColor(img_cv,cv2.COLOR_BGR2GRAY)
    
    scale_percent=180
    width=int(gray.shape[1]*scale_percent/100)
    height=int(gray.shape[0]*scale_percent/100)
    gray=cv2.resize(gray,(width,height),interpolation=cv2.INTER_LINEAR)


    _,thresh=cv2.threshold(gray,150,255,cv2.THRESH_BINARY)
    return thresh

def get_clipboard_input():
    img = ImageGrab.grabclipboard()
    if img:
        processed_img=preprocess_image(img)

        config="--oem 3 --psm 4"
        extracted = pytesseract.image_to_string(processed_img,lang="eng",config=config)
        return extracted.strip(), "image"

    # Otherwise, check for text
    text = pyperclip.paste()
    if text and text.strip():
        return text.strip(), "text"

    # If nothing useful found
    return None, None
def main():
    input_data,type_of_input=get_clipboard_input()

    if not input_data:
        print("Clipboard empty")
        return
    
    print(f"📋 Input ({type_of_input}):\n{input_data[:500]}...\n")

    system_prompt = """
    You are an AI assistant. Input may come from plain clipboard text or OCR (screenshot).

    Rules:
    - If the input is a coding question: return the solution in a Python code block with proper indentation and explanatory comments.
    - If the input is a non-coding question: return the answer in Markdown format with headings and subheadings.
    - Always clean up OCR mistakes if possible and produce structured, readable output.

    Examples:

    Coding question example:
    Q: "Write a Python function to reverse a string."
    A:python
    def reverse_string(s):
        ""
        Returns the reversed version of the input string.
        ""
        return s[::-1]


    Non-coding question example:
    Q: "What are the benefits of exercise?"
    A:
    # Benefits of Exercise

    ## Physical Health
    - Improves cardiovascular health
    - Strengthens muscles and bones

    ## Mental Health
    - Reduces stress
    - Enhances mood and focus
    """
    messages=[SystemMessage(content=system_prompt),HumanMessage(content=input_data)]

    response=model.invoke(messages)
    output=response.content.strip()
    
    print(output)
    pyperclip.copy(output)
    show_output(output)

if __name__ == "__main__":
    main()
