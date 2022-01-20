import os
import time
import requests
from IPython.display import HTML
import pyjs9

import logging

webdir = "/home/jovyan/js9-web/"

displayed_js9_ids = []

class JS9(pyjs9.JS9):    
    @staticmethod
    def show_js9(id):
        return JS9.create_js9(id)

    @staticmethod
    def create_js9(id):
        logging.warning('deprecated: please instead create an instance of JS9, and run .display method')
        return 
    
    _displayed = False

    def display(self):
        if self._displayed:
            raise RuntimeError('this has been already displayed once! You probably do not want to do it twice. Better re-create the JS9 object.')
        self._displayed = True
        displayed_js9_ids.append(self.js9_id)
        return HTML(f"""
<iframe class="js9frame_{self.base_id}" id="js9frame" src='/js9html/index_{self.base_id}.html' width="100%" height="700px" frameBorder="0" scrolling="no"></iframe>
""" + """

<script> 
    //var elms = document.querySelectorAll("[id='js9frame']");"""
    f"var elms = Array.from(document.getElementsByClassName('js9frame_{self.base_id}'));"
    """
    console.log(elms);
    elms.forEach(
        function (frame) {                            
            if ( document.URL.includes('renkulab') ) {
                console.log(`detected document.URL ${document.URL}`)
                detected_session_id = document.URL.split('/lab/')[0].split('/').pop();                
                console.log(detected_session_id);
                
                saved_src_url = new URL(frame.src);

                frame.src = 'https://renkulab.io/sessions/' + detected_session_id + saved_src_url.pathname;
                console.log(frame);
            } else {
                console.log('no renku - no need to detect long URL');
            }
        });
</script>
        """)
        
    def __init__(self, id):        
        self.logger = logging.getLogger(str(self.__class__.__name__))

        if id in displayed_js9_ids:
            self.logger.warning('JS9 with this ID was already displayed! Beware if you display another one, you will control both with this object')

        time.sleep(0.3)

        self.base_id = id
        self.js9_id = self.base_id + 'JS9'

        

    def connect(self, *args, **kwargs):
        """
        connects to helper
        """

        if not self._displayed:
            self.logger.warning('Possibly, the object has not been displayed?')

        super().__init__(id=self.js9_id)


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
        if not hasattr(self, 'id'):
            self.logger.info('first command to send: will try to connect first')
            self.connect()

        sleep = float(kwargs.pop('sleep', 0.4))

        R = super().send(*args, **kwargs)

        self.logger.info('send with args: %s kwargs: %s returns: "%s"', repr(args), repr(kwargs), repr(R))

        time.sleep(sleep) # needs it for some other commands        
        return R

    def SaveRegionFile(self, fn="js9.reg"):
        with open(fn, 'w') as f:
            f.write(self.GetRegions("all", {'format': 'text'}))
