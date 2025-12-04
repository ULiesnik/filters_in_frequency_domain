import streamlit as st
from filters import *
import numpy as np
from io import BytesIO
from PIL import Image

def display_original_image():

    left, right = st.columns(2)

    with left:
        st.write("Оригінальна світлина:")
        st.image(st.session_state["image"])

    with right:    
        st.write("\n\n\nОберіть, до якого формату зображення Ви хочете застосувати фільтри:")
        st.button("Кольорове фото", on_click=apply_transform, args=(st.session_state["image"], False))
        st.button("Чорно-біла світлина", on_click=apply_transform, args=(st.session_state["image"],True))
        st.write(st.session_state["notes"]['Вступ'])


@st.fragment
def display_original_spectrum():
    if st.session_state['grayscale_flag']:

        left1, right1 = st.columns(2)

        with left1:
            st.write("Чорно-біле зображення:")
            img = Image.open(st.session_state["image"]).convert('L')
            st.image(img)
            image_bytes = img_to_bytes(img)
            download_img_button("Завантажити чорно-біле зображення", img,"grayscale_")

        with right1:            
            st.write("Спектр величин:")
            spectrum = spectrum_log(st.session_state["original_ft"])
            spectrum_norm = normalize_to_uint8(spectrum)
            spectrum_image = Image.fromarray(spectrum_norm).convert('L')
            st.image(spectrum_image)
            download_img_button("Завантажити зображення спектру", spectrum_image, "spectr_")
            
    else:
        
        left1, right1 = st.columns(2)

        with left1:
            st.write(st.session_state["notes"]['RGB'])

        with right1:
            st.write("Спектр величин (для всіх трьох каналів RGB):")
            spectrum = np.array([spectrum_log(channel) for channel in st.session_state["original_ft"]]).transpose(1,2,0)
            spectrum_norm = normalize_to_uint8(spectrum)
            spectrum_image = Image.fromarray(spectrum_norm, 'RGB')
            st.image(spectrum_image)
            download_img_button("Завантажити зображення спектру", spectrum_image, "spectr_")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.write("Спектр величин каналу R:")
            spectrum = np.array(spectrum_log(st.session_state["original_ft"][0]))
            spectrum_norm = normalize_to_uint8(spectrum)
            spectrum_image = Image.fromarray(spectrum_norm, 'L')
            st.image(spectrum_image)
            download_img_button("Завантажити зображення спектру", spectrum_image, "spectr_red_")
            
        with c2:
            st.write("Спектр величин каналу G:")
            spectrum = np.array(spectrum_log(st.session_state["original_ft"][1]))
            spectrum_norm = normalize_to_uint8(spectrum)
            spectrum_image = Image.fromarray(spectrum_norm, 'L')
            st.image(spectrum_image)
            download_img_button("Завантажити зображення спектру", spectrum_image, "spectr_green_")

        with c3:
            st.write("Спектр величин каналу B:")
            spectrum = np.array(spectrum_log(st.session_state["original_ft"][2]))
            spectrum_norm = normalize_to_uint8(spectrum)
            spectrum_image = Image.fromarray(spectrum_norm, 'L')
            st.image(spectrum_image)
            download_img_button("Завантажити зображення спектру", spectrum_image, "spectr_blue_")
            

@st.fragment
def display_settings():
    col1, col2 = st.columns([1, 2])
    with col1:
        st.header("Налаштуйте фільтр:")
        st.session_state["frequency_option"] = st.radio( "Виберіть потрібний Вам фільтр:",
                        ["З пропуском низьких частот", "З пропуском високих частот", 
                        "Смуговий 1", "Смуговий 2"],
                        captions = ["Зміна для частот, нижчих за значення зрізу", 
                                    "Зміна для частот, вищих за значення зрізу",
                                    "Зміна для всіх частот, крім тих, що розташовані між d0 i d1", 
                                    "Зміна значень частот між двома заданими d"])
        if st.session_state["frequency_option"] == "З пропуском низьких частот":
            st.session_state["function_option"] = st.radio( "Виберіть потрібну функцію фільтрації:",
                        ["З ідеальним зрізом", "Гауса", 
                        "Баттерворта", "Лапласа", "Лапласа від Гауса"])
        else:
            st.session_state["function_option"] = st.radio( "Виберіть потрібну функцію фільтрації:",
                        ["З ідеальним зрізом", "Гауса", 
                        "Баттерворта"])
        st.session_state["filter_option"] = st.session_state["function_option"] + " | " + st.session_state["frequency_option"]
        st.session_state["d0"], st.session_state["w"], st.session_state["order"] = None, None, None

        if st.session_state['grayscale_flag']:
            _max = max_value(st.session_state["original_ft"])
        else:
            _max = max_value(st.session_state["original_ft"][0])

        if (st.session_state["frequency_option"] == "З пропуском низьких частот" or st.session_state["frequency_option"] == "З пропуском високих частот") and st.session_state["function_option"] != "Лапласа":
            d0 = st.number_input("Задайте значення зрізу (відсоток від максимльного значення):",1, 99, 33,
                        help=f"Відстань від центру спектру. Максимальне значення, що можна задати, становить 99%, мінімальне - 1%")
            st.session_state["d0"] = _max*d0/100
            
        if st.session_state["frequency_option"] == "Смуговий 1" or st.session_state["frequency_option"] == "Смуговий 2" :
            в0 = st.number_input("Вкажіть значення центру смуги (відсоток від максимального значення):",1, 99, 33,
                        help=f"Відстань від центру спектру. Максимальне значення, що можна задати, становить 99%, мінімальне - 1%")
            st.session_state["d0"] = _max*d0/100
            w = st.number_input("Вкажіть ширину смуги:", 1, 99, 33)
            st.session_state["w"] = _max*w/100

        if st.session_state["function_option"] == "Баттерворта":
            st.session_state["order"] = st.number_input("Вкажіть порядок для фільтра Баттерворта:", 1, 100, 2)
    with col2:
        st.header("")
        st.subheader("Про обрані налаштування:")
        st.write(st.session_state["notes"]["Про фільтри"][st.session_state["filter_option"]]["Про фільтр"])
        st.write(st.session_state["notes"]["Про фільтри"][st.session_state["filter_option"]]["Про параметри"])
        st.write(st.session_state["notes"]["Про фільтри"]["Загальне"])
        st.divider()
        st.subheader("Потрібна підказка щодо інших варіантів?")
        st.write(st.session_state["notes"]["Про фільтри"][st.session_state["filter_option"]]["Альтернативи"])


