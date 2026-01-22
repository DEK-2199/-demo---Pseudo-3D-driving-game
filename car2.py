import pygame
import math

# TO DO:
# ADD VEHICLE SPRITES
# ADD MORE TRACK DECORATION
# TUNNELS
# BRIDGES
# MORE TRACK VARIETY
# TUNE VEHICLE HANDLING


pygame.init()
screen = pygame.display.set_mode((496 * 2, 384 * 2), pygame.RESIZABLE| pygame.SCALED)
game_canvas = pygame.Surface((496, 384))
size = pygame.display.get_surface().get_size()
WIDTH = game_canvas.get_width()
HEIGHT = game_canvas.get_height()
halfH = HEIGHT/2
halfW = WIDTH/2
clock = pygame.time.Clock()

# font1 = pygame.font.Font(" ", 24)   #ADD YOUR OWN FONT HERE (UN-COMMENT SECTION IN GAME LOOP, AROUND LINE 445)

# pygame.mixer.music.load(' ')     #ADD YOUR OWN MUSIC HERE
# pygame.mixer.music.set_volume(0.5)
# pygame.mixer.music.play(loops=-1,start=0.0,)

SKY_BLUE = pygame.Color("#3078FF") 
FOG_COLOR_HORIZON = pygame.Color("#81C3E9")

FOG_COLOUR_ROAD = pygame.Color("#999790")
FOG_COLOUR_GROUND = pygame.Color("#F1DAA1")

GNDCOL_BASE = pygame.Color("#CE9558") 
GNDCOL_ALT  = pygame.Color("#D3A252")

RDCOL_BASE = pygame.Color("#807E75")
RDCOL_ALT = pygame.Color("#8B8981")

scol_base = pygame.Color("#FF0040") 
scol_alt  = pygame.Color("#C5C5C5") 

LINE_COLOUR = pygame.Color("#FFF1E8")

sprite_sheet = pygame.image.load("img/spritesheet.png").convert_alpha()

