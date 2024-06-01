#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pip install flask

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import RPi.GPIO as GPIO
import time
import os

app = Flask(__name__)

# Configuração dos pinos GPIO
GPIO.setmode(GPIO.BCM)
pins = {
    'up': 17,
    'down': 18,
    'left': 27,
    'right': 22,
    'power': 23,
    'pause': 24,
    'stop': 25
}

for pin in pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

current_directory = os.getcwd()
current_file = None

@app.route('/')
def index():
    return render_template('index.html', current_file=current_file)

@app.route('/action', methods=['POST'])
def action():
    direction = request.form['direction']
    if direction in pins:
        GPIO.output(pins[direction], GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(pins[direction], GPIO.LOW)
    return ('', 204)

@app.route('/file_browser')
def file_browser():
    files = os.listdir(current_directory)
    return render_template('file_browser.html', files=files, current_directory=current_directory)

@app.route('/change_directory', methods=['POST'])
def change_directory():
    global current_directory
    new_directory = request.form['directory']
    if os.path.isdir(new_directory):
        current_directory = new_directory
    return redirect(url_for('file_browser'))

@app.route('/select_file', methods=['POST'])
def select_file():
    global current_file
    file_name = request.form['file']
    if os.path.isfile(os.path.join(current_directory, file_name)):
        current_file = file_name
    return redirect(url_for('file_browser'))

@app.route('/download')
def download():
    if current_file:
        return send_from_directory(current_directory, current_file, as_attachment=True)
    return redirect(url_for('file_browser'))

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5001, debug=True)
    finally:
        GPIO.cleanup()
