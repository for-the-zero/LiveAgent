import flet as ft

import asyncio
import google.generativeai as genai

def ui(page: ft.Page):
	page.title = "LiveAgent"
	page.window.width = 400
	page.window.height = 500
	page.scroll = 'AUTO'
	page.fonts = {"Google Sans": "./assets/Product Sans Regular.ttf"}
	page.theme = ft.Theme(font_family="Google Sans")
	...
	#TODO:



def live(config_from_ui):
	ft.app(ui)
	genai.configure(api_key=config_from_ui['key'])
	client = genai.Client()
	...
	#TODO: