'''
import streamlit as st
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pandas as pd

# ----------------- STREAMLIT CONFIG -----------------
st.set_page_config(page_title='Aakash Automated BPR', page_icon='🎉', layout="wide")
st.title("📅 Aakash Automated BPR")

# ----------------- GOOGLE API AUTHENTICATION -----------------
def get_credentials():
    """Loads Google OAuth credentials from Streamlit secrets."""
    try:
        # Convert Streamlit secrets to a standard dictionary
        creds_data = dict(st.secrets["google_oauth"])
        # Rebuild the credentials object. If token is expired, the refresh_token renews it automatically.
        creds = Credentials.from_authorized_user_info(
            creds_data, 
            ['https://www.googleapis.com/auth/calendar.readonly']
        )
        return creds
    except Exception as e:
        st.error("❌ Google OAuth Secrets are missing or improperly formatted in Streamlit.")
        return None

# ----------------- UTILITY FUNCTIONS -----------------
def parse_api_time(event_time_dict):
    """Parses Google API time dict into a Python datetime object."""
    # API returns 'dateTime' for specific times, or 'date' for all-day events
    time_str = event_time_dict.get('dateTime') or event_time_dict.get('date')
    if 'T' in time_str:
        # Format: 2023-08-15T10:30:00+05:30 -> strip timezone for simple duration math
        return datetime.fromisoformat(time_str).replace(tzinfo=None)
    return datetime.strptime(time_str, "%Y-%m-%d")

def calculate_duration(start_time, end_time):
    duration = end_time - start_time
    hours, remainder = divmod(duration.total_seconds(), 3600)
    minutes = remainder // 60
    return f"{int(hours)} hr {int(minutes)} min"

def get_class_from_description(description):
    desc = description.upper() if description else ""
    if "FR01" in desc: return "CFSA"
    elif "9W02" in desc: return "IC9X"
    elif "8WI1" in desc: return "IC8X"
    elif "FW02" in desc: return "FSIV"
    elif "TW04" in desc: return "CTYE"
     # for Avinash Sir
    elif "SW01" in desc: return "CSSB"
    elif "SR01" in desc: return "CSSA"
    elif "FW01" in desc: return "CFSB"
    elif "OW03" in desc: return "CCFC"
    # for Siddharth Sir
    elif "RM10" in desc: return "CRF"
    elif "OR01" in desc: return "CCFA"
    elif "OW04" in desc: return "CCFD"
    elif "TW02" in desc: return "CTYC"
    elif "OW01" in desc: return "CCFJ"

    # for Deepak Jain Sir
    elif "RM02" in desc: return "CRA"
    elif "RM09" in desc: return "CRE"
    elif "OW10" in desc: return "COCFA"
    elif "SW02" in desc: return "SSIV"
    elif "TR05" in desc: return "OTYM"
    
    # for Rahul Sir
    elif "RM04" in desc: return "CRB"
    elif "RM06" in desc: return "CRD"
    elif "TR01" in desc: return "CTYA"
    elif "TW01" in desc: return "CCFG"
    elif "OW06" in desc: return "CCFF"
    elif "OW07" in desc: return "CTYB"

    # for Diptarka Ghosh
    elif "TR02" in desc: return "CTYG"
    elif "TW05" in desc: return "CTYF"
    elif "TW03" in desc: return "CTYD"

    # for Susovan Mitra
    elif "RM07" in desc: return "CWRMC"
    elif "RM03" in desc: return "CWRMB"
    elif "RM01" in desc: return "CWRMA"
    elif "TW04" in desc: return "CWTYA"
    elif "9W01" in desc: return "C9XB"
    elif "XW01" in desc: return "C10XB"
    elif "8W01" in desc: return "C8XA"
    elif "XR01" in desc: return "C10XA"

    # for Ratul Rudra
    
    elif "RM08" in desc: return "CWRMD"
    elif "PS01" in desc: return "CPSA"
    elif "OW05" in desc: return "CCFE"
    elif "9W03" in desc: return "ICX9A"
    elif "XW10" in desc: return "CW10X"
    elif "CCM2" in desc: return "CCCN"

    # for Amarjeet Kumar sir
    elif "RM05" in desc: return "CRC"
    elif "9R01" in desc: return "CX9A"
    elif "OW08" in desc: return "CCFH"
    elif "OW09" in desc: return "CCFI"
    elif "OW02" in desc: return "CCFB"
    elif "XWI01" in desc: return "CIC10XA"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"    
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"



    
    return "Other"

# ----------------- MAIN DISPLAY FUNCTION -----------------
def fetch_and_display_schedule(email):
    creds = get_credentials()
    if not creds: return

    with st.spinner(f'Fetching calendar data for {email}...'):
        try:
            # Build the Google Calendar API client
            service = build('calendar', 'v3', credentials=creds)

            # Calculate timeframe: 90 days ago to today
            now = datetime.utcnow()
            time_min = (now - timedelta(days=90)).isoformat() + 'Z'
            time_max = now.isoformat() + 'Z'

            # Fetch events directly from their email address
            events_result = service.events().list(
                calendarId=email,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            raw_events = events_result.get('items', [])
            
        except Exception as e:
            st.error(f"⚠️ Error accessing calendar for {email}. Make sure the email is correct and they are in the @aesl.in directory. Details: {e}")
            return

        if not raw_events:
            st.warning("No events found in the selected timeframe.")
            return

        # Process events
        processed_events = []
        for event in raw_events:
            # Skip events that don't have start/end times
            if 'start' not in event or 'end' not in event:
                continue

            start_time = parse_api_time(event['start'])
            end_time = parse_api_time(event['end'])
            description = event.get('description', '')
            summary = event.get('summary', 'No Title')

            event_info = {
                'Class': get_class_from_description(description),
                'Date': start_time.strftime("%d-%m-%Y"),
                'Day': start_time.strftime("%A"),
                'Time': start_time.strftime("%I:%M %p"),
                'Duration': calculate_duration(start_time, end_time),
                'Summary': summary,
                'start_time': start_time  # kept for sorting
            }
            processed_events.append(event_info)

        # Sort by Class, then by Date
        processed_events.sort(key=lambda x: (x['Class'], x['start_time']), reverse=True)

        # Group by Class and Display
        classes = {}
        for e in processed_events:
            classes.setdefault(e['Class'], []).append(e)

        for class_name, evts in classes.items():
            if evts:
                st.subheader(f"📘 Class: {class_name}")
                df = pd.DataFrame(evts).drop(columns=['start_time'])
                st.markdown(df.to_html(index=False, classes='styled-table'), unsafe_allow_html=True)

# ----------------- CSS FOR BEAUTIFUL TABLE -----------------
st.markdown("""
    <style>
        .styled-table { border-collapse: collapse; margin: 20px 0; font-size: 0.9em; font-family: 'Trebuchet MS', sans-serif; min-width: 700px; width: 100%; box-shadow: 0 0 20px rgba(0, 0, 0, 0.15); }
        .styled-table thead tr { background-color: #009879; color: #ffffff; text-align: left; }
        .styled-table th, .styled-table td { padding: 12px 15px; }
        .styled-table tbody tr { border-bottom: 1px solid #dddddd; background-color: #2d2d2d; color: #ffffff; }
        .styled-table tbody tr:nth-of-type(even) { background-color: #3e3e3e; }
        .styled-table tbody tr:last-of-type { border-bottom: 2px solid #009879; }
    </style>
""", unsafe_allow_html=True)

# ----------------- UI -----------------
st.sidebar.header("👨‍🏫 Faculty Lookup")
target_email = st.sidebar.text_input("Enter Faculty Email Address:", value="xxxxxx@aesl.in")

if st.sidebar.button("📥 Fetch Schedule"):
    if target_email.endswith("@aesl.in"):
        fetch_and_display_schedule(target_email)
    else:
        st.sidebar.error("Please enter a valid @aesl.in email address.")

'''

