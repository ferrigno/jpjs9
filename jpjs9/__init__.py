import os
import time
import requests
from IPython.display import HTML
import pyjs9

import logging

webdir = "/home/jovyan/js9-web/"

class JS9(pyjs9.JS9):    

    @staticmethod
    def show_js9():
        return HTML("""
<iframe class="js9frame" id="js9frame" src='/js9html' width="100%" height="700px" frameBorder="0" scrolling="no"></iframe>

<script> 
    //var elms = document.querySelectorAll("[id='js9frame']");
    var elms = Array.from(document.getElementsByClassName('js9frame'));
    console.log(elms);
    elms.forEach(
        function (frame) {                            
            if ( document.URL.includes('renkulab') ) {
                console.log(`detected document.URL ${document.URL}`)
                detected_session_id = document.URL.split('/lab/')[0].split('/').pop();                
                console.log(detected_session_id);

                frame.src = 'https://renkulab.io/sessions/' + detected_session_id + '/js9html';
                console.log(frame);
            } else {
                console.log('no renku - no need to detect long URL');
            }
        });
</script>
        """)
        
    def __init__(self, *args, **kwargs):
        time.sleep(0.3)
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(str(self.__class__))

    def open_fits(self, fn):
        return self.Load(fn)

    def Load(self, fn, *args):
        return super().Load(self.fn_in_web(fn), *args)

    def fn_in_web(self, fn):
        logger = self.logger.getChild('fn_in_web')
        
        basename = os.path.basename(fn)
        logger.debug('basename: %s', basename)
        
        web_server_fn = os.path.join(webdir, basename)  # TODO: maybe adapt
        logger.debug('web_server_fn: %s', web_server_fn)

        web_fn = os.path.basename(web_server_fn)
        logger.debug('web_fn: %s', web_fn)

        with open(web_server_fn, "wb") as f:
            if fn.startswith("http"):
                logger.debug('downloading fn: %s', fn)
                c = requests.get(fn).content                
            else:
                logger.debug('opening fn: %s', fn)
                c = open(fn, 'rb').read()

            logger.debug('got content: %s bytes', len(c))
            f.write(c)
            
        return web_fn

    def LoadRegions(self, fn, *args):
        return super().LoadRegions(self.fn_in_web(fn), *args)

    def send(self, *args, **kwargs):
        sleep = float(kwargs.pop('sleep', 0.2))

        R = super().send(*args, **kwargs)

        time.sleep(sleep) # needs it for some other commands        
        return R

    def SaveRegionFile(self, fn="js9.reg"):
        with open(fn, 'w') as f:
            f.write(self.GetRegions("all", {'format': 'text'}))
