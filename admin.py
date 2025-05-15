import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import os
from datetime import date
from PIL import Image
from datetime import date, timedelta
import warnings
warnings.filterwarnings("ignore")
warnings.simplefilter(action='ignore', category=FutureWarning)

allow_update = True
back_date = True

def admin_ui(df_wholesale):
    # --- DB SETUP ---
    conn = sqlite3.connect("users.db", check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Whole_Saler_id REAL NOT NULL,       
        Whole_Saler TEXT NOT NULL,
        Bill_date TEXT NOT NULL,
        Bill_number TEXT UNIQUE NOT NULL,
        Bill_photo TEXT,
        Sale_qty REAL
    )
    """)
    conn.commit()

    # --- IMAGE FOLDER ---
    if not os.path.exists("images"):
        os.makedirs("images")
    # --- WHOLESALER DATA ---
    
    df_wholesale['A'] = df_wholesale['Id'].astype(str) + "-"+ df_wholesale["Whole_Saler"]+"_( "+df_wholesale["Name_of_Route"] + " )"
    

    whole_salers = df_wholesale['A'].unique()
    # --- APP TITLE ---
    st.title("📦 QPS Bill Entry System")
    # Initialize session state to expand by default on first load
    if "expand_qps" not in st.session_state:
        st.session_state.expand_qps = True

    with st.expander("See QPS Scheme",expanded=st.session_state.expand_qps):
        
        st.image("logo/QPSScheme.jpeg", use_container_width=True)
    st.session_state.expand_qps = False 

    with st.expander('Data Uplode and Download System '):
        uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])
        if uploaded_file is not None:
            # Read Excel file
            try:
                df = pd.read_excel(uploaded_file,sheet_name='DB')
                df1 = pd.read_excel(uploaded_file,sheet_name='data')
                df.to_parquet('DATA/DB.parquet',index=False)
                df1.to_parquet('DATA/data.parquet',index=False)
                st.success("File successfully uploaded and read! and Write")

                # Show dataframe
                st.markdown('EXCEL DB Sheet')
                st.dataframe(df.sample(5))
                st.markdown('EXCEL Data Sheet')
                st.dataframe(df1.sample(5))
            except Exception as e:
                st.error(f"Error reading the Excel file: {e}")
    # --- TABS ---
    tab1, tab2 = st.tabs(["➕ Add Bill", "🛠️ Update/Delete Bill"])

    df_bills = pd.read_sql_query("SELECT * FROM bills", conn)
    wholesaler_id = df_wholesale['Id']
    df_bills = df_bills[df_bills['Whole_Saler_id'].isin(wholesaler_id)]
    

    # --- TAB 1: ADD BILL ---
    with tab1:
        st.subheader("➕ Add a New Bill")

        selected_wholesaler = st.selectbox("Select Wholesaler", whole_salers, key="add_wholesaler")
        Whole_Saler_id = selected_wholesaler.split("-")[0]
        if back_date:
            bill_date = st.date_input("Bill Date", value=date.today(), key="add_date")
        else:
            # Set the range: from 3 days ago to today
            min_date = "2025-05-01" #date.today() - timedelta(days=2)
            max_date = date.today()

            # Date input with restriction
            bill_date = st.date_input("Bill Date", 
                                    value=date.today(), 
                                    min_value=min_date, 
                                    max_value=max_date,
                                    key="add_date")    

        bill_number = st.text_input("Bill Number (unique)", key="add_bill_no")
        sale_qty = st.number_input("Sale Quantity", min_value=0, step=5, key="add_qty")
        uploaded_file = st.file_uploader("Upload Bill Photo", type=["jpg", "jpeg", "png"], key="add_upload")

        bill_photo_path = None
        if uploaded_file is not None:
            extension = uploaded_file.name.split('.')[-1]
            bill_photo_path = f"images/{bill_number}.{extension}"
            with open(bill_photo_path, "wb") as f:
                f.write(uploaded_file.read())
            st.image(bill_photo_path, caption="Uploaded Bill Photo", use_container_width=True)

        if st.button("Add Bill", key="add_btn"):
            if not bill_number:
                st.warning("⚠️ Bill number is required.")
            elif not uploaded_file:
                st.warning("⚠️ Please upload a bill photo.")
            else:
                try:
                    cursor.execute("""
                        INSERT INTO bills (Whole_Saler_id,Whole_Saler, Bill_date, Bill_number, Bill_photo, Sale_qty)
                        VALUES (?,?, ?, ?, ?, ?)
                    """, (Whole_Saler_id,selected_wholesaler, bill_date, bill_number, bill_photo_path, sale_qty))
                    conn.commit()
                    st.success("✅ Bill added successfully.")
                except sqlite3.IntegrityError:
                    st.error("⚠️ Bill number already exists!")

    # --- TAB 2: UPDATE / DELETE ---
    with tab2:
        st.subheader("🛠️ Update or Delete Bill")
        if allow_update:
            if df_bills.empty:
                st.info("ℹ️ No bills to show.")
            else:
                selected_bill_id = st.selectbox("Select Bill ID to Edit", df_bills['id'], key="edit_id")

                bill_to_edit = df_bills[df_bills['id'] == selected_bill_id].iloc[0]

                new_bill_date = st.date_input("Bill Date", value=pd.to_datetime(bill_to_edit['Bill_date']), key=f"edit_date_{selected_bill_id}")
                new_sale_qty = st.number_input("Sale Quantity", min_value=0, value=float(bill_to_edit['Sale_qty']), step=0.1, key="edit_qty")
                uploaded_file_update = st.file_uploader("Update Bill Photo (optional)", type=["jpg", "jpeg", "png"], key="edit_upload")

                updated_photo_path = bill_to_edit['Bill_photo']
                if uploaded_file_update is not None:
                    extension = uploaded_file_update.name.split('.')[-1]
                    updated_photo_path = f"images/{bill_to_edit['Bill_number']}.{extension}"
                    with open(updated_photo_path, "wb") as f:
                        f.write(uploaded_file_update.read())
                    st.image(updated_photo_path, caption="Updated Bill Photo", use_container_width=True)

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("Update Bill", key="update_btn"):
                        cursor.execute("""
                            UPDATE bills
                            SET Bill_date=?, Bill_photo=?, Sale_qty=?
                            WHERE id=?
                        """, (new_bill_date, updated_photo_path, new_sale_qty, selected_bill_id))
                        conn.commit()
                        st.success("✅ Bill updated successfully.")

                with col2:
                    if st.button("Delete Bill", key="delete_btn"):
                        # Delete image first
                        image_path = bill_to_edit['Bill_photo']
                        cursor.execute("DELETE FROM bills WHERE id=?", (selected_bill_id,))
                        conn.commit()
                        if image_path and os.path.exists(image_path):
                            os.remove(image_path)
                        st.success("✅ Bill deleted successfully.")
        else:
            st.markdown("### ❌ You have not permisson to edit or delete Bills")                

    # --- DISPLAY ALL BILLS ---
    st.markdown("### 📑 All Stored Bills")
    df_bills.set_index('id',inplace=True)

    # Show images in the 'Bill_photo' column using st.data_editor
    # st.data_editor(
    #     df_bills,
    #     column_config={
    #         "Bill_photo": st.column_config.ImageColumn(
    #             "Bill Photo",  # Column label
    #             help="Photo of the bill",
    #             width="medium"  # Options: 'small', 'medium', 'large'
    #         )
    #     },
    #     hide_index=True
    # )
    st.write(df_bills)

    st.markdown("### 📑 All Whole Seller TGT V/S ACH %")

    #st.write(df_wholesale)
    # Step 1: Create a month-year column in format "Apr-24"
    try:
        df_bills['Bill_date'] = pd.to_datetime(df_bills['Bill_date'])
        df_bills['month_str'] = df_bills['Bill_date'].dt.strftime('%b-%y')
        # Step 2: Streamlit selectbox for month
        unique_months = df_bills['month_str'].unique()
        selected_month = st.selectbox("Select Month", sorted(unique_months))
        # Step 3: Filter data by selected month
        filtered_df = df_bills[df_bills['month_str'] == selected_month]
        pivot_df = filtered_df.pivot_table(index='Whole_Saler_id', values='Sale_qty', aggfunc='sum').reset_index()
        merge = pd.merge(df_wholesale,pivot_df,left_on='Id',right_on='Whole_Saler_id',how='left')
        merge.drop(columns=['A','Whole_Saler_id'],inplace=True)
        merge['Balance'] = merge['TGT'] - merge['Sale_qty']
        merge['Balance'] = np.where( merge['Balance'] < 0, np.nan,merge['Balance'])
        merge['Ach%'] =  np.round(merge['Sale_qty']*100/merge['TGT'],1)
        merge['Ach%'] = merge['Ach%'].astype(str)+" %"
        st.write(merge)
    except:
        pass   
    conn.close()