import streamlit as st
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pandas as pd
from io import BytesIO
from fpdf import FPDF

# ----------------- STREAMLIT CONFIG -----------------
st.set_page_config(page_title='Aakash Automated BPR', page_icon='🎉', layout="wide")
st.title("📅 Aakash Automated BPR")

# ----------------- GOOGLE API AUTHENTICATION -----------------
def get_credentials():
    try:
        creds_data = dict(st.secrets["google_oauth"])
        creds = Credentials.from_authorized_user_info(
            creds_data, 
            ['https://www.googleapis.com/auth/calendar.readonly']
        )
        return creds
    except Exception as e:
        st.error("❌ Google OAuth Secrets are missing or improperly formatted.")
        return None

# ----------------- UTILITY FUNCTIONS -----------------
def parse_api_time(event_time_dict):
    time_str = event_time_dict.get('dateTime') or event_time_dict.get('date')
    if 'T' in time_str:
        return datetime.fromisoformat(time_str).replace(tzinfo=None)
    return datetime.strptime(time_str, "%Y-%m-%d")

def calculate_duration(start_time, end_time):
    duration = end_time - start_time
    hours, remainder = divmod(duration.total_seconds(), 3600)
    minutes = remainder // 60
    return f"{int(hours)} hr {int(minutes)} min"

