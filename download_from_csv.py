import os
import pandas as pd
import gdown 

# ------------------
# CONFIG
# -------------------
CSV_FILE="ques_list_ju_a_unit.csv"
URL_COLUMN="url"
NAME_COLUMN="file_name"
OUTPUT_FOLDER="downloads"

def extract_file_id(url: str):
    """Extract Google Drive file ID from any supported URL."""
    try:
        if "id=" in url:
            # Format: https://drive.google.com/open?id=FILE_ID 
            # ---- This takes the 2nd element after first split (split by, "id=")
            # ---- And the second 
            return url.split("id=")[1].split("&")[0]
        elif "/file/d/" in url:
            # Format: https://drive.google.com/file/d/FILE_ID/view?usp=sharing
            return url.split("/file/d/")[1].split("/")[0]
        elif "drive.google.com" in url and "=" in url:
            # Fallback: last = part
            return url.split("=")[-1]
    except:
        return None
    
    return None

def main():
    # Create download folder if missing 
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    print(f"📄 Reading CSV: {CSV_FILE}")
    df = pd.read_csv(CSV_FILE)
    
    #Check columns
    if URL_COLUMN not in df.columns:
        print(f"❌ ERROR: CSV missing '{URL_COLUMN}' column")
        return
        
    if NAME_COLUMN not in df.columns:
        print(f"❌ ERROR: CSV missing '{NAME_COLUMN}' column")
        return 
    
    print(f"🔗 Found {len(df)} rows")
    
    for idx, row in df.iterrows():
        url = str(row[URL_COLUMN]).strip()
        file_name = str(row[NAME_COLUMN]).strip()
        
        print("url--",url)
        print("file--",file_name)
        
        if not url or not file_name:
            print(f"⚠️ Skipping empty row #{idx}")
            continue
        
        file_id = extract_file_id(url)
        
        if not file_id:
            print(f"❌ Could not extract file ID from URL: {url}")
            continue
        
        # Ensure file ends with .pdf
        if not file_name.lower().endswith(".pdf"):
            file_name += ".pdf"
            
        save_path = os.path.join(OUTPUT_FOLDER, file_name)
        
        if os.path.exists(save_path):
            print(f"⏭️ Already downloaded: {file_name}")
            continue
        
        print(f"⬇️ Downloading: {file_name}")
        
        # gdown download
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

        try:
            gdown.download(download_url, save_path, quiet=False)
            print(f"✅ Saved: {save_path}\n")
        except Exception as e:
            print(f"❌ Failed to download {file_name}: {e}\n")
            
    print("🎉 DONE — All files processed!")


if __name__ == "__main__":
    main()