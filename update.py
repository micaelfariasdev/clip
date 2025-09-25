from tiktokautouploader import upload_tiktok
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pkg_resources")

file = "parte-04.mp4"
title = ("parte 4 Quando o céu não é o limite… #Superman está de volta! "
         "Quem mais está pronto para voar junto?  #DC #SuperHero "
         "#FilmeDoAno #ActionMovie #HeroIsBack #Cinema2025 #EpicScenes "
         "#ViralClips #MustWatch #SupermanReturns")

print(title)
resp = upload_tiktok(file, description=title, accountname='loovemusic.br', headless=False, schedule='16:20')


