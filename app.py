from flask import Flask, render_template, request
import RPi.GPIO as GPIO

app = Flask(__name__)

# Configuração dos pinos GPIO
GPIO.setmode(GPIO.BCM)
pins = {
    'up': 17,
    'down': 18,
    'left': 27,
    'right': 22,
    'jump': 23
}

for pin in pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/action', methods=['POST'])
def action():
    direction = request.form['direction']
    if direction in pins:
        GPIO.output(pins[direction], GPIO.HIGH)
        # Deixe o pino ativo por um breve momento e depois desligue
        time.sleep(0.1)
        GPIO.output(pins[direction], GPIO.LOW)
    return ('', 204)

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        GPIO.cleanup()
