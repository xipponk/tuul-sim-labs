import streamlit as st
import numpy as np

# ----- Function Definitions -----
def generate_data(rows, cols):
    return np.random.randint(0, 2, size=(rows, cols))

def compute_parity(data, mode="even"):
    row_sum = np.sum(data, axis=1)
    col_sum = np.sum(data, axis=0)
    if mode == "even":
        row_parity = row_sum % 2
        col_parity = col_sum % 2
        overall = row_parity.sum() % 2
    else:  # odd parity
        row_parity = (row_sum + 1) % 2
        col_parity = (col_sum + 1) % 2
        overall = (row_parity.sum() + 1) % 2
    return row_parity, col_parity, overall

def add_error(data):
    r = np.random.randint(0, data.shape[0])
    c = np.random.randint(0, data.shape[1])
    data[r][c] ^= 1
    return r, c

def detect_error(data, row_parity_ref, col_parity_ref, mode):
    r_sum = np.sum(data, axis=1)
    c_sum = np.sum(data, axis=0)
    if mode == "even":
        row_check = r_sum % 2
        col_check = c_sum % 2
    else:
        row_check = (r_sum + 1) % 2
        col_check = (c_sum + 1) % 2

    row_diff = row_check != row_parity_ref
    col_diff = col_check != col_parity_ref

    err_row = np.where(row_diff)[0]
    err_col = np.where(col_diff)[0]

    if len(err_row) == 1 and len(err_col) == 1:
        return err_row[0], err_col[0]
    return None, None

def show_matrix_with_parity(data, row_p, col_p, overall, error_pos=None):
    html = "<table style='border-collapse: collapse;'>"
    for i in range(data.shape[0] + 1):
        html += "<tr>"
        for j in range(data.shape[1] + 1):
            if i < data.shape[0] and j < data.shape[1]:
                val = data[i][j]
                color = "#ffcccc" if error_pos == (i, j) else "#ffffff"
            elif i == data.shape[0] and j < data.shape[1]:
                val = col_p[j]
                color = "#add8e6"  # light blue
            elif j == data.shape[1] and i < data.shape[0]:
                val = row_p[i]
                color = "#faa"  # light red
            else:
                val = overall
                color = "#dddddd"

            html += f"<td style='border: 1px solid black; padding: 6px; width:30px; height:30px; background-color:{color}; color: black; text-align:center; font-weight:bold;'>{val}</td>"
        html += "</tr>"
    html += "</table>"
    return html

# ----- Streamlit UI -----
st.title("🧮 2D Parity Bit Demo")

rows = st.slider("Number of data rows", 3, 10, 4)
cols = st.slider("Number of data columns", 3, 10, 5)
parity_mode = st.radio("Select Parity Mode:", ["even", "odd"], horizontal=True)

if 'data' not in st.session_state:
    st.session_state.data = generate_data(rows, cols)
    st.session_state.error_pos = None
    st.session_state.row_p, st.session_state.col_p, st.session_state.overall = compute_parity(st.session_state.data, parity_mode)

if st.button("🔁 Generate New Data"):
    st.session_state.data = generate_data(rows, cols)
    st.session_state.row_p, st.session_state.col_p, st.session_state.overall = compute_parity(st.session_state.data, parity_mode)
    st.session_state.error_pos = None

st.subheader("Original Data with Parity")
st.markdown(show_matrix_with_parity(st.session_state.data, st.session_state.row_p, st.session_state.col_p, st.session_state.overall), unsafe_allow_html=True)

if st.button("💥 Introduce Random Error"):
    r, c = add_error(st.session_state.data)
    st.session_state.error_pos = (r, c)

if st.button("🔍 Detect Error"):
    r, c = detect_error(st.session_state.data, st.session_state.row_p, st.session_state.col_p, parity_mode)
    if r is not None:
        st.success(f"✅ Error detected and can be corrected at (row {r}, col {c})")
        st.session_state.error_pos = (r, c)
    else:
        st.info("✅ No error detected")

st.subheader("Data With Parity Check")
st.markdown(show_matrix_with_parity(st.session_state.data, st.session_state.row_p, st.session_state.col_p, st.session_state.overall, error_pos=st.session_state.error_pos), unsafe_allow_html=True)