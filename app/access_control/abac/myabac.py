from os import path

from app.access_control.abac.runtime import PIP, PDP, RequestCtx, Decision
from app.config import GENERATED_DIR
from .bindings import *

from app.access_control import IAccessController


class ABAC(IAccessController):
    def __init__(self, pip_data):
        # Initialize PDP
        policy_file = path.join(GENERATED_DIR, "policy.lua")
        with open(policy_file) as f:
            self.PDP = PDP(f.read())
        # Create object factory
        self.factory = MyFactory()
        # Read JSON schema
        scheme_file = path.join(GENERATED_DIR, "schema.json")
        with open(scheme_file) as f:
            scheme = f.read()
        # Initialize PIP
        self.PIP = PIP.from_json(scheme, pip_data, self.factory)

    # Check whether the request is allowed in the current access
    # policy.
    def is_allowed(self, request, username):
        # Build request context
        ctx = RequestCtx(
            subject=Subject(name=username, request=request),
            entities=[
                UrlEntity(path=request.path)
            ],
            action=request.method.upper(),
        )
        # Resolve static entities attributes
        to_eval = self.PIP.create_ctx(ctx)
        # Get the decision from PDP
        response = self.PDP.evaluate(to_eval)
        print(to_eval[0].action)
        # Allow access only for decision permit
        return response == Decision.Permit

