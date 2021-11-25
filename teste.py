
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.uix.camera import Camera
from kivy.lang import Builder
import numpy as np
import cv2




Builder.load_string(''' 
<MyLayout>
    orientation: 'vertical'
    AndroidCamera:
        id: camera
        index: 0
        resolution: self.camera_resolution
        allow_stretch: True
        play: True
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
''')




def cv2_python(frame):
    frame = np.array([])
    org_img = lane_img = img = frame
    lines = []
    select_img = 50
    offset = 0    
    roi_y1, roi_y2 = 0, 0 
    frame1 = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE) 
    org_img = frame1   
    #print(org_img.shape[1])    
    roi_y1 = int(org_img.shape[0]/2) - select_img  - offset
    roi_y2 = int(org_img.shape[0]/2) + select_img  - offset              
    org_img = cv2.cvtColor(org_img, cv2.COLOR_BGR2RGB) # converts from BGR to RGB
    img = cv2.cvtColor(org_img, cv2.COLOR_RGB2GRAY) # converts from BGR to RGB
    cv2.GaussianBlur(img, (3, 3), 0)


    if len(lane_img) > 0:
        overlay_img = cv2.addWeighted(org_img, 0.8, lane_img, 1, 0)
        frame_rgb = overlay_img
    else:
        frame_rgb = org_img 
    return frame_rgb


class AndroidCamera(Camera):
  camera_resolution =  (480, 360) #(640, 480) # (960, 720) 
  counter = 0

  def _camera_loaded(self, *largs):
    self.texture = Texture.create(size=self.camera_resolution, colorfmt='rgb') 
    self.texture_size = list(self.texture.size)

  def on_tex(self, *l):
    if self._camera._buffer is None:
        return None
    frame = self.frame_from_buf()
    self.frame_to_screen(frame)
    super(AndroidCamera, self).on_tex(*l)

  def frame_from_buf(self):
    w, h = self.resolution
    frame = np.frombuffer(self._camera._buffer.tostring(), 'uint8').reshape((h + h // 2, w)) #w,h
    frame_bgr = cv2.cvtColor(frame, 93)
    rrt = np.rot90(frame_bgr, 1)    
    return rrt 

  def frame_to_screen(self, frame):

    frame_rgb = cv2_python(frame)
    flipped = np.flip(frame_rgb, 0)
    buf = flipped.tostring()
    self.texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')


class MyLayout(BoxLayout):
  pass

class MyApp(App):
  def build(self):
    return MyLayout()

if __name__ == '__main__':
  MyApp().run()

