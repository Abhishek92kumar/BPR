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
