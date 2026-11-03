import json, math, os, time, urllib.request
from PIL import Image, ImageDraw, ImageFont
Z=13; T=256
def px(lng,lat):
    n=2**Z*T; x=(lng+180)/360*n
    s=math.sin(math.radians(lat)); y=(0.5-math.log((1+s)/(1-s))/(4*math.pi))*n
    return x,y
pts=json.load(open('pts.json'))
xs=[px(p[1],p[2])[0] for p in pts]; ys=[px(p[1],p[2])[1] for p in pts]
pad=260
x0,x1=min(xs)-pad,max(xs)+pad; y0,y1=min(ys)-pad,max(ys)+pad
tx0,tx1=int(x0//T),int(x1//T); ty0,ty1=int(y0//T),int(y1//T)
W=(tx1-tx0+1)*T; H=(ty1-ty0+1)*T
img=Image.new('RGB',(W,H),(62,96,112))
for ty in range(ty0,ty1+1):
    for tx in range(tx0,tx1+1):
        f=f'tiles/{Z}_{ty}_{tx}.jpg'
        if not os.path.exists(f):
            url=f'https://tiles.mapgenie.io/games/crimson-desert/pywel/dlc-v3/{Z}/{ty}/{tx}.jpg'
            req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0','Referer':'https://mapgenie.io/'})
            try:
                open(f,'wb').write(urllib.request.urlopen(req,timeout=20).read()); time.sleep(0.15)
            except Exception as e:
                print('miss',tx,ty,e); continue
        try: img.paste(Image.open(f).convert('RGB'),((tx-tx0)*T,(ty-ty0)*T))
        except Exception as e: print('bad',f,e)
ox,oy=tx0*T,ty0*T
d=ImageDraw.Draw(img)
r=11
for k,lng,lat in pts:
    x,y=px(lng,lat); x-=ox; y-=oy
    fill,ring=((255,255,255),(233,30,140)) if k=='p' else ((255,179,0),(122,61,0))
    d.ellipse((x-r-3,y-r-3,x+r+3,y+r+3),fill=(0,0,0))
    d.ellipse((x-r,y-r,x+r,y+r),fill=ring); d.ellipse((x-r+5,y-r+5,x+r-5,y+r-5),fill=fill)
F=ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',44); f2=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',26)
d.rounded_rectangle((30,30,760,250),20,fill=(17,17,17))
d.text((60,45),'붉은사막 진주·해양 광석 지도',font=F,fill='white')
for i,(t,fl,rg) in enumerate([('천연 진주 53곳',(255,255,255),(233,30,140)),('열수 광맥(해양 광석) 160곳',(255,179,0),(122,61,0))]):
    y=125+i*52; d.ellipse((62,y,96,y+34),fill=rg); d.ellipse((69,y+7,89,y+27),fill=fl); d.text((112,y-6),t,font=ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',34),fill='white')
d.text((W-560,H-50),'위치 자료: MapGenie · gameworld7.com',font=f2,fill=(230,230,230))
img.save('../../public/images/crimson-desert-pearl-sea-ore-map-large.webp','WEBP',quality=80)
print(W,H, os.path.getsize('../../public/images/crimson-desert-pearl-sea-ore-map-large.webp')//1024,'KB')