def display_result():
    left2, right2 = st.columns(2)

    with left2:

        st.write("Спектр після фільтрації:")
        if st.session_state['grayscale_flag']:
            spectrum_filtered = spectrum_log(st.session_state["filtered_ft"])
            spectrum_filtered_norm = normalize_to_uint8(spectrum_filtered)
            spectrum_filtered_image = Image.fromarray(spectrum_filtered_norm).convert('L')
        else:
            spectrum_filtered = np.array([spectrum_log(channel) for channel in st.session_state["filtered_ft"]]).transpose(1,2,0)
            spectrum_filtered_norm = normalize_to_uint8(spectrum_filtered)
            spectrum_filtered_image = Image.fromarray(spectrum_filtered_norm, 'RGB')
        st.image(spectrum_filtered_image)
        download_img_button("Завантажити це зображення", spectrum_filtered_image, "filtered_spectr_")

    with right2:

        st.write("Світлина після зворотного перетворення:")
        if st.session_state['grayscale_flag']:
            image_filtered = np.fft.ifft2(np.fft.ifftshift(st.session_state["filtered_ft"]))
            img_result = np.abs(image_filtered)
            image_result = Image.fromarray(img_result).convert('L')
        else:
            image_filtered = np.array([np.fft.ifft2(np.fft.ifftshift(channel)) for channel in st.session_state["filtered_ft"]]).transpose(1,2,0)
            img_result = normalize_to_uint8(np.abs(image_filtered))
            image_result = Image.fromarray(img_result, 'RGB')
        st.image(image_result)
        download_img_button("Завантажити фільтроване фото", image_result,"filtered_")
        

@st.fragment
def filter_and_display():
    st.button("Застосувати фільтр",on_click=start_filter)
    st.divider()
    if st.session_state["filtration_in_progress"]:
        with st.spinner("Застосування фільтра..."):
            result = apply_filter(
                st.session_state["filter_option"],
                st.session_state["d0"],
                st.session_state["w"],
                st.session_state["order"]
            )

        st.session_state['filtered_ft'] = result
        st.session_state["filtration_in_progress"] = False
        display_result()


@st.fragment
def display_examples():
    if "examples_shown" not in st.session_state:
        st.session_state["examples_shown"] = False
        st.button("Показати приклади", on_click=show_examples)
    else:
        if not st.session_state["examples_shown"]:
            st.button("Показати приклади", on_click=show_examples)
        else:
            st.button("Приховати приклади", on_click=hide_examples)
            st.write("Нижче розташовано кілька прикладів застосування різноманітних фільтрів до одного зображення.")
            for example in st.session_state["examples_dicts"]:
                st.write(example["Descryption"])
                _left, _right = st. columns(2)
                with _left:
                    st.image(example["Spectrum"])
                with _right:
                    st.image(example["Image"])
            st.button("Згорнути приклади", on_click=hide_examples)

        

@st.fragment
def download_img_button(label, image, prefix):
    spectrum_bytes = img_to_bytes(image)
    st.download_button(label, spectrum_bytes,
        file_name=prefix+st.session_state["image"].name, mime="image/png")
    

def apply_filter(_filter, _d0, _w, _order):
    if st.session_state['grayscale_flag']:
        return frequency_filter(_filter, st.session_state["original_ft"], _d0, _w, _order)
    else:
        filtered = []
        for channel in st.session_state['original_ft']:
            filtered.append(frequency_filter(_filter, channel, _d0, _w, _order))
        return np.array(filtered)
    

def start_filter():
    st.session_state["filtration_in_progress"] = True
    

def show_examples():
    st.session_state["examples_shown"] = True
    

def hide_examples():
    st.session_state["examples_shown"] = False
    

def img_to_bytes(img):
    buf = BytesIO()
    img.save(buf, format="png")
    return buf.getvalue()


def spectrum_log(_ft): # логарифмічна шкала для кращого відображення:
    return np.log(np.abs(_ft)+1) 

def normalize_to_uint8(arr):
    arr = arr - arr.min()
    if arr.max() > 0:
        arr = arr / arr.max()
    return (arr * 255).astype(np.uint8)

def apply_transform(_image, _grayscale):
    st.session_state['grayscale_flag'] = _grayscale
    if _grayscale:
        img = Image.open(_image).convert('L')
        _ft = np.fft.fftshift(np.fft.fft2(img))
    else:
        img = Image.open(_image).convert('RGB')
        img = np.array(img)
        _ft = []
        for c in range(3):
            _ft.append(np.fft.fftshift(np.fft.fft2(img[:, :, c])))
    st.session_state["original_ft"] = np.array(_ft)
    return


def img_changed():
    st.session_state["original_ft"] = None
    st.session_state["filtered_ft"] = None
    st.session_state["grayscale_flag"] = None
    st.session_state["filtration_in_progress"] = False


def max_value(_ft):
    M, N = _ft.shape
    m, n = M//2, N//2
    return np.sqrt((m ** 2) + (n ** 2))

