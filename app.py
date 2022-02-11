import pandas as pd
import numpy as np
import PIL.Image, json, random
from pathlib import Path
import streamlit as st

# Set the page layout
st.set_page_config(page_title="OutfitGen Demo Application", layout = "wide", initial_sidebar_state = "collapsed")
with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
# Show the logo on top
st.image(PIL.Image.open("./logo.png"))

# Get all the image file names
fs = [x for x in list(Path("./images/").glob("**/*")) if x.is_file()]

# Read the config file
config = json.loads(Path("./config.json").read_text())

# Create elements you will need for session state
if "p2" not in st.session_state:
    st.session_state["p2"] = True
if "p3" not in st.session_state:
    st.session_state["p3"] = False
if "occasion" not in st.session_state:
    st.session_state["occasion"] = ["Casual", "Brunch"]
if "category" not in st.session_state:
    st.session_state["category"] = ["Dress", "Bags"]



# Select which view you want to toggle to
cols = st.columns([15, 10, 5, 10, 5])

if cols[1].button("Build your own outfit", key = "page2"):
    st.session_state["p2"] = True
    st.session_state["p3"] = False

if cols[3].button("Recreate the look", key = "page3"):
    st.session_state["p2"] = False
    st.session_state["p3"] = True



# Render Page 2
if st.session_state["p2"]:
    st.markdown("## Outfit Builder")
    lhs, rhs1, rhs2 = st.columns([5, 15, 15])

    # Show the selected categories and tags on the LHS
    lhs.markdown("**Occasions Selected**")
    for o in config["occasion"]:
        v = False
        if o in st.session_state["occasion"]: v = True
        lhs.checkbox(o, value = v)

    lhs.markdown("**Categories Selected**")
    category_checkboxes = []
    for c in config["category"]:
        v = False
        if c in st.session_state["category"]: v = True
        cbx = lhs.checkbox(c, value = v)
        category_checkboxes.append(cbx)
    
    render_categories = []
    for name, cat in zip(config['category'], category_checkboxes):
        if cat:
            render_categories.append(name)

    render_categories = sorted(list(set(render_categories)))

    
    # Create RHS side boxes
    for c in render_categories[:2]:
        rhs1.file_uploader(f"Upload {c} of your choice")
        expander = rhs1.expander(f" Expand to see more {c} suggestions")
        valid_im_files = [x for x in fs if x.parent.name == c]
        with expander:
            img_cnt = st.select_slider("Select Image", options = range(len(valid_im_files)), key = c)
            imgs = []
            for x in fs:
                if x.parent.name == c:
                    imgs.append(PIL.Image.open(x).resize((200,200)))
            dst = PIL.Image.new('RGB', (600, 200))
            dst.paste(imgs[0], (0, 0))
            dst.paste(imgs[1], (200, 0))
            dst.paste(imgs[2], (400, 0))
            st.image(dst)   
        
        # Display the nth index of the respective category
        im_file = valid_im_files[img_cnt]
        rhs1.image(PIL.Image.open(im_file).resize((200,200)))
    
    # Create RHS side boxes
    if len(render_categories) > 2:
        for c in render_categories[2:]:
            rhs2.file_uploader(f"Upload {c} of your choice")
            expander = rhs2.expander(f" Expand to see more {c} suggestions")
            valid_im_files = [x for x in fs if x.parent.name == c]
            with expander:
                img_cnt = st.select_slider("Select Image", options = range(len(valid_im_files)), key = c)
                imgs = []
                for x in fs:
                    if x.parent.name == c:
                        imgs.append(PIL.Image.open(x).resize((200,200)))
                dst = PIL.Image.new('RGB', (600, 200))
                dst.paste(imgs[0], (0, 0))
                dst.paste(imgs[1], (200, 0))
                dst.paste(imgs[2], (400, 0))
                st.image(dst)   
            
            # Display the nth index of the respective category
            im_file = valid_im_files[img_cnt]
            rhs2.image(PIL.Image.open(im_file).resize((200,200)))
    

# Render Page 3
if st.session_state["p3"]:
    st.markdown("## Recreate the look")
    lhs, rhs1, rhs2 = st.columns([10, 15, 15])

    # Show the selected categories and tags on the LHS
    with lhs:
        link = st.text_input("Paste a link")
        st.markdown("**OR**")
        link = st.text_input("Select from Instagram")
        st.markdown("**OR**")
        uploader = st.file_uploader("Upload from your computer")
    
    with rhs1:
        if uploader is not None:
            st.image(PIL.Image.open(uploader).resize((250,250)))

            st.markdown("**Categories Detected**")
            category_checkboxes = []
            for c in config["category"]:
                v = False
                if c in ["Dress", "Shoes"]:
                    v = True
                    
                cbx = st.checkbox(c, value = v)
                category_checkboxes.append(cbx)
            
            if len(category_checkboxes) == 0:
                category_checkboxes = [""]

    with rhs2:
        if uploader is not None:
            render_categories = []
            for name, cat in zip(config['category'], category_checkboxes):
                if cat:
                    render_categories.append(name)

            render_categories = sorted(list(set(render_categories)))

            # Create RHS side boxes
            for c in render_categories:
                valid_im_files = [x for x in fs if x.parent.name == c]
                
                expander = st.expander(f" Expand to see more {c} suggestions")
                with expander:
                    img_cnt = st.select_slider("Select Image", options = range(len(valid_im_files)), key = c)
                    imgs = []
                    for x in valid_im_files:
                        if x.parent.name == c:
                            imgs.append(PIL.Image.open(x).resize((200,200)))
                    dst = PIL.Image.new('RGB', (600, 200))
                    dst.paste(imgs[0], (0, 0))
                    dst.paste(imgs[1], (200, 0))
                    dst.paste(imgs[2], (400, 0))
                    st.image(dst)  

                # Display the nth index of the respective category
                im_file = [x for x in fs if x.parent.name == c][img_cnt]
                st.image(PIL.Image.open(im_file).resize((200,200)))
                
                 