def get_class_from_description(description):
    desc = description.upper() if description else ""
    # for Abhishek Sir
    if "FR01" in desc: return "CFSA"
    elif "9W02" in desc: return "IC9X"
    elif "8WI1" in desc: return "IC8X"
    elif "FW02" in desc: return "FSIV"
    elif "TW04" in desc: return "CTYE"
     # for Avinash Sir
    elif "SW01" in desc: return "CSSB"
    elif "SR01" in desc: return "CSSA"
    elif "FW01" in desc: return "CFSB"
    elif "OW03" in desc: return "CCFC"
    # for Siddharth Sir
    elif "RM10" in desc: return "CRF"
    elif "OR01" in desc: return "CCFA"
    elif "OW04" in desc: return "CCFD"
    elif "TW02" in desc: return "CTYC"
    elif "OW01" in desc: return "CCFJ"

    # for Deepak Jain Sir
    elif "RM02" in desc: return "CRA"
    elif "RM09" in desc: return "CRE"
    elif "OW10" in desc: return "COCFA"
    elif "SW02" in desc: return "SSIV"
    elif "TR05" in desc: return "OTYM"
    
    # for Rahul Sir
    elif "RM04" in desc: return "CRB"
    elif "RM06" in desc: return "CRD"
    elif "TR01" in desc: return "CTYA"
    elif "TW01" in desc: return "CCFG"
    elif "OW06" in desc: return "CCFF"
    elif "OW07" in desc: return "CTYB"

    # for Diptarka Ghosh
    elif "TR02" in desc: return "CTYG"
    elif "TW05" in desc: return "CTYF"
    elif "TW03" in desc: return "CTYD"

    # for Susovan Mitra
    elif "RM07" in desc: return "CWRMC"
    elif "RM03" in desc: return "CWRMB"
    elif "RM01" in desc: return "CWRMA"
    elif "TW04" in desc: return "CWTYA"
    elif "9W01" in desc: return "C9XB"
    elif "XW01" in desc: return "C10XB"
    elif "8W01" in desc: return "C8XA"
    elif "XR01" in desc: return "C10XA"

    # for Ratul Rudra
    
    elif "RM08" in desc: return "CWRMD"
    elif "PS01" in desc: return "CPSA"
    elif "OW05" in desc: return "CCFE"
    elif "9W03" in desc: return "ICX9A"
    elif "XW10" in desc: return "CW10X"
    elif "CCM2" in desc: return "CCCN"

    # for Amarjeet Kumar sir
    elif "RM05" in desc: return "CRC"
    elif "9R01" in desc: return "CX9A"
    elif "OW08" in desc: return "CCFH"
    elif "OW09" in desc: return "CCFI"
    elif "OW02" in desc: return "CCFB"
    elif "XWI01" in desc: return "CIC10XA"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"    
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"
    # elif "SW01" in desc: return "CSSB"



    

    

    
    return "Other"

# ----------------- DOWNLOAD GENERATORS -----------------
def create_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Schedule')
    return output.getvalue()

def create_pdf(df):
    pdf = FPDF(orientation='L') # Landscape mode for better table fit
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    
    # Headers
    cols = df.columns.tolist()
    col_widths = [20, 25, 25, 25, 25, 120] # Adjusting widths (Class, Date, Day, Time, Duration, Summary)
    
    pdf.set_font("Arial", 'B', 10)
    for i, col in enumerate(cols):
        pdf.cell(col_widths[i], 10, str(col), border=1)
    pdf.ln()
    
    # Data Rows
    pdf.set_font("Arial", size=9)
    for _, row in df.iterrows():
        for i, item in enumerate(row):
            # Sanitize text to prevent FPDF character encoding errors
            text = str(item).encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(col_widths[i], 10, text[:65], border=1) # truncate extremely long summaries
        pdf.ln()
        
    return pdf.output(dest='S').encode('latin-1')

