#!/user/bin/env python
# encoding: utf-8
#@time      : 2019/11/4 10:47

__author__ = 'Ethan'

import streamlit as st
st.write('Hello, world!')
x = st.slider('x')
st.write(x, 'squard is', x * x)