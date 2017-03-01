from app import db

from flask import Blueprint, g

from flask_restful import Api, Resource 
from flask.ext.restful import abort, fields, marshal_with, reqparse
from flask_inputs import Inputs
from wtforms.validators import DataRequired

from app.base.decorators import login_required, has_permissions

from pygrepurl import Searcher

import itertools
import re
#from app.urlsearch.models import BlogPost as Post

urlsearch_bp = Blueprint('urlsearch_api', __name__)

searcher = Searcher()
api = Api(urlsearch_bp)


class UrlRegexSearch(Resource):

    def valid_regex(self, candidate):
        if len(candidate) < 3:
            return False, "regex too short"
        if len(candidate) > 100:
            return False, "regex too long"
        try:
            re.compile(candidate)
        except re.error:
            return False, "invalid regex"
        return True, ""            
        
    def get(self, regex):
        isvalid,err = self.valid_regex(regex)
        if not isvalid:
            abort(400, message=err)
        max_matches = 20
        matches = searcher.search(regex)
        first_matches = list(itertools.islice(matches, max_matches))
        return {
            'matches': first_matches,
            }

api.add_resource(UrlRegexSearch, '/<string:regex>')

