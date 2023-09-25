import streamlit as st
import pikepdf as pp
import time
from time import sleep
from stqdm import stqdm
from streamlit_extras.add_vertical_space import add_vertical_space
import PyPDF2
from streamlit_option_menu import option_menu
import os
import PyPDF2
import base64
from PyPDF2 import PdfReader, PdfWriter

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
st.image("png.jpg")
selected = option_menu(None, ["Home","Encrypt pdf","Decrypt pdf", "Read PDF"], 
icons=["house","lock","key", "book"],
default_index=0,
orientation="horizontal",
styles={"nav-link": {"font-size": "25px", "text-align": "center", "margin": "0px", "--hover-color": "red", "transition": "color 0.3s ease, background-color 0.3s ease"},
        "icon": {"font-size": "25px"},
        "container": {"max-width": "5000px", "padding": "10px"},
        "nav-link-selected": {"background-color": "green", "color": "white"},
        "nav-link-0": {"icon": "fa-home", "background-color": "#4285F4", "color": "white", "padding-left": "15px"}})

if selected == "Home":
    st.markdown('__<p style="text-align:left; font-size: 23px; color: #020000">Encrypting and decrypting PDF passwords is a crucial security measure to protect the content of PDF files and restrict access to authorized individuals.</P>__',
                unsafe_allow_html=True)
    st.caption("Here are some common use cases for encrypting and decrypting PDF passwords:")
    col1,col2 = st.columns([5,5])
    
    with col1 : 
     st.markdown('__<p style="text-align:left; font-size: 20px; color: #020000">Confidential Document Protection : </P>__',
                unsafe_allow_html=True)
     st.write(" Encrypting PDF files with a password ensures that sensitive or confidential information remains secure and accessible only to authorized users.")
     st.markdown('__<p style="text-align:left; font-size: 20px; color: #020000">Secure Sharing of PDFs : </P>__',
                unsafe_allow_html=True)
     st.write("Encrypting PDFs before sharing via email, cloud storage, or any other means.")
     st.markdown('__<p style="text-align:left; font-size: 20px; color: #020000">Secure Archiving and Storage :</P>__',
                unsafe_allow_html=True)
     st.write("Safely storing confidential PDF documents in archives or databases while ensuring that only authorized personnel can access them.")
    
    with col2 : 
     st.markdown('__<p style="text-align:left; font-size: 20px; color: #020000">Protection of Intellectual Property :</P>__',
                unsafe_allow_html=True)
     st.write("Safeguarding proprietary or intellectual property information from unauthorized access, sharing, or distribution.")
     st.markdown('__<p style="text-align:left; font-size: 20px; color: #020000">Preventing Unauthorized Printing or Copying :</P>__',
                unsafe_allow_html=True)
     st.write("Controlling the printing, copying, or modification of PDF content to maintain its confidentiality and control distribution.")
     st.markdown('__<p style="text-align:left; font-size: 20px; color: #020000">Restricted Access to Sensitive Data :</P>__',
                unsafe_allow_html=True)
     st.write("Limiting access to specific sections or pages of a PDF document containing sensitive data.")
if selected == "Encrypt pdf":
 st.subheader("PDF Password Protection")

# Upload a PDF file
 uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

 if uploaded_file is not None:
    st.write("PDF file successfully uploaded!")

    # Create PdfWriter and add pages
    pdf_writer = PdfWriter()
    pdf_reader = PdfReader(uploaded_file)
    num_pages = len(pdf_reader.pages)

    for page_num in range(num_pages):
        pdf_writer.add_page(pdf_reader.pages[page_num])

    # Get password from user
    password = st.text_input("Enter Password:", type="password")

    if password:
        pdf_writer.encrypt(password)

        # Save the password-protected PDF
        password_protected_filename = 'password_protected.pdf'
        with open(password_protected_filename, 'wb') as f:
            pdf_writer.write(f)

        st.success("PDF file is now password protected!")

        # Encode the PDF file to base64 for download
        with open(password_protected_filename, "rb") as f:
            pdf_bytes = f.read()
            pdf_base64 = base64.b64encode(pdf_bytes).decode()

        # Create a link to download the password-protected PDF
        href = f'<a href="data:application/octet-stream;base64,{pdf_base64}" download="{password_protected_filename}">Download password protected PDF</a>'
        st.markdown(href, unsafe_allow_html=True)

        os.remove(password_protected_filename)  # Remove the temporary PDF file

    else:
        st.warning("Please enter a password.")
if selected == "Decrypt pdf":
    def main():
     st.markdown('__<p style="text-align:left; font-size: 28px; color: #020000">PDF Password Finder </P>__',
                unsafe_allow_html=True)

     st.write("Upload the PDF file and the passwords file, and the app will try to find the password for the PDF.")
     df_file = st.file_uploader("Upload PDF file", type=["pdf"])

     if df_file is not None:
        st.info(f"Selected PDF file :  {df_file.name}", icon="ℹ️")
     add_vertical_space(3)
     st.write("Select the passwords file : ")
     password_list = st.selectbox("Choose a file", ["combo.txt","rockyou_1.txt","rockyou_2.txt","permutations.txt"])
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



