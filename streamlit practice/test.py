import streamlit as st
import numpy as np
import pandas as pd
import time

# cache this really slow function to speedup runtime on method calls with same arguments 
@st.cache
def slowFunction(arg1, arg2, arg3):
   time.sleep(10)
   return int(arg1) * int(arg2) * int(arg3)

if __name__ == "__main__":
    st.title('Data Visualization')

    st.write("First attmept at visualizing data")
    if st.checkbox('Show DataFrame'):
        df = pd.DataFrame({
        'first column': [1, 2, 3, 4],
        'second column': [10, 20, 30, 40]
        })
        st.write(df)
        st.line_chart(df)

        option = st.sidebar.selectbox(
            "Favorite number?", df["first column"])

        "You selected: ", option


    # latest_iteration = st.empty()
    # bar = st.progress(0)
    # for i in range(100):
    #     # Update the progress bar with each iteration.
    #     latest_iteration.text(f'Iteration {i+1}')
    #     bar.progress(i + 1)
    #     time.sleep(0.1)
    # '...and now we\'re done!'
    nums = []
    nums.append(st.sidebar.slider("Select a number 1-10", 1, 10, 1, 1))
    nums.append(st.sidebar.slider("Select second number 1-10", 1, 10, 1, 1))
    nums.append(st.sidebar.slider("Select thrid number 1-10", 1, 10, 1, 1))
    
    # sort the numbers so that number combinations can be cached easier since function uses multiplication, which is commutative
    nums.sort()

    st.write(slowFunction(nums[0], nums[1], nums[2]))