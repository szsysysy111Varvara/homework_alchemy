from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base


engine = create_engine('sqlite:///:memory:', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Numeric(10,2))
    in_stock = Column(Boolean)
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship("Category", back_populates="products")

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(255))

    products = relationship("Product", back_populates="category")


Base.metadata.create_all(engine)

category_1 = Category(name='Kosmetics', description='Skin care')
category_2 = Category(name='Clothes', description='Jeans')
product_1 = Product(name='Moisturizing mask', price=10.96, in_stock=True, category=category_1)
product_2 = Product(name='White jeans', price=20.13, in_stock=True, category=category_2)

session.add(category_1)
session.add(product_1)
session.add(category_2)
session.add(product_2)

session.commit()

category_products = session.query(Product).filter_by(category_id=category_1.id).all()

session.close()