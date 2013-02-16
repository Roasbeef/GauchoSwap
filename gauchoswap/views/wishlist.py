from flask import (redirect, url_for, session, request, Blueprint, render_template,
                   flash, g)

mod = Blueprint('wishlist', __name__, url_prefix='/wishlist')

@mod.route('/')
def get_wishlist():
    return render_template('base.html')
