import streamlit as st

def main():
    st.set_page_config(page_title="Credits & References", layout="wide")
    st.title("Credits & References")

    st.markdown("""
    **Credits**:  
    Below are links and resources referenced or consulted while building 
    this project on the Vietnam War, its weaponry, herbicides, and bombing data.
    """)

    st.write("---")

    st.markdown("""
    - [Vietnam War Overview](https://en.wikipedia.org/wiki/Vietnam_War)  
    - [Kaggle Dataset](https://www.kaggle.com/datasets/usaf/vietnam-war-bombing-operations?resource=download)
    - [Kaggle Code](https://www.kaggle.com/code/linhvit/vietnam-war)
    - [Topographical Map](https://www.reddit.com/r/MapPorn/comments/lg0nz7/the_topography_of_vietnam/)
    - [Herbicide Research Documents](https://www.ncbi.nlm.nih.gov/books/NBK209597/)
    - [Guns](https://en.wikipedia.org/wiki/D-74_122_mm_field_gun)
    - [Weapons](https://www.history.com/topics/vietnam-war/weapons-of-the-vietnam-war)
    - [More Weapons](https://www.pritzkermilitary.org/explore/vietnam-war/vietnam-equipment)
    - [Bombing Data](https://data.world/datamil/)              
    """)

if __name__ == "__main__":
    main()
