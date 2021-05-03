from kivy.properties import StringProperty, ColorProperty
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
				text: "Switch1"
				pos_hint:{'center_x':0.5,'center_y':0.5}
				on_release:app.switch('screen 2')
		MDScreen:
			name:"screen 2"
			Image:
				source:'wood.jpg'
			MDRaisedButton:
				text: "Switch2"
				pos_hint:{'center_x':0.5,'center_y':0.5}
				on_release:app.switch('screen 1')
'''


class CustomTransition(ShaderTransition):

	# Got this awesome shader from 'laserdog' in shadertoy ---> https://www.shadertoy.com/view/ls3cDB
	fs = """
			$HEADER$

			#define pi 3.14159265359
			#define radius .1

			uniform float t;
			uniform vec2 resolution;
			uniform sampler2D tex_in;
			uniform sampler2D tex_out;

			//IDK why but need to remap it to work, if something doesnt works try remap xD
			float map(float value)
			{
			  float low_map_from = 0., high_map_from = 1., low_map_to = 0.075, high_map_to = -1.15;
			  return low_map_to + (value - low_map_from) * (high_map_to - low_map_to) / (high_map_from - low_map_from);
			}

			void main( void )
			{
			    float aspect = resolution.x / resolution.y ;

			    vec2 uv = gl_FragCoord.xy/resolution.xy;
			    vec2 dir = vec2(0.25,-1.0);
			    vec2 origin = vec2(.25,0.0);
			    
			    float move = map(t);

			    float proj = dot(uv - origin, dir);
			    float dist = proj - move ;
			    
			    vec2 linePoint = uv - dist * dir ;
			    
			    if (dist > radius) 
			    {
			        gl_FragColor = texture2D(tex_in, uv);
			        gl_FragColor.rgb *= pow(clamp(dist - radius, 0., 1.) * 1.5, .2);
			    }
			    else if (dist >= 0.)
			    {
			        float theta = asin(dist / radius);
			        vec2 p2 = linePoint + dir * (pi - theta) * radius;
			        vec2 p1 = linePoint + dir * theta * radius;
			        uv = (p2.x <= aspect && p2.y <= 1. && p2.x > 0. && p2.y > 0.) ? p2 : p1;
			        gl_FragColor = texture2D(tex_out, uv);
			        gl_FragColor.rgb *= pow(clamp((radius - dist) / radius, 0., 1.), .2);
			    }
			    else 
			    {
			        vec2 p = linePoint + dir * (abs(dist) + pi * radius) ;
			        uv = (p.x <= aspect && p.y <= 1. && p.x > 0. && p.y > 0.) ? p : uv;
			        gl_FragColor = texture2D(tex_out, uv);
			    }
			}
		"""

	fs = StringProperty(fs)
	clearcolor = ColorProperty([0, 0, 0, 0])

	def add_screen(self, screen):
		super().add_screen(screen)
		self.render_ctx["resolution"] = list(map(float, screen.size))


class PageCurlApp(MDApp):

	def switch(self,screen):
		self.kv.ids.screens.transition = CustomTransition(duration=1)
		self.kv.ids.screens.current = screen

	def build(self):
		
		self.kv = Builder.load_string(kv)

		return self.kv

PageCurlApp().run()
