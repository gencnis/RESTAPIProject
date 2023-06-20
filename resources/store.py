import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
from db import stores


  
blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):

    @blp.response(200, StoreSchema)
    def get(cls, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message = "Dükkan bulunamadı")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Dükkan bulunamadı.")

@blp.route("/store")
class StoreList(MethodView):

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        # return {"stores": list(stores.values())}
        return stores.values()
    

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        # store_data = request.get_json()
        # if "name" not in store_data:
        #     abort(
        #         400,
        #         message = 'Kötü deneme. Inputun "name" içerdiğinden emin olun.'
        #     )
    
        for store in stores.values():
            if(store_data["name"] == store["name"]):
                abort(400, message = 'Bu dükkan zaten vardır.')   

        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        return store

