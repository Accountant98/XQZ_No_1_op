import streamlit as st
import pandas as pd
from streamlit_extras.grid import grid
from read_data_view import *
from user_read_only import view
from update_file import get_csrf_token, update_file_into_server, update_file_after_edit
from create_cadics import create_cadics
from create_document_step2 import create_doc


def reset_data():
    if st.session_state.get('data') is None:
        st.session_state['data'] = {}


def set_data(key: str, value):
    st.session_state['data'][key] = value


def get_data(key):
    return st.session_state['data'].get(key)


def admin():
    reset_data()
    csrf_token = get_csrf_token()
    col_left, col_right = st.columns([1, 3])
    with col_left:
        with st.form('input_form'):
            # PROJECT BOX
            col_left_prj_grid = grid(1, 2, 2, 2, vertical_align="top")
            # Row 1:
            col_left_prj_grid.header("Project")
            # Row 2:
            col_left_prj_grid.text_input("Model Code", key="code")
            col_left_prj_grid.selectbox("PowerTrain", ['EV', 'e-Power', 'ICE'], key="pwt")
            # Row 3:
            col_left_prj_grid.selectbox("Case", ['CASE1', 'CASE1.5', 'CASE2'], key="case")
            col_left_prj_grid.selectbox("Plant", ['JPN', 'US', 'EUR', 'PRC'], key="plant")
            # Row 4:
            col_left_prj_grid.selectbox("Dev", ['ALL', 'XQ4', 'XR2', 'XR3'], key="dev")
            col_left_prj_grid.selectbox("Lot", ["ALL", 'DS', 'DC', 'PFC', 'VC', 'PT1', 'PT2'], key="lot")
            st.header("Spec box")
            files = st.file_uploader("", accept_multiple_files=True)

            col_left_spec_grid = grid(2, 2, vertical_align="top")
            set_data("running", 0)
            if col_left_spec_grid.form_submit_button("View Data", use_container_width=True) and get_data(
                    "running") == 0:
                set_data("running", 1)
                list_file, folder_output, name_zip = check_file_out(st.session_state.code, st.session_state.pwt,
                                                                    st.session_state.plant, st.session_state.case)
                set_state(list_file, folder_output, name_zip)
                set_data("running", 0)

            if files is not None and col_left_spec_grid.form_submit_button("Load File",
                                                                           use_container_width=True) and get_data(
                "running") == 0:
                set_data("running", 1)
                update_file_into_server(st.session_state.code, files, csrf_token)
                set_data("running", 0)

            if col_left_spec_grid.form_submit_button("Create Cadics", use_container_width=True) == True and get_data(
                    "running") == 0:
                set_data("running", 1)
                notice = create_cadics(st.session_state.case, st.session_state.plant, st.session_state.pwt,
                                       st.session_state.code)
                st.write(notice)
                list_file, folder_output, name_zip = check_file_out(st.session_state.code, st.session_state.pwt,
                                                                    st.session_state.plant, st.session_state.case)
                set_state(list_file, folder_output, name_zip)
                set_data("running", 0)
            if col_left_spec_grid.form_submit_button("Create Outputs", use_container_width=True) and get_data(
                    "running") == 0:
                set_data("running", 1)
                notice = create_doc(st.session_state.case, st.session_state.plant, st.session_state.pwt,
                                    st.session_state.code)
                st.write(notice)
                list_file, folder_output, name_zip = check_file_out(st.session_state.code, st.session_state.pwt,
                                                                    st.session_state.plant, st.session_state.case)
                set_state(list_file, folder_output, name_zip)
                set_data("running", 0)
            if st.form_submit_button("Update File Cadics", use_container_width=True) and get_data("running") == 0:
                notice=update_file_after_edit(st.session_state.code, st.session_state.pwt, st.session_state.plant,
                                       st.session_state.case, files, csrf_token)
                st.write(notice)

    with col_right:
        # BANNER RIGHT
        col_r1, col_r2 = st.columns([2, 1])
        with col_r1:
            st.markdown('<h1 style="text-align: center;">プロ管集約業務システム</h1>', unsafe_allow_html=True)
        with col_r2:
            st.markdown(f'<p style="text-align: center;">{st.session_state.position}</p>', unsafe_allow_html=True)
            # st.markdown(f'<p style="text-align: center;">{"st.session_state.type"}.</p>', unsafe_allow_html=True)
        view("admin")


def set_state(list_file, folder_output, name_zip):
    set_data("folder_output", folder_output)
    set_data("name_zip", name_zip)
    list_link = ["CADICS", "Car配車要望表", "WTC仕様用途一覧表", "WTC要望集約兼チェックリスト", "実験部品", "特性管理部品リスト",
                 "File Log"]
    for index in range(len(list_link)):
        set_data(list_link[index], list_file[index])
    set_data("flag_view", 1)
