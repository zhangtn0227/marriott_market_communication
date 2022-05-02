from app import app
from flask import Flask, render_template, request,send_file,send_from_directory,url_for,jsonify
import pandas as pd
import xlrd
import olefile
import xlwings as xw
import numpy as np
from datetime import timedelta

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['JSON_AS_ASCII'] = False
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
    app.run(debug=True)