# -*- coding: utf-8 -*-
import re
import time

global global_var,stop_all#global
global_var=[]
stop_all=0
from  resources.modules.client import get_html
from resources.modules import log
from resources.modules.general import clean_name,check_link,server_data,replaceHTMLCodes,domain_s,similar,all_colors,base_header
from  resources.modules import cache
try:
    from resources.modules.general import Addon
except:
  import Addon
type=['movie','tv','torrent']

import urllib,logging,base64,json
from urllib.parse import unquote
try:
    que=urllib.quote_plus
except:
    que=urllib.parse.quote_plus
def get_links(tv_movie,original_title,season_n,episode_n,season,episode,show_original_year,id):
    global global_var,stop_all

    
    
    all_links=[]
    if tv_movie=='movie':
     tv_movie='movies'
     search_url=[('%s %s'%(clean_name(original_title,1),show_original_year)).replace(' ','+').lower()]
    else:
      if Addon.getSetting('debrid_select')=='0' :
        search_url=[('%s s%se%s'%(clean_name(original_title,1),season_n,episode_n)).replace(' ','+').lower(),('%s s%s'%(clean_name(original_title,1),season_n)).replace(' ','+').lower(),('%s season %s'%(clean_name(original_title,1),season)).replace(' ','+').lower()]
      else:
        search_url=[('%s s%se%s'%(clean_name(original_title,1),season_n,episode_n)).replace(' ','+').lower()]
    
    
            
    for itt in search_url:
      for page in range(0,4):
        
        x=get_html(f'https://filemood.com/result?q={itt}+in%3Atitle&f={page*40}',headers=base_header).content()
    
    
        
        
        regex='<tr>(.+?)</tr>'
        macth_pre=re.compile(regex,re.DOTALL).findall(x)
        
        for items in macth_pre:
            if stop_all==1:
                break
   
            regex='title="(.+?)".+?<p class="text" style="width: 80px;"><b>(.+?)<.+?href="(.+?)"'
            match=re.compile(regex,re.DOTALL).findall(items)
  
            for title,size,link in match:
                     
                     if stop_all==1:
                        break
                
                     if '4k' in title:
                              res='2160'
                     elif '2160' in title:
                          res='2160'
                     elif '1080' in title:
                          res='1080'
                     elif '720' in title:
                          res='720'
                     elif '480' in title:
                          res='480'
                     elif '360' in title:
                          res='360'
                     else:
                          res='HD'
                     links=link.split('-')
                     link=links[len(links)-1].split('.')[0]
                     
                     link='magnet:?xt=urn:btih:%s&dn=%s'%(link,que(title))
                     
                     o_link=link
                
                     try:
                         o_size=size
                         size=float(o_size.replace('GB','').replace('MB','').replace(",",'').strip())
                         if 'MB' in o_size:
                           size=size/1000
                     except:
                        size=0
                     max_size=int(Addon.getSetting("size_limit"))
              
                     if size<max_size:
                  
                       all_links.append((title,o_link,str(size),res))
                   
                       global_var=all_links
    return global_var
        
    