import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema
from db import items

  
blp = Blueprint("Items", "items", description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):

    @blp.response(200,ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        
        except KeyError:
            abort(404, message = "Item bulunamadı")


    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        
        except KeyError:
            abort(404, message="Item bulunamadı.")


    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def put(self, item_data, item_id):
        # item_data = request.get_json()

        # if "price" not in item_data or "name" not in item_data:
        #     abort(404, message = "Item verisi yanlış.")

        try:
            item = items[item_id]
            item |= item_data
            return item 
        
        except KeyError:
            abort(404, message = "Item bulunamadı")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        # return {"items": list(items.values())}
        return items.values()
    

    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)

    def post(self, item_data):

      
        # # removed this because we do not need it since we are using it to validate the data
        # if ( 
        #     "price" not in item_data 
        #     or "store_id" not in item_data 
        #     or "name" not in item_data):
        #     abort(400, 
        #         message = 'Kötü deneme, inputun "price", "store_id" ya da "name" içerdiğinden emin olun.')    
        
        
        for item in items.values():
            if(item_data["name"] == item["name"] 
            and item_data["store_id"] == item["store_id"]):
                abort(400, 
                message = 'Bu item zaten vardır.')   

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item

        return item


