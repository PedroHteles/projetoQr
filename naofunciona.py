from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.uix.camera import Camera
from kivy.lang import Builder
import numpy as np
import cv2
from kivy.clock import mainthread
from kivy.utils import platform


# check for type of device


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


frame = np.array([])
org_img = lane_img = img = frame
lines = []
##print(img.shape[1], img.shape[0])
select_img = 50
offset = 0    
roi_y1, roi_y2 = 0, 0



'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
---------------------------------------------------------------------->>>>>>>>>>>>>>>
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def cv2_python(frame):
    global lines, org_img, lane_img, img, select_img, offset, roi_y1, roi_y2   
    frame1 = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE) 
    org_img = frame1   
    #print(org_img.shape[1])    
    roi_y1 = int(org_img.shape[0]/2) - select_img  - offset
    roi_y2 = int(org_img.shape[0]/2) + select_img  - offset              
    org_img = cv2.cvtColor(org_img, cv2.COLOR_BGR2RGB) # converts from BGR to RGB
    img = cv2.cvtColor(org_img, cv2.COLOR_RGB2GRAY) # converts from BGR to RGB
    cv2.GaussianBlur(img, (3, 3), 0)
    roi_vertices = np.array([[[org_img.shape[1],roi_y1], [0,roi_y1], [0,  roi_y2], [org_img.shape[1],  roi_y2]]])
    gray_select_roi = region_of_interest(img, roi_vertices)
    cannyed_image = cv2.Canny(gray_select_roi, 20, 140)
    lines = cv2.HoughLinesP(cannyed_image,
                            rho=6,
                            theta=np.pi / 60,
                            threshold=50,
                            lines=np.array([]),
                            minLineLength=30,
                            maxLineGap=50 )

    if len(lane_img) > 0:

        overlay_img = cv2.addWeighted(org_img, 0.8, lane_img, 1, 0)
        frame_rgb = overlay_img
    else:
        frame_rgb = org_img 
    return frame_rgb



#################################################################################
def region_of_interest(img, vertices):
    #defining a blank mask to start with
    mask = np.zeros_like(img)   
    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255       
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
    if len(lines[0][0]) > 1:
        for line in lines:
            for x1,y1,x2,y2 in line:
                cv2.line(img, (x1, y1), (x2, y2), color, thickness)


def seperate_left_right(lines, img):
    lines_left = []
    lines_right = []
    if lines is not None:
        for line in lines:
            for x1,y1,x2,y2 in line:
                if y1 > y2: #positive slope
                    lines_left.append([x1, y1, x2, y2])
                elif y1 < y2: #negative slope
                    lines_right.append([x1, y1, x2, y2])
                #cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)    
    return lines_left, lines_right

def cal_avg_value(values):
    if not (type(values) == 'NoneType'):
        if len(values) > 0:
            cnt_values = len(values)
        else:
            cnt_values = 1
            values = [1]
        return sum(values) / cnt_values

def extrapolate_lines(lines, upper_border, lower_border):
    #TODO: use ROI polygon for extrapolating lines for further improvement
    # y = m*x+c
    
    #calulate average slope 'slope' and y-axis intersection 'c'
    slopes = []
    c_s = []
    
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            if x1 != x2:
                slope = (y1-y2)/(x1-x2)
                slopes.append(slope)
                c = y1 - slope * x1
                c_s.append(c)
    ##print(slopes)            
    avg_slope = cal_avg_value(slopes)
    avg_c = cal_avg_value(c_s)
    #calulate average intersection at lower_border
    x_lower_border_intersections = []
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            x_lower_border_intersection = (lower_border - avg_c) / avg_slope
            x_lower_border_intersections.append(x_lower_border_intersection)

    x_lane_lower_point = cal_avg_value(x_lower_border_intersections)
    x_lane_lower_point = int(x_lane_lower_point)
    
    #calulate average intersection at upper_border
    x_upper_border_intersections = []
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            x_upper_border_intersection = (upper_border - avg_c) / avg_slope
            x_upper_border_intersections.append(x_upper_border_intersection)
    x_lane_upper_point = int(cal_avg_value(x_upper_border_intersections))
    return [x_lane_lower_point, lower_border, x_lane_upper_point, upper_border]

def extract_single_lane(lines, img, upper_border, lower_border):
    lines_left, lines_right = seperate_left_right(lines, img) 
    lane_left = []
    lane_right = []
    if len(lines_left) > 1:
        lane_left = extrapolate_lines(lines_left, upper_border, lower_border)
    if len(lines_right) > 1:
        lane_right = extrapolate_lines(lines_right, upper_border, lower_border) 
    return lane_left, lane_right

def extrapolated_lanes_image(image, lines, roi_upper_border, roi_lower_border):
    lanes_img = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
    #print(lanes_img.shape)    
    lane_left, lane_right = extract_single_lane(lines, image, roi_upper_border, roi_lower_border)
    draw_lines(lanes_img, [[lane_left]], thickness=10)
    draw_lines(lanes_img, [[lane_right]], thickness=10)
    return lanes_img
############################################################################################
class AndroidCamera(Camera):
  camera_resolution =  (480, 360) #(640, 480) # (960, 720) 
  counter = 0

  def _camera_loaded(self, *largs):
    self.texture = Texture.create(size=self.camera_resolution, colorfmt='rgb') #np.flip(self.camera_resolution)
    #print(self.texture.size)
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
