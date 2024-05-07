import tkinter as tk
from tkinter import scrolledtext, ttk
import requests
from bs4 import BeautifulSoup
import difflib
from PIL import Image, ImageTk

def search_page(query):
    search_url = f"https://www.google.com/search?q=site:wikipedia.org+{query}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    page_link = None
    for link in soup.find_all('a'):
        url = link.get('href')
        if url.startswith('/url?q=https://en.wikipedia.org/wiki/'):
            page_link = url.split('/url?q=')[1].split('&')[0]
            break
    return page_link

def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    content_div = soup.find(id='mw-content-text')
    paragraphs = content_div.find_all('p')
    text = '\n'.join([p.get_text() for p in paragraphs])
    return text

def extract_section(page_content, section_title):
    start_index = page_content.find(section_title)
    if start_index != -1:
        end_index = page_content.find("==", start_index + len(section_title))
        if end_index != -1:
            return page_content[start_index:end_index].strip()
    return "Sorry, no information found for this section."

def handle_query(query, page_content):
    query_sections = {
        'history': 'History',
        'definition': 'Definition',
        'notable': 'Notable',
        'advantages': 'Advantages',
        'disadvantages': 'Disadvantages',
        'uses': 'Uses',
        'features': 'Features',
        'application': 'Application',
        'variants': 'Variants',
        'technology': 'Technology',
        'usage': 'Usage',
        'overview': 'Overview',
        'properties': 'Properties',
        'benefits': 'Benefits',
        'risks': 'Risks',
        'comparison': 'Comparison',
        'regulation': 'Regulation',
        'future': 'Future',
        'structure': 'Structure',
        'components': 'Components',
        'working': 'Working',
        'advancements': 'Advancements',
        'statistics': 'Statistics'
    }

    best_match = difflib.get_close_matches(query.lower(), query_sections.keys(), n=1, cutoff=0.6)

    if best_match:
        return extract_section(page_content, query_sections[best_match[0]])
    else:
        return page_content

def chatbot(query):
    page_link = search_page(query)
    if page_link:
        page_content = scrape_page(page_link)
        if page_content:
            return handle_query(query, page_content)
        else:
            return "Sorry, I couldn't retrieve information for that topic."
    else:
        return "Sorry, I couldn't find information on that topic."

def submit_query():
    user_input = input_text.get("1.0", tk.END).strip()
    if user_input:
        response = chatbot(user_input)
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, response)
        output_text.config(state=tk.DISABLED)

window = tk.Tk()
window.title("Chatbot")
window.geometry("800x600")
window.configure(bg='#f0f0f0')

# Logo
logo_image = Image.open("logo.png")
logo_image = logo_image.resize((100, 100), Image.ANTIALIAS)
logo_photo = ImageTk.PhotoImage(logo_image)

logo_label = ttk.Label(window, image=logo_photo, background='#f0f0f0')
logo_label.pack(pady=20)

# Title
title_label = ttk.Label(window, text="Chatbot", font=("Arial", 24), background='#f0f0f0')
title_label.pack()

input_frame = ttk.Frame(window)
input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=20)

input_label = ttk.Label(input_frame, text="Enter your query:", font=("Arial", 14), background='#f0f0f0')
input_label.pack(side=tk.LEFT, padx=(0, 5))

input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, width=50, height=3, bg='#e0e0e0', font=("Arial", 12))
input_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

submit_button = ttk.Button(window, text="Submit", command=submit_query)
submit_button.pack(pady=10)

output_frame = ttk.Frame(window)
output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

output_label = ttk.Label(output_frame, text="Chatbot Response:", font=("Arial", 14), background='#f0f0f0')
output_label.pack(side=tk.LEFT)

output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=70, height=10, bg='#e0e0e0', font=("Arial", 12))
output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
output_text.config(state=tk.DISABLED)

window.mainloop()
