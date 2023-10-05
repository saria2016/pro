# #!/usr/bin/env python3
# """The blueprint for all CRUD operation for Brand."""
# from models.brand import Brand
# from flask import jsonify, abort, request
# from api.v1.views import app_views
# from models import storage
# from api.v1.views import *

# parent_cls = Brand


# @app_views.route(
#     "/brands",
#     methods=["GET"],
#     strict_slashes=False,
#     defaults={"brand_id": None},
# )
# @app_views.route("/brands/<brand_id>", methods=["GET"], strict_slashes=False)
# def get_brand(brand_id):
#     """Get all brand or get a particular brand by brand id."""
#     if brand_id:
#         return get_match(parent_cls, brand_id)
#     brand = [brands.to_dict() for brands in storage.all(Brand).values()]
#     return jsonify(brand)


# @app_views.route(
#     "/brands/<brand_id>",
#     methods=["DELETE"],
#     strict_slashes=False
# )
# def delete_brand(brand_id):
#     """Delete a brand by id."""
#     return delete_match(parent_cls, brand_id)


# @app_views.route(
#     "/brands",
#     methods=["POST"],
#     strict_slashes=False,
# )
# def create_brand():
#     """Create a brand via a POST request."""
#     if not request.json:
#         abort(400, description="Error: Not a valid JSON")
#     if "brand_name" not in request.json:
#         abort(400, description="Error: Missing name")
#     kwargs = request.get_json()
#     return create_new(parent_cls, None, None, kwargs)


# @app_views.route(
#     "/brands/<brand_id>",
#     methods=["PUT"],
#     strict_slashes=False
# )
# def update_brand(brand_id):
#     """Update a brand by id."""
#     if not request.json:
#         abort(400, description="Error: Not a valid JSON")
#     # validate if the current content exists
#     get_brand_obj = storage.get(parent_cls, brand_id)
#     if not get_brand_obj:
#         abort(404, description="Object instance not found")
#     kwargs = request.get_json()
#     return update_match(get_brand_obj, kwargs)
