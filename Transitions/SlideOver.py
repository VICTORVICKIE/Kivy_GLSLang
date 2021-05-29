from kivy.properties import StringProperty, ColorProperty, OptionProperty
from kivy.uix.screenmanager import ShaderTransition
from kivy.lang import Builder
from kivymd.app import MDApp

kv = '''
MDNavigationLayout:
	ScreenManager:
		id: screens
		MDScreen:
			name:"screen 1"
			Image:
				source:'bg.jpg'
			MDRaisedButton:
				text: "UP"
				pos_hint:{'center_x':0.5,'center_y':0.5}
				on_release:app.switch('screen 2')
		MDScreen:
			name:"screen 2"
			Image:
				source:'wood.jpg'
			MDRaisedButton:
				text: "DOWN"
				pos_hint:{'center_x':0.5,'center_y':0.5}
				on_release:app.switch('screen 1')
'''

class SingleSlideTransition(ShaderTransition):

	direction = OptionProperty("up", options=["up", "down"])
	
	fs = """
			
$HEADER$

uniform float t;
uniform float direction;

uniform vec2 resolution;
uniform sampler2D tex_in;
uniform sampler2D tex_out;

float progress;

vec4 getToColor(vec2 p){
	if(direction == 2.0){return texture2D(tex_in, p);}
	else{return texture2D(tex_out, p);}
}

vec4 getFromColor(vec2 p){
	if(direction == 2.0){return texture2D(tex_out, p);}
	else{return texture2D(tex_in, p);}
	
}

const vec4 black = vec4(0.0, 0.0, 0.0, 1.0);
const vec2 boundMin = vec2(0.0, 0.0);
const vec2 boundMax = vec2(1.0, 1.0);

bool inBounds (vec2 p) {
	return all(lessThan(boundMin, p)) && all(lessThan(p, boundMax));
}

vec4 transition (vec2 uv) {
	vec2 spfr,spto = vec2(-1.);
	float size = mix(1.0, 3.0, progress*0.2);
	spto = (uv + vec2(-0.5,-0.5))+vec2(0.5,0.5);
	spfr = (uv + vec2(0.0, 1.0 - progress));
	if(inBounds(spfr)){
		return getToColor(spfr);
	} else if(inBounds(spto)){
		return getFromColor(spto);
	}
}

void main( void ) {
	vec2  uv = gl_FragCoord.xy / resolution.xy;
	if(direction == 1.0){progress = 1.0 - t;}
	else{progress = t;}

	gl_FragColor = transition(uv);
}

		"""
	fs = StringProperty(fs)
	clearcolor = ColorProperty([0, 0, 0, 0])

	
	def add_screen(self, screen):
		super().add_screen(screen)
		self.render_ctx["resolution"] = list(map(float, screen.size))

		aspect_ratio = screen.size[0]/screen.size[1]
		
		if aspect_ratio >= 1:
			self.render_ctx["aspect"] = 1.0

		else:
			self.render_ctx["aspect"] = 2.0

		if self.direction == "down":
			self.render_ctx["direction"] = 1.0
		
		else:
			self.render_ctx["direction"] = 2.0
			
class SlideOverApp(MDApp):

	def switch(self,screen):
		if screen == "screen 2":
			self.kv.ids.screens.transition = SingleSlideTransition(duration=2)
		else:
			self.kv.ids.screens.transition = SingleSlideTransition(direction="down", duration=2)
		self.kv.ids.screens.current = screen

	def build(self):
		
		self.kv = Builder.load_string(kv)

		return self.kv

SlideOverApp().run()