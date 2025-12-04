import json
from steps import *

st.set_page_config(page_title="Frequency filters", page_icon="🎨",layout="wide",
                    menu_items={"About":"Цей застосунок створено у 2025 році у межах кваліфікаційної магістерської роботи"})

with open('notes.json', 'r', encoding='utf-8') as f:
    st.session_state["notes"] = json.load(f)

with open("examples/examples.json", "r", encoding="UTF-8") as read_file:
    st.session_state["examples_dicts"] = json.load(read_file)

st.header("**Фільтри у частотній області**")

st.session_state["image"] = st.file_uploader("Оберіть зображення, щоб почати:", 
                    type=["png", "jpg", "jpeg"], 
                    on_change=img_changed,
                    help="Всі результати попередніх дій буде втрачено " \
                    "щоразу, коли буде завантажено новий файл")

css='''
<style>
[data-testid="stFileUploaderDropzone"] div div::before {content:"Оберіть файл чи підтягніть його сюди"}
[data-testid="stFileUploaderDropzone"] div div span{display:none;}
[data-testid="stFileUploaderDropzone"] div div::after {color:red; font-size: .8em; content:"Ліміт: 200MB для одного файлу"}
[data-testid="stFileUploaderDropzone"] div div small{display:none;}
[data-testid="stFileUploaderDropzone"] button {visibility: hidden;}
[data-testid="stFileUploaderDropzone"] button::after {content:"Шукати файл";  visibility: visible;}
[data-testid="stStatusWidget"] { visibility: hidden; }
</style>
'''

st.markdown(css, unsafe_allow_html=True)

if st.session_state["image"] is not None:

    display_original_image()
        

    if st.session_state["original_ft"] is not None:

        st.divider()

        display_original_spectrum()

        st.divider()
        
        display_settings()

        filter_and_display()
        
st.divider()

display_examples()
