import streamlit as st
import pandas as pd

# Load and preprocess data
# Load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv('data.csv')  # Update with your actual file path
    
    # Handle missing values for beds
    df['min_beds'] = df['min_beds'].fillna(0)
    df['max_beds'] = df['max_beds'].fillna(df['min_beds'].max())
    
    # Handle amenities formatting
    df['amenities'] = df['amenities'].fillna('')  # Handle NaN values
    df['amenities'] = df['amenities'].str.split(', ')
    
    return df

df = load_data()


# Sidebar filters
st.sidebar.header('Filters')

# Price range filter
min_price = int(df['min_price'].min())
max_price = int(df['max_price'].max())
price_range = st.sidebar.slider(
    'Price Range ($)',
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price)
)

# Bed range filter
min_bed = int(df['min_beds'].min())
max_bed = int(df['max_beds'].max())
bed_range = st.sidebar.slider(
    'Number of Bedrooms',
    min_value=min_bed,
    max_value=max_bed,
    value=(min_bed, max_bed)
)

# Amenities filter
all_amenities = sorted({amenity for sublist in df['amenities'] for amenity in sublist})
selected_amenities = st.sidebar.multiselect('Amenities', all_amenities)

# Availability filter
available_only = st.sidebar.checkbox('Show available properties only', value=True)

# Filter data
filtered_df = df[
    (df['min_price'] <= price_range[1]) & 
    (df['max_price'] >= price_range[0]) &
    (df['min_beds'] <= bed_range[1]) & 
    (df['max_beds'] >= bed_range[0])
]

if selected_amenities:
    filtered_df = filtered_df[filtered_df['amenities'].apply(
        lambda x: all(amenity in x for amenity in selected_amenities)
    )]

if available_only:
    filtered_df = filtered_df[filtered_df['available'] == True]

# Display metrics
st.header('🏠 Property Rental Dashboard')
col1, col2, col3 = st.columns(3)
col1.metric("Total Properties", len(filtered_df))
col2.metric("Average Min Price", f"${filtered_df['min_price'].mean():.0f}")
col3.metric("Average Max Price", f"${filtered_df['max_price'].mean():.0f}")

# Display properties
def format_phone(phone):
    phone_str = str(int(phone))
    return f"({phone_str[:3]}) {phone_str[3:6]}-{phone_str[6:]}"

for index, row in filtered_df.iterrows():
    st.markdown("---")
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image(row['main_image'], use_container_width=True)
    
    with col2:
        st.subheader(row['name'])
        st.write(f"**Address:** {row['address']}")
        st.write(f"**Price Range:** ${row['min_price']} - ${row['max_price']}")
        st.write(f"**Bedrooms:** {row['min_beds']} - {row['max_beds']}")
        st.write(f"**Amenities:** {', '.join(row['amenities'])}")
        st.write(f"**Contact:** {format_phone(row['contact_phone'])}")
        st.markdown(f"[Visit Property Website]({row['url']})")