def get_image(sheet, framewidth,frameheight,width, height, scale):
    image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    image.blit(sheet, (0,0), (framewidth, frameheight, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    

    return image

lamppost_l = get_image(sprite_sheet, 0, 0, 100, 190, 1)
turn_sign_l = get_image(sprite_sheet, 100, 0, 70, 130, 1)
gantry = get_image(sprite_sheet, 190, 10, 320, 130, 1)

bg_lamppost={
        'img': lamppost_l,
        'x': 4,
        'y': 0,
        's': 0.025,
        'spc': 12,
        'flpr': True
}

bg_turnsign={
        'img': turn_sign_l,
        'x': 3,
        'y': 0,
        's': 0.02,
        'spc': 6,
        'flpr': True
}

bg_gantry = {
        'img': gantry,
        'x': 0,
        'y': 0,
        's': 0.03,
        'spc': 6,
}



Track = [  # ct  tu  (segments, turn sharpness)
    {"ct": 90, "tu": 0,      "pi": 0,   "bg1": bg_lamppost, "bg2": 0,           "bg3":0},

    {"ct": 20, "tu": 0,      "pi": -0.25,    "bg1": bg_lamppost, "bg2": bg_turnsign, "bg3":0},
    {"ct": 20,  "tu": -0.025,"pi": -0.25,   "bg1": bg_lamppost, "bg2": bg_turnsign, "bg3":0},

    {"ct": 70,  "tu": -0.025,"pi": 0,   "bg1": 0, "bg2": 0,           "bg3":bg_gantry},
    {"ct": 50,  "tu": 0,     "pi": 0,   "bg1": 0, "bg2": 0,           "bg3":bg_gantry},

    {"ct": 20,  "tu": 0,     "pi": 0.55,   "bg1": 0, "bg2": bg_turnsign, "bg3":bg_gantry},
    {"ct": 20,  "tu": 0.025, "pi": 0.25,   "bg1": 0, "bg2": bg_turnsign, "bg3":bg_gantry},

    
    {"ct": 50,  "tu": 0.025, "pi": -0.5,   "bg1": 0, "bg2": 0,           "bg3":bg_gantry},
    {"ct": 10,  "tu": -0.02, "pi": -0.25,   "bg1": 0, "bg2": 0,           "bg3":bg_gantry},

    {"ct": 20,  "tu": -0.02, "pi": 0,   "bg1": bg_lamppost, "bg2": bg_turnsign, "bg3":0},
    {"ct": 20,  "tu": 0.025, "pi": 0,   "bg1": bg_lamppost, "bg2": bg_turnsign, "bg3":0},


    {"ct": 70,  "tu": 0.025, "pi": 0,   "bg1": bg_lamppost, "bg2": 0,           "bg3":0},
    {"ct": 30, "tu": 0,      "pi": -0.5,   "bg1":  bg_lamppost,  "bg2": bg_turnsign,"bg3":0},
    {"ct": 60,  "tu": -0.025,"pi": 0,   "bg1": bg_lamppost, "bg2": 0,           "bg3":0},

    {"ct": 20,  "tu": -0.025,"pi": 0,   "bg1": bg_lamppost, "bg2": bg_turnsign, "bg3":0},
    {"ct": 20,  "tu": -0.05, "pi": 0,   "bg1": bg_lamppost, "bg2": bg_turnsign, "bg3":0},


    {"ct": 40,  "tu": -0.05, "pi": 0,   "bg1": bg_lamppost, "bg2": 0,           "bg3":0},
    {"ct": 20, "tu": 0,      "pi": 0,   "bg1": bg_lamppost, "bg2": 0,           "bg3":0},

    {"ct": 20, "tu": 0,      "pi": 0,   "bg1": bg_lamppost, "bg2": bg_turnsign, "bg3":0},
    {"ct": 20,  "tu": 0.04,  "pi": 0,    "bg1": bg_lamppost, "bg2": bg_turnsign, "bg3":0},

    {"ct": 60,  "tu": 0.04,  "pi": 0,    "bg1": bg_lamppost, "bg2": 0,           "bg3":0},
    {"ct": 60, "tu": 0,      "pi": 0,    "bg1": bg_lamppost, "bg2": 0,           "bg3":0},

    {"ct": 50, "tu": 0.025,  "pi": 0,    "bg1": bg_lamppost, "bg2": 0,           "bg3":0},
    {"ct": 20, "tu": 0.025,  "pi": -0.5,    "bg1": bg_lamppost, "bg2": bg_turnsign, "bg3":0},
    {"ct": 20, "tu": 0.05,   "pi": -0.5,    "bg1": bg_lamppost, "bg2": 0,           "bg3":0}
]



class Vec3(pygame.math.Vector3):
    def __init__ (self, x = 0.0, y = 0.0, z = 0.0):
        self.x = x
        self.y = y
        self.z = z

def init_road():
    sum_ct = 0
    for corner in Track:
        corner["sumct"] = sum_ct
        sum_ct += corner["ct"]

    for i in range(len(Track)):
        corner = Track[i]

        pi = corner.get("pi", 0)
        
        next_pi = Track[(i + 1) % len(Track)].get('pi',0)

        corner['dpi'] = (next_pi - pi) / corner['ct']
        corner['pi'] = pi



def projection(x, y, z):
    scale = halfW / (z + 0.00001)
    return x * scale + halfW , y * scale + halfH, scale - 4

def advance(cnr, seg): #advance current road segment
    seg += 1
    if seg > Track[cnr]["ct"]:
        seg = 0
        cnr = (cnr + 1) % len(Track)
    return cnr, seg

def skew(x,y,z,xd,yd):      #skew Z axis from (0,0,1) to (xd, yd, 1)
    return x+z*xd, y+z*yd, z

def drawroad(x1, y1, scale1, x2, y2, scale2, sumct):
    y_top = y1
    y_bottom = y2



    max_road_z = 50
    road_fog_factor = min(z_pos / max_road_z, 1.0) 

    max_ground_z = 50
    ground_fog_factor = min(z_pos / max_ground_z, 1.0) 
    
    #draw ground

    gndcol = GNDCOL_ALT if sumct%2 == 0 else GNDCOL_BASE
    gndcol_fogged = gndcol.lerp(FOG_COLOUR_GROUND, ground_fog_factor)

    pygame.draw.rect(game_canvas, gndcol_fogged, (0, y_top, WIDTH, y_bottom - y_top + 1))


    rdcol = RDCOL_ALT if sumct % 2 == 0 else RDCOL_BASE
    rdcol_fogged = rdcol.lerp(FOG_COLOUR_ROAD, road_fog_factor)

    #draw main road
    w1, w2 = 3.5*scale1, 3.5*scale2
    drawtrapezium(x1, y1, w1, x2, y2, w2, rdcol_fogged)

    # draw shoulders
    
    scol = scol_alt if sumct % 2 == 0 else scol_base
    scol_fogged = scol.lerp(FOG_COLOUR_GROUND, ground_fog_factor)
    sw1, sw2=.2*scale1, 0.2*scale2
    drawtrapezium(x1-w1, y1, sw1, x2-w2, y2, sw2, scol_fogged)
    drawtrapezium(x1+w1, y1, sw1, x2+w2, y2, sw2, scol_fogged)

    # draw center line
    
    linecol = LINE_COLOUR.lerp(FOG_COLOUR_ROAD, road_fog_factor)
    if sumct % 2 == 0: 
        mw1, mw2 = 0.03*scale1, 0.03*scale2
        lw1, lw2 = 0.8*scale1, 0.8*scale2
        cw1, cw2 = 3.3*scale1, 3.3*scale2
        drawtrapezium(x1 - lw1, y1, mw1, x2 - lw2, y2, mw2, linecol)
        drawtrapezium(x1 + lw1, y1, mw1, x2 + lw2, y2, mw2, linecol)
        drawtrapezium(x1 - cw1, y1, mw1, x2 - cw2, y2, mw2, linecol)
        drawtrapezium(x1 + cw1, y1, mw1, x2 + cw2, y2, mw2, linecol)
    else:
        mw1, mw2 = 0.05*scale1, 0.05*scale2
        lw1, lw2 = 3*scale1, 3*scale2
        drawtrapezium(x1 - lw1, y1, mw1, x2 - lw2, y2, mw2, linecol)
        drawtrapezium(x1 + lw1, y1, mw1, x2 + lw2, y2, mw2, linecol)
    
def getsumct(cnr, seg):
    return Track[cnr]["sumct"]+seg-1

def drawtrapezium(x1, y1, w1, x2, y2, w2, colour):
    points = [
        (x1 - w1, y1),
        (x1 + w1, y1),
        (x2 + w2, y2),
        (x2 - w2, y2)
    ]
    pygame.draw.polygon(game_canvas, colour, points, width = 0)

def drawsprite(sp, sumct, sprite, side, px, py, scale, clp):

    if sumct%sprite["spc"] != 0: return

    px+=sprite["x"]*scale*side
    py+=sprite["y"]*scale

    size = sprite["s"]*scale

    flp = (side > 0) and sprite.get("flpr", False)

    sp.append({
        'img': sprite['img'],
        'x': px,
        'y': py,
        's': size,
        'flp': flp,
        'clp': (clp[0],clp[1],clp[2],clp[3])
    })


def draw_sky(surface, top, bottom, horizon):
    sky_h = horizon
    
    for y in range(int(sky_h)):
        factor = (y/sky_h) ** 25

        colour = top.lerp(bottom, factor)
        pygame.draw.line(surface, colour, (0, y), (WIDTH, y))



cursor = Vec3(0,1,1) #3D cursor, how the road is drawn
                    # (x = horizontal, y = height, z = depth into screen)
                    # (0 - centered, 1 - slightly below camera, 1 - slightly in front)


direction = Vec3(0,0,1) 
distance = 0
speed = 0
curvature = 0
trackCurvature = 0
playerCurvature = 0
trackDistance = 0
for t in Track:
    trackDistance += t["ct"]

camcnr, camseg = 0, 0 # camera

camera = Vec3(0,0,0)

cam_x = camera.x
cam_y = camera.y
cam_z = camera.z

cnr, seg = camcnr, camseg #cursor's position



steps = 50

init_road()

running = True
while running:
    delta_time = min(clock.tick(60) / 1000, 0.1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[ord('w')]:
        speed += 1 * (delta_time)
    elif keys[pygame.K_DOWN] or keys[ord('s')]:
        speed -= 2 * (delta_time)
    else:
        speed -= 0.75 * (delta_time)

    if keys[pygame.K_LEFT] or keys[ord('a')]:
        playerCurvature -= 7 * delta_time
        

    if keys[pygame.K_RIGHT] or keys[ord('d')]:
        playerCurvature += 7 * delta_time
    
    if distance >= trackDistance:
        distance -= trackDistance
    
    if speed < 0: speed = 0
    if speed > 1: speed = 1

    cam_z += speed

    if cam_z < 0: cam_z = 0
    if cam_z > 70 * delta_time: cam_z = 70 * delta_time

    while cam_z > 1:
        cam_z -= 1 
        camcnr, camseg = advance(camcnr, camseg)

 



    #road position
    cnr, seg = camcnr, camseg

    targetCurvature = Track[cnr]["tu"] * 3
    trackCurveDiff = (targetCurvature - curvature) * speed
    curvature += trackCurveDiff

    trackCurvature += curvature * speed

    #camera "look at"
    cam_angle = cam_z * Track[camcnr]["tu"] #find camera angle from camera's z-depth and corner
    x_dir = -cam_angle
    y_dir = Track[camcnr]["pi"] + Track[camcnr]["dpi"]*(camseg-1)
    z_dir = 1

    #skew camera
    cx, cy, cz = skew(cam_x, cam_y, cam_z, x_dir, y_dir)
    

    #cursor (relative twwwwwwwwwwwwwwwwo skewed camera)
    x_pos = -cx -((playerCurvature - trackCurvature))
    y_pos = float(-cy+1.5)
    z_pos = -cz+1.5

    

    distance += (100 * speed) * delta_time
    
    #previous projected position
    ppx, ppy, pscale = projection(x_pos,y_pos,z_pos)

    #array of sprites to draw
    sp = []

    clp=[0,0, WIDTH, HEIGHT]

    

    
    #draw forward view
    for i in range(steps):

        #move draw call forward
        x_pos += x_dir
        y_pos += y_dir
        z_pos += 1

        #calculate projection
        px, py, scale = projection(x_pos,y_pos,z_pos)
        draw_sky(game_canvas, SKY_BLUE, FOG_COLOR_HORIZON, py)
        #draw road
        if z_pos > 0 and pscale > 0:
            sumct = getsumct(cnr, seg)
            drawroad(px, py, scale, ppx, ppy, pscale, sumct)

            bg1 = Track[cnr]["bg1"]
            if bg1 != 0:
                drawsprite(sp, sumct, bg1, 1, px, py, scale, clp)
                drawsprite(sp, sumct, bg1, -1, px, py, scale, clp)

            bg2 = Track[cnr]["bg2"]
            if bg2 != 0:

                if bg2 == bg_turnsign:
                    side = 1 if Track[cnr+1]["tu"]  < 0 else -1
                    drawsprite(sp, sumct, bg2, side, px, py, scale, clp)
                    drawsprite(sp, sumct, bg2, side, px, py, scale, clp)

            bg3 = Track[cnr]["bg3"]
            if bg3 != 0:
                drawsprite(sp, sumct, bg3, 0, px, py, scale, clp)

        clp[3] = min(clp[3], math.ceil(py))
        rect = (clp[0], clp[1], clp[2]-clp[0], clp[3]-clp[1])
        game_canvas.set_clip(rect)

        
        # turn 
        #          "tu"=-1 means lines will curve maximum left, 
        #          "tu"=0 doesnt change x_dir therefore no turn
        #          "tu"=1 means lines will curve maximum right
        x_dir += Track[cnr]["tu"]
        y_dir += Track[cnr]["dpi"]  

        # advance along road
        cnr, seg = advance(cnr, seg)

        ppx, ppy, pscale = px, py, scale
    
    for i in reversed(sp):
        img = i['img']
        game_canvas.set_clip(i["clp"])

        sw = img.get_width() * i['s']
        sh = img.get_height() * i['s']

        if i['flp']:
            img = pygame.transform.flip(img, True, False)

        if sw > 0 and sh > 0:
            img = pygame.transform.scale(img, (int(sw), int(sh)))

            x = i['x'] - sw / 2
            y = i['y'] - sh
            game_canvas.blit(img, (x, y))
    game_canvas.set_clip(None)
    # text = font1.render(str(int(clock.get_fps())), True, (80,80,70))
    # text2 = font1.render(f"{str(int(speed*280))}km/h", True, ("#970D52"))
    # textpos = text2.get_width()
    screen.blit(pygame.transform.scale(game_canvas, size), (0, 0))
    # screen.blit(text,(12,10))
    # screen.blit(text2,(10,screen.get_height()-40))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()


