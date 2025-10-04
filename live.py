import flet as ft
import json
import sys

import asyncio
from google import genai
from google.genai import types

import numpy as np
import sounddevice as sd

async def app(page: ft.Page):
	global config_from_file, sys_prompt
	page.title = "LiveAgent"
	page.window.width = 400
	page.window.height = 300
	page.scroll = 'AUTO'
	page.fonts = {"Google Sans": "./assets/Product Sans Regular.ttf"}
	page.theme = ft.Theme(font_family="Google Sans")

	stop_btn = ft.OutlinedButton(text="Stop", width=page.width)
	
	cb_audio = ft.Checkbox(label="Mic", value=True)
	cb_screen = ft.Checkbox(label="Screen", value=True)
	text_rtn = ft.Text("Text")

	input_text = ft.TextField(label="Send Text")
	input_btn = ft.IconButton(icon=ft.Icons.SEND,icon_size=20)

	page.add(
		ft.Column(controls=[
			ft.Row(controls=[
				input_text, input_btn
			],width=page.width,expand=True),
			ft.Row(controls=[
				ft.Text("Input:"), cb_audio, cb_screen,
			]),
			ft.Card(content=ft.Container(content=text_rtn, margin=15), width=page.width),
			stop_btn
		],expand=True,alignment=ft.MainAxisAlignment.END)
	)

	cb_audio.on_change = lambda e: print(e.control.value)
	cb_screen.on_change  =lambda e: print(e.control.value)
	input_btn.on_click = lambda e: print(input_text.value)

	page.update()

	#client = genai.Client(api_key=config_from_file['key'],http_options={"api_version": "v1alpha"})
	# config = types.LiveConnectConfig(
	# 	response_modalities=[types.Modality.TEXT if config_from_file['modalities'] == "TEXT" else types.Modality.AUDIO],
	# 	realtime_input_config=types.RealtimeInputConfig(
	# 		automatic_activity_detection={
	# 			"disabled": False,
	# 			"start_of_speech_sensitivity": types.StartSensitivity.START_SENSITIVITY_HIGH,
	# 			"end_of_speech_sensitivity": types.EndSensitivity.END_SENSITIVITY_LOW,
	# 			"prefix_padding_ms": 100,
	# 			"silence_duration_ms": 500
	# 		},
	# 		activity_handling=types.ActivityHandling.START_OF_ACTIVITY_INTERRUPTS
	# 	),
	# 	speech_config={
	# 		"voice_config": {
	# 			"prebuilt_voice_config": {
	# 				"voice_name": config_from_file['voice']
	# 			}
	# 		}
	# 	},
	# 	context_window_compression=types.ContextWindowCompressionConfig(
	# 		trigger_tokens=25600,
	# 		sliding_window=types.SlidingWindow(target_tokens=12800),
	# 	),
	# 	media_resolution=types.MediaResolution(['MEDIA_RESOLUTION_LOW', 'MEDIA_RESOLUTION_MEDIUM', 'MEDIA_RESOLUTION_HIGH'][config_from_file['media_resolution_num']]),
	# 	system_instruction=sys_prompt
	# )


try:
	with open('config.json') as f:
		config_from_file = json.load(f)
except FileNotFoundError:
	print("Could not find config.json file")
	sys.exit(1)
except json.JSONDecodeError:
	print("Invalid config.json file")
except Exception as e:
	print(f"Error loading config.json: {e}")
	sys.exit(1)
try:
	with open('utils/prompt.md') as f:
		sys_prompt = f.read()
except FileNotFoundError:
	print("Could not find prompt.md file")
	sys.exit(1)
except Exception as e:
	print(f"Error loading prompt.md: {e}")
	sys.exit(1)
ft.app(app)

