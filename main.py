import flet as ft
import json

config_from_ui = {
	"key": '',
	"model": "gemini-2.5-flash-native-audio-preview-09-2025",
	"modalities": ["AUDIO"],
	"media_resolution_num": 1,
	"search": False
}

def set_config_from_ui(key, value):
	global config_from_ui
	config_from_ui[key] = value
def set_config_from_ui_checkbox(modality, bool_value):
	global config_from_ui
	if modality in config_from_ui['modalities']:
		if bool_value:
			config_from_ui['modalities'].append(modality)
		else:
			config_from_ui['modalities'].remove(modality)
def save(_):
	with open('config.json', 'w') as f:
		f.write(json.dumps(config_from_ui, indent=4))
		
try:
	with open('config.json', 'r') as f:
		config_from_ui = json.loads(f.read())
except FileNotFoundError:
	print("config.json file not found")
except json.JSONDecodeError:
	print("Invalid config.json file")
except Exception as e:
	print(f"Error loading config.json: {e}")

def start(_):
	#TODO:
	...

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
		ft.Text("responseModalities:"),
		ft.Row(controls=[
			ft.Checkbox(label="AUDIO", value=config_from_ui['modalities'].count('AUDIO') > 0, on_change=lambda e: set_config_from_ui_checkbox('AUDIO',e.control.value)),
			ft.Checkbox(label="TEXT", value=config_from_ui['modalities'].count('TEXT') > 0, on_change=lambda e: set_config_from_ui_checkbox('TEXT',e.control.value)),
		]),
		ft.Text("mediaResolution:"),
		ft.Slider(min=0,max=2,divisions=2,value=config_from_ui['media_resolution_num'],on_change=lambda e: set_config_from_ui('media_resolution_num',int(e.control.value))),
		ft.Switch(label="Grounding with Google Search", value=config_from_ui['search'], on_change=lambda e: set_config_from_ui('search',e.control.value)),
	)
	page.floating_action_button = ft.FloatingActionButton(
		icon=ft.Icons.PLAY_ARROW_OUTLINED, on_click=start
	)
	
	page.update()

ft.app(main)