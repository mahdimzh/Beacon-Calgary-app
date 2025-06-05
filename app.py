import streamlit as st
import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv
import folium
from streamlit_folium import st_folium
from folium import plugins

# --- App Configuration ---
st.set_page_config(layout="wide", page_title="Beacon Calgary", page_icon="📍")

# --- Load Environment Variables ---
load_dotenv()
api_key_input = os.getenv("OPENAI_API_KEY")

# --- Extended Data for Calgary Locations ---
locations_data = [
    # Shelters
    {
        "name": "Calgary Drop-In Centre",
        "type": "Shelter",
        "latitude": 51.0444,
        "longitude": -114.0500,
        "address": "1 Dermot Baldwin Way SE, Calgary, AB T2G 0P8",
        "status": "Open",
        "current_needs": ["Warm blankets", "Men's winter socks (new)", "Toothpaste & toothbrushes"],
        "hours": "24/7 for registered clients; Day services 8 AM - 8 PM",
        "contact": "403-263-5707",
        "description": "Provides emergency shelter, health services, employment training, and housing support.",
        "icon": "🏠",
        "category": "shelter"
    },
    {
        "name": "Alpha House Society",
        "type": "Shelter & Detox",
        "latitude": 51.0390,
        "longitude": -114.0590,
        "address": "203 15 Ave SE, Calgary, AB T2G 1G4",
        "status": "Limited",
        "current_needs": ["Men's gloves/mittens", "Travel-size shampoo", "New underwear (all sizes)"],
        "hours": "24/7 for shelter and detox programs",
        "contact": "403-234-7388",
        "description": "Offers shelter, detox, and outreach programs for individuals struggling with addiction and homelessness.",
        "icon": "🏠",
        "category": "shelter"
    },
    {
        "name": "The Mustard Seed",
        "type": "Shelter & Community Support",
        "latitude": 51.0423,
        "longitude": -114.0613,
        "address": "102 11 Ave SE, Calgary, AB T2G 0X5",
        "status": "Open",
        "current_needs": ["Canned protein (tuna, chicken)", "Coffee", "Women's hygiene products"],
        "hours": "Shelter 24/7; Community Centre Mon-Fri 9 AM - 4 PM",
        "contact": "403-269-1319",
        "description": "Provides shelter, meals, wellness programs, and employment coaching.",
        "icon": "🏠",
        "category": "shelter"
    },
    {
        "name": "Inn from the Cold",
        "type": "Family Shelter",
        "latitude": 51.0422,
        "longitude": -114.0610,
        "address": "106, 110 11 Ave SE, Calgary, AB T2G 0X5",
        "status": "Limited",
        "current_needs": ["Diapers (all sizes)", "Children's books", "School snacks"],
        "hours": "24/7 for registered families",
        "contact": "403-263-8384",
        "description": "Provides emergency shelter and support services for families experiencing homelessness.",
        "icon": "👨‍👩‍👧‍👦",
        "category": "shelter"
    },
    {
        "name": "Wood's Homes - EXIT Youth Shelter",
        "type": "Youth Shelter",
        "latitude": 51.0645,
        "longitude": -114.0915,
        "address": "1234 16 Ave NW, Calgary, AB T2M 0L4",
        "status": "Open",
        "current_needs": ["Bus tickets", "New socks (all sizes)", "Healthy snacks (granola bars, fruit cups)"],
        "hours": "24/7 for youth aged 12-17",
        "contact": "403-504-7790",
        "description": "Provides emergency shelter, crisis counselling, and support services for youth aged 12-17 experiencing homelessness or at risk.",
        "icon": "🧑‍🤝‍🧑",
        "category": "shelter"
    },
    {
        "name": "Calgary Women's Emergency Shelter",
        "type": "Women's Shelter (Crisis)",
        "latitude": 51.0380,
        "longitude": -114.1150,
        "address": "Confidential Location - Contact for Information",
        "status": "Limited",
        "current_needs": ["Toiletries", "New pajamas for women & children", "Gift cards for groceries/pharmacies"],
        "hours": "24/7 Crisis Line & Intake",
        "contact": "403-290-1552 (24-Hour Family Violence Helpline)",
        "description": "Offers safe shelter, counselling, and essential support services for women and children fleeing domestic violence and abuse.",
        "icon": "🚺",
        "category": "shelter"
    },
    {
        "name": "YWCA of Calgary",
        "type": "Women's Shelter & Support",
        "latitude": 51.0478,
        "longitude": -114.0667,
        "address": "320 5 Ave SE, Calgary, AB T2G 2C4",
        "status": "Open",
        "current_needs": ["Children's clothing", "Personal hygiene items", "Phone cards"],
        "hours": "24/7 for emergency services",
        "contact": "403-263-1550",
        "description": "Provides emergency shelter, transitional housing, and support programs for women and children.",
        "icon": "🚺",
        "category": "shelter"
    },
    {
        "name": "Street Church",
        "type": "Community Support & Shelter",
        "latitude": 51.0470,
        "longitude": -114.0845,
        "address": "1020 7A St SW, Calgary, AB T2R 1A5",
        "status": "Open",
        "current_needs": ["Winter clothing", "Sleeping bags", "Food donations"],
        "hours": "Services Mon-Fri 9 AM - 5 PM; Emergency support 24/7",
        "contact": "403-244-8499",
        "description": "Community outreach providing meals, clothing, and emergency shelter support.",
        "icon": "⛪",
        "category": "shelter"
    },
    
    # Food Banks and Food Services
    {
        "name": "Calgary Food Bank",
        "type": "Food Bank",
        "latitude": 50.9986,
        "longitude": -114.0345,
        "address": "5000 11 St SE, Calgary, AB T2H 2Y5",
        "status": "Open (By Appointment)",
        "current_needs": ["Pasta & pasta sauce", "Baby formula (Stage 1 & 2)", "Peanut butter"],
        "hours": "Mon-Thu 8:30 AM - 4:30 PM, Fri 8:30 AM - 3:00 PM",
        "contact": "403-253-2055",
        "description": "Distributes emergency food hampers to individuals and families in need.",
        "icon": "🍽️",
        "category": "food"
    },
    {
        "name": "Be The Change YYC",
        "type": "Mobile Food Services",
        "latitude": 51.0497,
        "longitude": -114.0847,
        "address": "Multiple locations - Mobile service",
        "status": "Open",
        "current_needs": ["Canned goods", "Fresh produce", "Volunteer drivers"],
        "hours": "Various times throughout the week",
        "contact": "403-708-8451",
        "description": "Mobile food hamper delivery and community support services.",
        "icon": "🚚",
        "category": "food"
    },
    {
        "name": "Bowness Community Food Bank",
        "type": "Community Food Bank",
        "latitude": 51.0897,
        "longitude": -114.2144,
        "address": "7904 43 Ave NW, Calgary, AB T3B 1R2",
        "status": "Open",
        "current_needs": ["Non-perishable items", "Baby food", "Personal care items"],
        "hours": "Tue & Thu 1 PM - 3 PM, Sat 10 AM - 12 PM",
        "contact": "403-288-0477",
        "description": "Community-based food bank serving the Bowness area and surrounding communities.",
        "icon": "🥫",
        "category": "food"
    },
    {
        "name": "Forest Lawn Community Food Bank",
        "type": "Community Food Bank",
        "latitude": 51.0397,
        "longitude": -113.9600,
        "address": "1520 8 Ave SE, Calgary, AB T2G 0M4",
        "status": "Open",
        "current_needs": ["Rice & beans", "Cooking oil", "Children's snacks"],
        "hours": "Mon, Wed, Fri 10 AM - 2 PM",
        "contact": "403-272-3663",
        "description": "Serves the Forest Lawn community with emergency food assistance and support programs.",
        "icon": "🥫",
        "category": "food"
    },
    
    # Health Services
    {
        "name": "CUPS Calgary - Health Clinic",
        "type": "Health Services",
        "latitude": 51.0430,
        "longitude": -114.0830,
        "address": "1001 10 Ave SW, Calgary, AB T2R 0B7",
        "status": "Open",
        "current_needs": ["Over-the-counter pain relievers", "Band-aids", "Hand sanitizer"],
        "hours": "Mon-Fri 9 AM - 4 PM",
        "contact": "403-221-8780",
        "description": "Provides primary healthcare, mental health support, and social services to low-income Calgarians.",
        "icon": "🏥",
        "category": "health"
    },
    {
        "name": "The Alex Community Health Centre",
        "type": "Community Health Centre",
        "latitude": 51.0356,
        "longitude": -114.0798,
        "address": "1338 4 St SE, Calgary, AB T2G 2T1",
        "status": "Open",
        "current_needs": ["Medical supplies", "Reading glasses", "Health education materials"],
        "hours": "Mon-Fri 8:30 AM - 4:30 PM",
        "contact": "403-234-7448",
        "description": "Full-service health clinic providing medical care, mental health services, and addiction support.",
        "icon": "🏥",
        "category": "health"
    },
    {
        "name": "Sheldon M. Chumir Health Centre",
        "type": "Urgent Care & Health Services",
        "latitude": 51.0430,
        "longitude": -114.0726,
        "address": "1213 4 St SW, Calgary, AB T2R 0X7",
        "status": "Open",
        "current_needs": ["N/A - Full-service facility"],
        "hours": "24/7 Emergency & Urgent Care",
        "contact": "403-955-6200",
        "description": "24/7 urgent care and emergency services, walk-in mental health crisis support.",
        "icon": "🚑",
        "category": "health"
    },
    {
        "name": "Kensington-Hillhurst Community Health Centre",
        "type": "Community Health Centre",
        "latitude": 51.0567,
        "longitude": -114.0892,
        "address": "1527 Centre St N, Calgary, AB T2E 2S1",
        "status": "Open",
        "current_needs": ["Health education materials", "First aid supplies"],
        "hours": "Mon-Fri 8:30 AM - 4:30 PM",
        "contact": "403-944-4040",
        "description": "Public health services, immunizations, and health education programs.",
        "icon": "🏥",
        "category": "health"
    },
    
    # Mental Health Services
    {
        "name": "CMHA Calgary - Welcome Centre",
        "type": "Mental Health Support",
        "latitude": 51.0489,
        "longitude": -114.0850,
        "address": "#105, 1040 7 Ave SW, Calgary, AB T2P 3G9",
        "status": "Open",
        "current_needs": ["Journals and pens", "Art supplies for therapeutic programs", "Ground coffee & tea bags"],
        "hours": "Mon-Fri 9:00 AM - 4:30 PM",
        "contact": "403-297-1700",
        "description": "Recovery-focused programs, peer support, counselling, and mental health resources.",
        "icon": "🧠",
        "category": "mental_health"
    },
    {
        "name": "Access Mental Health - Walk-in Clinic",
        "type": "Mental Health Crisis Support",
        "latitude": 51.0445,
        "longitude": -114.0612,
        "address": "1240 Kensington Rd NW, Calgary, AB T2N 3P7",
        "status": "Open",
        "current_needs": ["Mental health resources", "Comfort items"],
        "hours": "Mon-Fri 8 AM - 8 PM, Weekends 10 AM - 6 PM",
        "contact": "403-943-1500",
        "description": "Walk-in mental health services, crisis intervention, and counselling support.",
        "icon": "🧠",
        "category": "mental_health"
    },
    {
        "name": "Calgary Counselling Centre",
        "type": "Counselling Services",
        "latitude": 51.0390,
        "longitude": -114.0950,
        "address": "1000 8 Ave SW, Calgary, AB T2P 3M7",
        "status": "Open",
        "current_needs": ["Counselling materials", "Stress relief items"],
        "hours": "Mon-Fri 8:30 AM - 8:30 PM, Sat 9 AM - 4 PM",
        "contact": "403-691-5991",
        "description": "Individual, family, and group counselling services with sliding fee scale options.",
        "icon": "💭",
        "category": "mental_health"
    },
    
    # Resource Hubs and Support Services
    {
        "name": "SORCe (Safe Communities Opportunity and Resource Centre)",
        "type": "Resource Hub",
        "latitude": 51.0478,
        "longitude": -114.0580,
        "address": "316 7 Ave SE, Calgary, AB T2G 0J2",
        "status": "Open",
        "current_needs": ["Bus tickets", "Reusable water bottles"],
        "hours": "Mon-Fri 8:30 AM - 4:30 PM",
        "contact": "Service specific, general info via 211",
        "description": "Multi-agency collaborative offering access to various programs and services for individuals and families at risk of or experiencing homelessness.",
        "icon": "🏢",
        "category": "resources"
    },
    {
        "name": "Prospect Human Services - Main Office",
        "type": "Employment Services",
        "latitude": 51.0585,
        "longitude": -113.9700,
        "address": "915 33 St NE #1, Calgary, AB T2A 6T2",
        "status": "Open (By Appointment)",
        "current_needs": ["Professional attire donations", "Bus tickets for interviews", "Laptop/tablet donations"],
        "hours": "Mon-Fri 8:30 AM - 4:30 PM",
        "contact": "403-273-2822",
        "description": "Employment training, job search assistance, and career development services for diverse Calgarians.",
        "icon": "💼",
        "category": "employment"
    },
    {
        "name": "Calgary Public Library - Central Library",
        "type": "Public Resources & Support",
        "latitude": 51.0456,
        "longitude": -114.0562,
        "address": "800 3 St SE, Calgary, AB T2G 0E7",
        "status": "Open",
        "current_needs": ["Computer time donations", "Learning materials"],
        "hours": "Mon-Thu 9 AM - 8 PM, Fri-Sat 9 AM - 5 PM, Sun 12 PM - 5 PM",
        "contact": "403-260-2600",
        "description": "Free computer access, job search resources, social services information, and community programs.",
        "icon": "📚",
        "category": "resources"
    },
    {
        "name": "Bow Valley College - Upgrading & Preparation",
        "type": "Education & Training",
        "latitude": 51.0494,
        "longitude": -114.0581,
        "address": "332 6 Ave SE, Calgary, AB T2G 4S6",
        "status": "Open",
        "current_needs": ["School supplies", "Technology equipment", "Learning resources"],
        "hours": "Mon-Fri 8 AM - 4:30 PM",
        "contact": "403-410-1400",
        "description": "Adult education, job training, and skills development programs.",
        "icon": "🎓",
        "category": "education"
    },
    
    # Additional Community Services
    {
        "name": "Salvation Army - Centre of Hope",
        "type": "Multi-Service Centre",
        "latitude": 51.0445,
        "longitude": -114.0485,
        "address": "420 9 Ave SE, Calgary, AB T2G 0V1",
        "status": "Open",
        "current_needs": ["Clothing donations", "Household items", "Food donations"],
        "hours": "Mon-Fri 8:30 AM - 4:30 PM",
        "contact": "403-410-1111",
        "description": "Emergency services, food programs, clothing bank, and transitional housing support.",
        "icon": "⭐",
        "category": "resources"
    },
    {
        "name": "United Way of Calgary - Resource Centre",
        "type": "Community Information Hub",
        "latitude": 51.0467,
        "longitude": -114.0789,
        "address": "1202 Centre St SE, Calgary, AB T2G 5A5",
        "status": "Open",
        "current_needs": ["Community program information", "Volunteer coordination"],
        "hours": "Mon-Fri 8:30 AM - 4:30 PM",
        "contact": "403-231-6265",
        "description": "Community resource information, program coordination, and volunteer matching services.",
        "icon": "🤝",
        "category": "resources"
    },
    {
        "name": "Calgary Legal Guidance",
        "type": "Legal Aid Services",
        "latitude": 51.0445,
        "longitude": -114.0720,
        "address": "840 7 Ave SW, Calgary, AB T2P 3G2",
        "status": "Open",
        "current_needs": ["Legal resource materials", "Office supplies"],
        "hours": "Mon-Fri 9 AM - 4 PM",
        "contact": "403-234-9266",
        "description": "Free legal services for low-income individuals including housing, employment, and family law.",
        "icon": "⚖️",
        "category": "legal"
    }
]

