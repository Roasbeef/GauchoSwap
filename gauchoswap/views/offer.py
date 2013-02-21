from flask import Blueprint

mod = Blueprint('offer', __name__, url_prefix='/offer')

def get_all_offers():
	
