@st.cache_data
def load_data():
    # Try different encodings until one works
    encodings = ['utf-8', 'latin-1', 'cp1252', 'utf-16']
    df = None
    
    for enc in encodings:
        try:
            df = pd.read_csv('data.csv', encoding=enc)
            break # If it works, stop looking
        except (UnicodeDecodeError, Exception):
            continue
            
    if df is None:
        st.error("Could not read the CSV file. Please check the file format.")
        return pd.DataFrame()

    # Column mapping (Make sure these match your CSV columns)
    cols = ['ID', 'Stock_Name', 'Price', 'PE', 'MarketCap', 'DivYield', 
            'NP_Qtr', 'Profit_Var', 'ROCE', 'ROE', 'Sales_Var', 'D_E', 'P_B', 'Reserves']
    
    # If your CSV has no header row, use this:
    if len(df.columns) == len(cols):
        df.columns = cols
    else:
        # This handles cases where the CSV might have extra/fewer columns
        df = pd.read_csv('data.csv', encoding=enc, names=cols, header=None)
        
    return df
