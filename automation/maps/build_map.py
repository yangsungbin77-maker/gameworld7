# 바탕 지도(점 없음) + 점 좌표(dots.json)를 따로 만든다. 점은 글 안의 SVG가 그려서 종류별로 켜고 끈다.
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
d.text((W-560,H-50),'위치 자료: MapGenie · gameworld7.com',font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',26),fill=(230,230,230))
img.save('../../public/images/crimson-desert-sea-map-base.webp','WEBP',quality=80)
dots=[[k,round(px(lng,lat)[0]-ox),round(px(lng,lat)[1]-oy)] for k,lng,lat in pts]
json.dump({'w':W,'h':H,'dots':dots},open('dots.json','w'))
print(W,H,len(dots),os.path.getsize('../../public/images/crimson-desert-sea-map-base.webp')//1024,'KB')
