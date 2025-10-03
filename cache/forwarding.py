
import flet as ft
import json
import sys

import asyncio
from google import genai
from google.genai import types

import numpy as np
import sounddevice as sd

import time

async def mic_stream(chunk=160, sr=16000):
	q = asyncio.Queue()
	def callback(indata, frame_count, time_info, status):
		for i in range(0, frame_count, 160):
			q.put_nowait(indata[i:i+160, 0].astype(np.float32))
	stream = sd.InputStream(
		samplerate=sr,
		channels=1,
		dtype='float32',
		blocksize=chunk,
		latency='low',
		callback=callback
	)
	with stream:
		while True:
			yield await q.get()
async def send_mic(session):
	async for pcm_float32 in mic_stream():
		pcm_bytes = (pcm_float32 * 32767).astype(np.int16).tobytes()
		await session.send_realtime_input(audio={"data": pcm_bytes, "mime_type": "audio/pcm"})
		print('send_mic' + str(time.time_ns()))
async def receive_loop(session):
	audio_chunks = []
	async for response in session.receive():
		if response.data:
			audio_chunks.append(response.data)
			print("[LOG] received audio chunk")
		if response.text:
			print(response.text, end="", flush=True)
		if response.server_content and response.server_content.turn_complete:
			if audio_chunks:
				full_audio_bytes = b''.join(audio_chunks)
				audio_data = np.frombuffer(full_audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
				sd.play(audio_data, samplerate=24000)
				await asyncio.to_thread(sd.wait)
				audio_chunks.clear()
			print("[LOG]—— turn complete ——")

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

		recv_task = asyncio.create_task(receive_loop(session))
		send_task = asyncio.create_task(send_mic(session))
		try:
			await asyncio.gather(recv_task, send_task)
		except asyncio.CancelledError:
			print("[LOG] User cancelled session")

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

