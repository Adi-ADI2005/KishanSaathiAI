from flask import Blueprint, request, jsonify
from config import schemes_collection
from extensions import csrf
from bson import ObjectId
from bson.errors import InvalidId

scheme_bp = Blueprint("scheme_bp", __name__)

# =========================================
# ADD SCHEME
# =========================================
@csrf.exempt
@scheme_bp.route("/api/schemes/add", methods=["POST"])
def add_scheme():
    try:
        data = request.get_json()

        print("DATA:", data)

        if not data:
            return jsonify({
                "success": False,
                "message": "No data received"
            }), 400

        scheme = {
            "title": data.get("title"),
            "icon": data.get("icon"),
            "link": data.get("link"),
            "description": data.get("description"),
            "eligibility": data.get("eligibility"),
            "benefits": data.get("benefits", []),
            "categories": data.get("categories", []),
            "badge": data.get("badge", "None")
        }

        schemes_collection.insert_one(scheme)

        return jsonify({
            "success": True,
            "message": "Scheme added successfully"
        })

    except Exception as e:
        print("ERROR:", str(e))

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================
# GET ALL SCHEMES
# =========================================
@scheme_bp.route("/api/schemes", methods=["GET"])
def get_schemes():
    try:
        schemes = []

        for s in schemes_collection.find():

            schemes.append({
                "id": str(s["_id"]),
                "title": s.get("title"),
                "icon": s.get("icon"),
                "link": s.get("link"),
                "description": s.get("description"),
                "eligibility": s.get("eligibility"),
                "benefits": s.get("benefits", []),
                "categories": s.get("categories", []),
                "badge": s.get("badge", "None")
            })

        return jsonify(schemes)

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================
# UPDATE SCHEME
# =========================================
@csrf.exempt
@scheme_bp.route("/api/schemes/update/<id>", methods=["PUT"])
def update_scheme(id):

    try:

        data = request.get_json()

        print("UPDATE DATA:", data)

        updated_data = {
            "title": data.get("title"),
            "icon": data.get("icon"),
            "link": data.get("link"),
            "description": data.get("description"),
            "eligibility": data.get("eligibility"),
            "benefits": data.get("benefits", []),
            "categories": data.get("categories", []),
            "badge": data.get("badge", "None")
        }

        result = schemes_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": updated_data}
        )

        return jsonify({
            "success": True,
            "message": "Scheme updated successfully"
        })

    except Exception as e:

        print("UPDATE ERROR:", str(e))

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
        
# =========================================
# DELETE SCHEME
# =========================================
@csrf.exempt
@scheme_bp.route("/api/schemes/delete/<id>", methods=["DELETE"])
def delete_scheme(id):

    try:

        # Convert safely
        try:
            obj_id = ObjectId(id)

        except InvalidId:

            return jsonify({
                "success": False,
                "message": "Invalid scheme ID"
            }), 400

        # Delete scheme
        result = schemes_collection.delete_one({
            "_id": obj_id
        })

        # If not found
        if result.deleted_count == 0:

            return jsonify({
                "success": False,
                "message": "Scheme not found"
            }), 404

        # Success
        return jsonify({
            "success": True,
            "message": "Scheme deleted successfully"
        })

    except Exception as e:

        print("DELETE ERROR:", str(e))

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500