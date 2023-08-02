import streamlit as st
import pikepdf as pp
import time
from time import sleep
from stqdm import stqdm
from streamlit_extras.add_vertical_space import add_vertical_space
import PyPDF2
import fitz
from streamlit_option_menu import option_menu
import os

st.set_page_config(page_title='password', layout='wide', page_icon="#")

reduce_header_height_style = """
    <style>
        div.block-container {padding-top:0rem;}
        div.Sidebar   {padding-top:0rem;}
    </style>
"""
st.markdown(reduce_header_height_style, unsafe_allow_html=True)

hide_st_style ="""
        <style>
        MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """      
st.markdown(hide_st_style,unsafe_allow_html=True)

selected = option_menu(None, ["Home","PDF Password", "Read PDF"], 
icons=["house","key", "book"],
default_index=0,
orientation="horizontal",
styles={"nav-link": {"font-size": "25px", "text-align": "center", "margin": "0px", "--hover-color": "red", "transition": "color 0.3s ease, background-color 0.3s ease"},
        "icon": {"font-size": "25px"},
        "container": {"max-width": "5000px", "padding": "10px"},
        "nav-link-selected": {"background-color": "green", "color": "white"},
        "nav-link-0": {"icon": "fa-home", "background-color": "#4285F4", "color": "white", "padding-left": "15px"}})

if selected == "Home":
    st.markdown('__<p style="text-align:left; font-size: 28px; color: #020000">Finding the password of a PDF can be useful in various scenarios.</P>__',
                unsafe_allow_html=True)
    st.caption(" Here are some of the common uses of finding PDF passwords :")
    st.markdown('__<p style="text-align:left; font-size: 22px; color: #020000">Authorized Access Recovery : </P>__',
                unsafe_allow_html=True)
    st.write(" If you have forgotten the password to a PDF file that you are authorized to access, finding the password can help you regain access to the contents of the file.")
    st.markdown('__<p style="text-align:left; font-size: 22px; color: #020000">Password Recovery : </P>__',
                unsafe_allow_html=True)
    st.write(" If you have encrypted a PDF file with a password and forgotten it, finding the password can help you recover the content without having to recreate the PDF from scratch.")
    st.markdown('__<p style="text-align:left; font-size: 22px; color: #020000">Security Testing :</P>__',
                unsafe_allow_html=True)
    st.write(" In cybersecurity and penetration testing, finding PDF passwords can be part of security assessments to check the strength of passwords used to protect sensitive documents. It helps identify weak passwords that might be vulnerable to brute-force attacks.")
    st.markdown('__<p style="text-align:left; font-size: 22px; color: #020000">Digital Forensics :</P>__',
                unsafe_allow_html=True)
    st.write(" In digital forensics investigations, finding PDF passwords can aid in accessing potentially relevant evidence stored within encrypted PDF files.")
    st.markdown('__<p style="text-align:left; font-size: 22px; color: #020000">Legal and Compliance Purposes :</P>__',
                unsafe_allow_html=True)
    st.write(" Organizations might need to find PDF passwords to access documents for legal or compliance reasons, such as during audits or investigations.")

if selected == "PDF Password":
    def main():
     st.markdown('__<p style="text-align:left; font-size: 28px; color: #020000">PDF Password Finder </P>__',
                unsafe_allow_html=True)

     st.write("Upload the PDF file and the passwords file, and the app will try to find the password for the PDF.")
     df_file = st.file_uploader("Upload PDF file", type=["pdf"])

     if df_file is not None:
        st.info(f"Selected PDF file :  {df_file.name}", icon="ℹ️")
     add_vertical_space(3)
     st.write("Select the passwords file : ")
     password_list = st.selectbox("Choose a file", ["combo.txt","rockyou.txt","permutations.txt"])
     with open(password_list, 'r', encoding='utf-8', errors='ignore') as passwords:
        if st.button("Find Password"):
            i = 0
            start_time = time.time()
            for password in passwords:
                password = password.strip("\n")
                i += 1
                print("\r {} Password Tested! ".format(i), end="")
                try:
                    pp.open(df_file, password=password)
                    end_time = time.time()
                    with st.spinner('Wait for it...'):
                     time.sleep(5)
                    st.write("Password found successfully!!")
                    st.success(" Password : {} ".format(password))
                    st.caption("[{}] PASSWORD TESTED in {} SECONDS. ".format(i, str(end_time - start_time)[:4]))
                    break
                                   
                except:
                    pass
                
    if __name__ == "__main__":
       main()

if selected == "Read PDF":

    def read_encrypted_pdf(pdf_file_path, password):
     with open(pdf_file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        if pdf_reader.decrypt(password):
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        else:
            return None

    def main():
      st.markdown('__<p style="text-align:left; font-size: 28px; color: #020000">PDF Reader </P>__',
                unsafe_allow_html=True)

      st.write("Upload the PDF file and enter the password to read its content.")
      pdf_file = st.file_uploader("Upload Encrypted PDF", type=["pdf"])

      if pdf_file is not None:
        st.info(f"Selected PDF file: {pdf_file.name}", icon="ℹ️")
        password = st.text_input("Enter the password for the PDF", type="password")

        if st.button("Read PDF"):
            if password:
                # Save the uploaded PDF to a temporary location
                with open("temp.pdf", "wb") as temp_file:
                    temp_file.write(pdf_file.read())

                pdf_text = read_encrypted_pdf("temp.pdf", password)
                os.remove("temp.pdf")  # Delete the temporary file

                if pdf_text:
                    st.write("PDF content:")
                    st.text(pdf_text)
                else:
                    st.error("Invalid password. Please try again.")
            else:
                st.error("Please enter the password to read the PDF.")

    if __name__ == "__main__":
     main()



