from flask import Blueprint,request,render_template

blu = Blueprint('layout',__name__,url_prefix='/layout')

@blu.route('')
def layout():
    pass