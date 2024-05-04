from flask import Flask, render_template
import json
import os
from collections import Counter, defaultdict
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)

from src.main import main as generate_plots

@app.route('/')
def display_charts():
    