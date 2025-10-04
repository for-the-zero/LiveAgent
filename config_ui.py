import flet as ft
import json
import subprocess

config_from_ui = {
	"key": '',
	"model": "gemini-2.5-flash-native-audio-preview-09-2025",
	"voice": "Zephyr",
	"modalities": "AUDIO",
	"media_resolution_num": 1,
	"search": False
}

def set_config_from_ui(key, value):
	global config_from_ui
	config_from_ui[key] = value
def save(_):
	with open('config.json', 'w') as f:
		f.write(json.dumps(config_from_ui, indent=4))
		
try:
	with open('config.json', 'r') as f:
		config_from_ui = json.loads(f.read())
except FileNotFoundError:
	...
except json.JSONDecodeError:
	print("Invalid config.json file")
except Exception as e:
	print(f"Error loading config.json: {e}")

def start(page: ft.Page):
	print("Starting LiveAgent")
	save(None)
	page.window.close()
	subprocess.Popen(["python", "live.py"])

def main(page: ft.Page):
	page.title = "LiveAgent"
	page.window.width = 400
	page.window.height = 500
	page.scroll = 'AUTO'
	page.fonts = {"Google Sans": "./assets/Product Sans Regular.ttf"}
	page.theme = ft.Theme(font_family="Google Sans")

	page.add(
		ft.Row(controls=[
			ft.Text("Setup", size=30),
			ft.IconButton(icon=ft.Icons.SAVE, icon_color=ft.Colors.ON_PRIMARY_CONTAINER, icon_size=20, on_click=save)
		],alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
		ft.TextField(label="Key", password=True, can_reveal_password=True, value=config_from_ui['key'], on_change=lambda e: set_config_from_ui('key',e.control.value)),
		ft.Dropdown(label="Model",options=[
			ft.DropdownOption("gemini-2.5-flash-native-audio-preview-09-2025"),
			ft.DropdownOption("gemini-2.5-flash-preview-native-audio-dialog"),
			ft.DropdownOption("gemini-live-2.5-flash-preview"),
			ft.DropdownOption("gemini-2.0-flash-live-001"),
		],value=config_from_ui['model'],on_change=lambda e: set_config_from_ui('model',e.control.value)),
		ft.Dropdown(label="Voice",options=[
			ft.DropdownOption("Zephyr"),
			ft.DropdownOption("Kore"),
			ft.DropdownOption("Leda"),
			ft.DropdownOption("Orus"),
			ft.DropdownOption("Callirrhoe"),
			ft.DropdownOption("Despina"),
			ft.DropdownOption("Erinome"),
			ft.DropdownOption("Laomedeia"),
			ft.DropdownOption("Achernar"),
			ft.DropdownOption("Alnilam"),
			ft.DropdownOption("Schedar"),
			ft.DropdownOption("Pulcherrima"),
			ft.DropdownOption("Sadaltager"),
			ft.DropdownOption("Sulafat")
		],value=config_from_ui['voice'],on_change=lambda e: set_config_from_ui('voice',e.control.value)),
		ft.Text("responseModalities:"),
		ft.RadioGroup(content=ft.Row(controls=[
			ft.Radio(label="AUDIO", value="AUDIO"),
			ft.Radio(label="TEXT", value="TEXT")
		]), value=config_from_ui['modalities'], on_change=lambda e: set_config_from_ui('modalities',e.control.value)),
		ft.Text("mediaResolution:"),
		ft.Slider(min=0,max=2,divisions=2,value=config_from_ui['media_resolution_num'],on_change=lambda e: set_config_from_ui('media_resolution_num',int(e.control.value))),
		ft.Switch(label="  Grounding with Google Search", value=config_from_ui['search'], on_change=lambda e: set_config_from_ui('search',e.control.value)),
	)
	page.floating_action_button = ft.FloatingActionButton(
		icon=ft.Icons.PLAY_ARROW_OUTLINED, on_click=lambda _: start(page)
	)
	
	page.update()

ft.app(main)