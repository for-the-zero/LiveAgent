
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
	page.window.width = 300
	page.window.height = 300
	page.scroll = 'AUTO'
	page.fonts = {"Google Sans": "./assets/Product Sans Regular.ttf"}
	page.theme = ft.Theme(font_family="Google Sans")
	#TODO:
	page.update()

	client = genai.Client(api_key=config_from_file['key'],http_options={"api_version": "v1alpha"})
	config = types.LiveConnectConfig(
		response_modalities=[types.Modality.TEXT if config_from_file['modalities'] == "TEXT" else types.Modality.AUDIO],
		realtime_input_config=types.RealtimeInputConfig(
			automatic_activity_detection={
				"disabled": False,
				"start_of_speech_sensitivity": types.StartSensitivity.START_SENSITIVITY_HIGH,
				"end_of_speech_sensitivity": types.EndSensitivity.END_SENSITIVITY_LOW,
				"prefix_padding_ms": 100,
				"silence_duration_ms": 500
			},
			activity_handling=types.ActivityHandling.START_OF_ACTIVITY_INTERRUPTS
		),
		speech_config={
			"voice_config": {
				"prebuilt_voice_config": {
					"voice_name": config_from_file['voice']
				}
			}
		},
		media_resolution=types.MediaResolution(['MEDIA_RESOLUTION_LOW', 'MEDIA_RESOLUTION_MEDIUM', 'MEDIA_RESOLUTION_HIGH'][config_from_file['media_resolution_num']]),
		system_instruction=sys_prompt
	)
	async with client.aio.live.connect(model=config_from_file['model'], config=config) as session:
		print("[LOG] Connected to Live API")

		# await session.send_client_content(
		# 	turns={"role": "user", "parts": [{"text": 'hello'}]}, turn_complete=True
		# )

		# TODO: send audio

		audio_chunks = []
		async for response in session.receive():
			if response.data:
				audio_chunks.append(response.data)
				print("[LOG] Received audio data")
			if response.server_content and response.server_content.model_turn and response.server_content.model_turn.parts:
				thought = response.server_content.model_turn.parts[0].text
				if thought:
					print(thought)
			if response.text is not None:
				print(response.text)
			if response.server_content and response.server_content.turn_complete:
				break
		full_audio_bytes = b''.join(audio_chunks)
		audio_data = np.frombuffer(full_audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
		print("[LOG] Playing audio...")
		sd.play(audio_data, samplerate=24000)
		sd.wait()
		print("[LOG] Done playing audio")
	print("[LOG] Disconnected from Live API")


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

