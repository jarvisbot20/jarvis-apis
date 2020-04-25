from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from admin_panel_resources import signup, login
from profile_integrations import listIntgerations, createIntegrations
from profile_integrations import updateIntegrations
from installation_instructions import listgitrepos, helpwithinstallation
from installation_instructions import projectreleasestatus
from travis_builds import buildResult
import mongoengine

app = Flask(__name__)
cors = CORS(app)
api = Api(app)
mongoengine.connect('Jarvis')

@app.route("/")
def mainpage():
    return "API Server Running Correctly"

class Signup(Resource):
    def post(self):
        resp = signup(request.get_json())
        return jsonify(resp)


class Login(Resource):
    def post(self):
        resp = login(request.get_json())
        return jsonify(resp)


class Integrations(Resource):
    def get(self):
        resp = listIntgerations(request.headers.get("token"))
        return jsonify(resp)
    def post(self):
        resp = createIntegrations(
            request.headers.get("token"),
            request.get_json()
        )
        return jsonify(resp)
    def put(self):
        resp = updateIntegrations(
            request.headers.get("token"),
            request.get_json()
        )
        return jsonify(resp)

class GithubApi(Resource):
    def get(self):
        resp = listgitrepos(
            request.headers.get("token")
        )
        return jsonify(resp)

class InstallationApi(Resource):
    def get(self):
        if request.headers.get("reqddocker") == "false":
            resp = helpwithinstallation(
                request.headers.get("token"),
                request.headers.get("projectname"),
                False,
                request.headers.get("os")
            )
        else:
            resp = helpwithinstallation(
                request.headers.get("token"),
                request.headers.get("projectname"),
                True
            )
        return jsonify(resp)

class ProjectStatus(Resource):
    def get(self):
        resp = projectreleasestatus(
            request.headers.get("token"),
            request.headers.get("projectname")
        )
        return jsonify(resp)

class TravisBuilds(Resource):
    def get(self):
        resp = buildResult(
            request.headers.get("token"),
            request.headers.get("projectname")
        )
        return jsonify(resp)


api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")
api.add_resource(Integrations, "/integrations")
api.add_resource(GithubApi, "/github")
api.add_resource(InstallationApi, "/installation")
api.add_resource(ProjectStatus, "/status/project")
api.add_resource(TravisBuilds, "/buildresult")


if __name__ == "__main__":
    app.run(port=5000, debug=True)