# Convert to DataFrame
df_locations = pd.DataFrame(locations_data)

def get_marker_color(status):
    """Determine marker color based on status"""
    status_lower = status.lower()
    if 'open' in status_lower and 'appointment' not in status_lower:
        return '#2E8B57'  # Sea Green
    elif 'limited' in status_lower or 'appointment' in status_lower:
        return '#FF8C00'  # Dark Orange
    else:
        return '#DC143C'  # Crimson

def create_enhanced_map():
    """Create an enhanced Folium map with better styling and markers"""
    # Center the map on Calgary
    m = folium.Map(
        location=[51.0447, -114.0719],
        zoom_start=11,
        tiles=None
    )
    
    # Add bright, clear tile layers
    folium.TileLayer(
        'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attr='© OpenStreetMap contributors',
        name='Street Map',
        overlay=False,
        control=True
    ).add_to(m)
    
    folium.TileLayer(
        'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
        attr='© CartoDB © OpenStreetMap contributors',
        name='Light Map',
        overlay=False,
        control=True
    ).add_to(m)
    
    folium.TileLayer(
        'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
        attr='© OpenStreetMap contributors, Tiles style by Humanitarian OpenStreetMap Team',
        name='Humanitarian Map',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Create marker clusters by category for better organization
    shelter_cluster = plugins.MarkerCluster(name="Shelters & Housing").add_to(m)
    food_cluster = plugins.MarkerCluster(name="Food Services").add_to(m)
    health_cluster = plugins.MarkerCluster(name="Health Services").add_to(m)
    mental_health_cluster = plugins.MarkerCluster(name="Mental Health").add_to(m)
    resource_cluster = plugins.MarkerCluster(name="Community Resources").add_to(m)
    
    # Map categories to clusters
    category_clusters = {
        'shelter': shelter_cluster,
        'food': food_cluster,
        'health': health_cluster,
        'mental_health': mental_health_cluster,
        'resources': resource_cluster,
        'employment': resource_cluster,
        'education': resource_cluster,
        'legal': resource_cluster
    }
    
    # Add markers for each location
    for idx, location in df_locations.iterrows():
        marker_color = get_marker_color(location['status'])
        
        # Create comprehensive popup content
        popup_html = f"""
        <div style="width: 350px; font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.4;">
            <div style="background: linear-gradient(135deg, {marker_color}, {marker_color}dd); color: white; padding: 15px; margin: -10px -10px 15px -10px; border-radius: 8px 8px 0 0;">
                <h3 style="margin: 0; font-size: 18px;">{location['icon']} {location['name']}</h3>
                <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 14px;">{location['type']}</p>
            </div>
            
            <div style="padding: 0 5px;">
                <div style="margin-bottom: 12px;">
                    <strong style="color: #333;">Status:</strong> 
                    <span style="color: {marker_color}; font-weight: bold; background: {marker_color}22; padding: 3px 8px; border-radius: 12px; font-size: 12px;">{location['status']}</span>
                </div>
                
                <div style="margin-bottom: 10px;">
                    <strong style="color: #333;">📍 Address:</strong><br>
                    <span style="color: #666; font-size: 13px;">{location['address']}</span>
                </div>
                
                <div style="margin-bottom: 10px;">
                    <strong style="color: #333;">🕒 Hours:</strong><br>
                    <span style="color: #666; font-size: 13px;">{location['hours']}</span>
                </div>
                
                <div style="margin-bottom: 10px;">
                    <strong style="color: #333;">📞 Contact:</strong><br>
                    <span style="color: #666; font-size: 13px;">{location['contact']}</span>
                </div>
                
                <div style="margin-bottom: 12px;">
                    <strong style="color: #333;">📋 Description:</strong><br>
                    <span style="color: #666; font-size: 12px;">{location['description']}</span>
                </div>
                
                <div>
                    <strong style="color: #333;">🎯 Current Needs:</strong>
                    <ul style="margin: 5px 0; padding-left: 18px; color: #666; font-size: 12px;">
        """
        
        for need in location['current_needs']:
            popup_html += f"<li style='margin: 2px 0;'>{need}</li>"
        
        popup_html += """
                    </ul>
                </div>
            </div>
        </div>
        """
        
        # Determine which cluster to add the marker to
        cluster = category_clusters.get(location['category'], resource_cluster)
        
        # Create custom marker with house-like icon
        marker_html = f"""
        <div style="
            background: {marker_color};
            border: 4px solid white;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            position: relative;
        ">
            {location['icon']}
        </div>
        """
        
        folium.Marker(
            location=[location['latitude'], location['longitude']],
            popup=folium.Popup(popup_html, max_width=370),
            tooltip=f"🏠 {location['name']} - {location['type']} ({location['status']})",
            icon=folium.DivIcon(
                html=marker_html,
                icon_size=(50, 50),
                icon_anchor=(25, 25)
            )
        ).add_to(cluster)
    
    # Add layer control
    folium.LayerControl(position='topright').add_to(m)
    
    # Add fullscreen button
    plugins.Fullscreen(position='topleft').add_to(m)

    
    return m

# --- Page Title and Introduction ---
st.title("📍 Beacon Calgary: Community Support Network")
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
    <h3 style="margin: 0 0 10px 0;">Welcome to Beacon Calgary</h3>
    <p style="margin: 0; opacity: 0.9;">Your comprehensive guide to support services in Calgary. Find shelters, food banks, health clinics, mental health support, and community resources. Use our interactive map and chat with our AI assistant for personalized help.</p>
</div>
""", unsafe_allow_html=True)

# Quick Stats Dashboard
col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
with col_stats1:
    st.metric("🏠 Shelters", len(df_locations[df_locations['category'] == 'shelter']))
with col_stats2:
    st.metric("🍽️ Food Services", len(df_locations[df_locations['category'] == 'food']))
with col_stats3:
    st.metric("🏥 Health Services", len(df_locations[df_locations['category'] == 'health']))
with col_stats4:
    st.metric("🧠 Mental Health", len(df_locations[df_locations['category'] == 'mental_health']))

# Service Filter
st.sidebar.header("🔍 Filter Services")
category_filter = st.sidebar.multiselect(
    "Select service categories:",
    options=['shelter', 'food', 'health', 'mental_health', 'resources', 'employment', 'education', 'legal'],
    default=['shelter', 'food', 'health', 'mental_health'],
    format_func=lambda x: {
        'shelter': '🏠 Shelters & Housing',
        'food': '🍽️ Food Services',
        'health': '🏥 Health Services',
        'mental_health': '🧠 Mental Health',
        'resources': '🏢 Community Resources',
        'employment': '💼 Employment Services',
        'education': '🎓 Education & Training',
        'legal': '⚖️ Legal Services'
    }.get(x, x)
)

status_filter = st.sidebar.selectbox(
    "Filter by availability:",
    options=['All', 'Open', 'Limited', 'By Appointment'],
    index=0
)

# Filter dataframe based on selections
filtered_df = df_locations.copy()
if category_filter:
    filtered_df = filtered_df[filtered_df['category'].isin(category_filter)]

if status_filter != 'All':
    if status_filter == 'Open':
        filtered_df = filtered_df[filtered_df['status'].str.contains('Open', na=False)]
    elif status_filter == 'Limited':
        filtered_df = filtered_df[filtered_df['status'].str.contains('Limited', na=False)]
    elif status_filter == 'By Appointment':
        filtered_df = filtered_df[filtered_df['status'].str.contains('Appointment', na=False)]

st.markdown("---")

# --- Main Content: Enhanced Map and Location Details ---
col1, col2 = st.columns([2.5, 1.5])

with col1:
    st.subheader("🗺️ Interactive Service Map")
    st.markdown("*Use the map controls to switch between different map styles, zoom, and get detailed information by clicking on markers.*")
    
    # Create and display the enhanced map
    map_obj = create_enhanced_map()
    map_data = st_folium(map_obj, width=700, height=500, returned_objects=["last_object_clicked"])
    
    # Display clicked location info
    if map_data['last_object_clicked']:
        clicked_tooltip = map_data['last_object_clicked'].get('tooltip', '')
        if clicked_tooltip:
            st.info(f"📍 Last clicked: {clicked_tooltip}")

with col2:
    st.subheader("ℹ️ Service Information")
    st.markdown("Select a service from the dropdown below for detailed information.")
    
    # Sort locations by name for the dropdown
    sorted_location_names = sorted(df_locations['name'].tolist())
    
    selected_location_name = st.selectbox(
        "Select a service:",
        options=sorted_location_names,
        index=0
    )

    if selected_location_name:
        location_details = df_locations[df_locations['name'] == selected_location_name].iloc[0]
        
        status_color = "green"
        if location_details['status'] == "Limited":
            status_color = "orange"
        elif location_details['status'] in ["Full", "Full/Closed", "Closed"]:
            status_color = "red"

        st.markdown(f"#### {location_details['icon']} {location_details['name']}")
        st.markdown(f"**Type:** {location_details['type']}")
        st.markdown(f"**Address:** {location_details['address']}")
        
        if location_details['name'] == "Calgary Women's Emergency Shelter":
            st.caption("_Note: For safety, the precise map location for this shelter is general. Please use the contact information for direct assistance._")
        
        st.markdown(f"**Status:** <span style='color:{status_color}; font-weight:bold;'>{location_details['status']}</span>", unsafe_allow_html=True)
        st.markdown(f"**Hours:** {location_details['hours']}")
        st.markdown(f"**Contact:** {location_details['contact']}")
        
        st.markdown("**Description:**")
        st.write(location_details['description'])

        st.markdown("**Current Needs:**")
        if isinstance(location_details['current_needs'], list) and location_details['current_needs']:
            for item in location_details['current_needs']:
                st.markdown(f"- {item}")
        else:
            st.markdown("- *No specific needs listed at this moment.*")
        
        

st.markdown("---")

# --- Enhanced Chatbot Section ---
st.header("💬 Chat with Beacon Bot")

if api_key_input:
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key_input
            )
    except Exception as e:
        st.error(f"Failed to initialize OpenAI client: {e}")
        client = None
else:
    st.warning("OpenAI API Key not found in environment variables. Please ensure it is set in your .env file for the chatbot to function.")
    client = None

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Enhanced system prompt
SYSTEM_PROMPT = f"""
You are 'Beacon Bot', a compassionate and helpful AI assistant for the 'Beacon Calgary' app. 
Your goal is to provide information about resources for those experiencing homelessness or seeking to help in Calgary.

The app lists the following services with their current status:
{chr(10).join([f"- {loc['name']} ({loc['type']}) - Status: {loc['status']}" for loc in locations_data])}

Guidelines:
- Answer general questions about homelessness, types of services available
- Provide emotional support and encouragement
- For specific availability or urgent needs, direct users to check the interactive map or contact services directly
- Be kind, respectful, and focus on actionable information
- Don't make up information - state when you don't have specific details
- Mention relevant services from the app when appropriate
- For directions, provide addresses that users can input into navigation apps

Remember: You're here to help connect people with the resources they need in Calgary.
"""

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask Beacon Bot a question..."):
    if not client:
        st.error("OpenAI client not initialized. Please ensure your API key is correctly set in the .env file.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            try:
                api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + \
                               [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

                completion = client.chat.completions.create(
                    model="google/gemma-3-1b-it:free", 
                    messages=api_messages,
                    stream=True
                )
                for chunk in completion:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            except Exception as e:
                full_response = f"Sorry, I encountered an error: {e}"
                message_placeholder.markdown(full_response)
            
        st.session_state.messages.append({"role": "assistant", "content": full_response})

elif not st.session_state.messages and client: 
    with st.chat_message("assistant"):
        initial_greeting = "Hello! I'm Beacon Bot. How can I help you find information about support services in Calgary today?"
        st.markdown(initial_greeting)
    if not any(msg['role'] == 'assistant' and msg['content'] == initial_greeting for msg in st.session_state.messages):
        st.session_state.messages.append({"role": "assistant", "content": initial_greeting})

# Footer
st.markdown("---")
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    <p>Beacon Calgary - Connecting Community Resources</p>
    <p>For emergency situations, please call 911 | For crisis support, call 211</p>
</div>
""", unsafe_allow_html=True)