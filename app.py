import gradio as gr
import time
from main import Korepetycje
import threading


def scraping():
    while True:

        try:
            Korepetycje().main()
        except Exception as e:
            print("Error occurred:", e)

        time.sleep(18000)
        print("Sleeping for 5Hrs...")


def download():
    return "output.csv"


threading.Thread(target=scraping).start()
iface = gr.Interface(fn=download, inputs=None, outputs="file")
iface.launch()
