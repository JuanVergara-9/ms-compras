from app.extension import db

class Compras(db.Model):
    id_compra = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=True)
    purchase_direction = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Compras {self.id_compra}>'