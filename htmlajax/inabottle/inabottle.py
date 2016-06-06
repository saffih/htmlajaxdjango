
from bottle import redirect

from bottle import Bottle, run, route,get,post, static_file, request
from bottle import template
import itertools
# from collections import ChainMap

app = Bottle()

with app:
    @route('/')
    @route('/htmlajax')
    def main_page():
        return template(open('htmlajax.html', 'r').read(), request.forms)

    @get('/htmlajaxform')
    def get_the_form():
        # context = ChainMap({}, request.forms, dict(isnested=''))
        context = dict(isnested='', msg='')
        context.update(request.forms)

        return template(open('htmlajaxform.html', 'r').read(), context)

    @post('/htmlajaxform')
    def post_the_form():
        if request.forms.get('msg').lower().startswith('hi'):
            if request.forms.get('isnested')=='True':
              return "you did well"
            redirect('htmlajaxsuccess')
        return template(open('htmlajaxform.html', 'r').read(), request.forms)

    @route('/htmlajaxsuccess')
    def return_success():
        return template(open('htmlajaxsuccess.html', 'r').read(), request.forms)

    @route('/static/<filename>')
    def server_static(filename):
        return static_file(filename, root='static/')

    @route('/ping')
    def main_page():
        return 'hello world'


    run(host='localhost', port=8080, debug=True)