# ----------------- MAIN DISPLAY FUNCTION -----------------
def fetch_and_display_schedule(email, name_label):
    creds = get_credentials()
    if not creds: return

    with st.spinner(f'Fetching calendar data for {name_label}...'):
        try:
            service = build('calendar', 'v3', credentials=creds)
            now = datetime.utcnow()
            time_min = (now - timedelta(days=90)).isoformat() + 'Z'
            time_max = now.isoformat() + 'Z'

            events_result = service.events().list(
                calendarId=email, timeMin=time_min, timeMax=time_max,
                singleEvents=True, orderBy='startTime'
            ).execute()

            raw_events = events_result.get('items', [])
        except Exception as e:
            st.error(f"⚠️ Error accessing calendar for {email}. Details: {e}")
            return

        if not raw_events:
            st.warning("No events found in the selected timeframe.")
            return

        # processed_events = []
        # for event in raw_events:
        #     if 'start' not in event or 'end' not in event:
        #         continue

        #     start_time = parse_api_time(event['start'])
        #     end_time = parse_api_time(event['end'])
        #     description = event.get('description', '')
        #     summary = event.get('summary', 'No Title')
        processed_events = []
        for event in raw_events:
            if 'start' not in event or 'end' not in event:
                continue

            start_time = parse_api_time(event['start'])
            end_time = parse_api_time(event['end'])
            
            # --- NEW FEATURE: Skip events shorter than 10 minutes (600 seconds) ---
            if (end_time - start_time).total_seconds() < 600:
                continue
            # ----------------------------------------------------------------------

            description = event.get('description', '')
            summary = event.get('summary', 'No Title')

            processed_events.append({
                'Class': get_class_from_description(description),
                'Date': start_time.strftime("%d-%m-%Y"),
                'Day': start_time.strftime("%A"),
                'Time': start_time.strftime("%I:%M %p"),
                'Duration': calculate_duration(start_time, end_time),
                'Summary': summary,
                'start_time': start_time 
            })
            # processed_events.append({
            #     'Class': get_class_from_description(description),
            #     'Date': start_time.strftime("%d-%m-%Y"),
            #     'Day': start_time.strftime("%A"),
            #     'Time': start_time.strftime("%I:%M %p"),
            #     'Duration': calculate_duration(start_time, end_time),
            #     'Summary': summary,
            #     'start_time': start_time 
            # })

        processed_events.sort(key=lambda x: (x['Class'], x['start_time']), reverse=True)
        
        # Create a flat DataFrame for the downloads
        all_df = pd.DataFrame(processed_events).drop(columns=['start_time'])

        # Group by Class
        classes = {}
        for e in processed_events:
            classes.setdefault(e['Class'], []).append(e)

        # SORTING LOGIC: Push "Other" to the bottom
        # This sorts the keys so that if key == 'Other' (True), it gets evaluated as 1 and moves to the end.
        sorted_class_names = sorted(classes.keys(), key=lambda k: (k == "Other", k))

        for class_name in sorted_class_names:
            evts = classes[class_name]
            st.subheader(f"📘 Class: {class_name}")
            df = pd.DataFrame(evts).drop(columns=['start_time'])
            st.markdown(df.to_html(index=False, classes='styled-table'), unsafe_allow_html=True)
            
        # ----------------- DOWNLOAD BUTTONS -----------------
        st.write("---")
        st.subheader("📥 Export Schedule")
        col1, col2, col3 = st.columns(3)
        
        safe_name = name_label.replace(" ", "_")
        
        # CSV
        csv_data = all_df.to_csv(index=False).encode('utf-8')
        col1.download_button("Download CSV", data=csv_data, file_name=f"{safe_name}_Schedule.csv", mime="text/csv")
        
        # Excel
        excel_data = create_excel(all_df)
        col2.download_button("Download Excel", data=excel_data, file_name=f"{safe_name}_Schedule.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        
        # PDF
        pdf_data = create_pdf(all_df)
        col3.download_button("Download PDF", data=pdf_data, file_name=f"{safe_name}_Schedule.pdf", mime="application/pdf")

# ----------------- CSS FOR BEAUTIFUL TABLE -----------------
st.markdown("""
    <style>
        .styled-table { border-collapse: collapse; margin: 20px 0; font-size: 0.9em; font-family: 'Trebuchet MS', sans-serif; min-width: 700px; width: 100%; box-shadow: 0 0 20px rgba(0, 0, 0, 0.15); }
        .styled-table thead tr { background-color: #009879; color: #ffffff; text-align: left; }
        .styled-table th, .styled-table td { padding: 12px 15px; }
        .styled-table tbody tr { border-bottom: 1px solid #dddddd; background-color: #2d2d2d; color: #ffffff; }
        .styled-table tbody tr:nth-of-type(even) { background-color: #3e3e3e; }
        .styled-table tbody tr:last-of-type { border-bottom: 2px solid #009879; }
    </style>
""", unsafe_allow_html=True)

# ----------------- UI / SIDEBAR -----------------
st.sidebar.header("👨‍🏫 Faculty Lookup")

# Load faculty dictionary from secrets
try:
    faculty_dict = dict(st.secrets["faculty_directory"])
except Exception:
    faculty_dict = {}

# Build the dropdown options
options = ["-- Select Faculty --"] + list(faculty_dict.keys()) + ["Search by Custom Email..."]

# The selectbox natively allows the user to type to search!
selected_option = st.sidebar.selectbox("Search Name or Select:", options)

target_email = ""
if selected_option == "Search by Custom Email...":
    target_email = st.sidebar.text_input("Enter @aesl.in email:")
elif selected_option != "-- Select Faculty --":
    target_email = faculty_dict[selected_option]

if st.sidebar.button("📥 Fetch Schedule"):
    if target_email and target_email.endswith("@aesl.in"):
        # Pass both email and the display name for the download files
        fetch_and_display_schedule(target_email, selected_option)
    else:
        st.sidebar.error("Please provide a valid @aesl.in email address.")
