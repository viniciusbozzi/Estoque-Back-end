from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.settings.database import get_session
from app.schemas.product import ProductRequest
from app.models.product import Product

router = APIRouter(prefix="/product", tags=["Product"])

def get_product_by_name(name: str, session: Session):
	query = select(Product).where(Product.name == name)
	return session.scalars(query).first()

def product_exists(name: str, session: Session) -> bool:
	return get_product_by_name(name, session) is not None

@router.get("/read")
async def read_all_products(session: Session = Depends(get_session)):
	query = select(Product)
	result = session.scalars(query).all()
	return result

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_product(
	product: ProductRequest,
	session: Session = Depends(get_session),
):
	if product_exists(product.name, session):
		raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Product already registered.")

	product_data = product.model_dump()
	session.add(Product(**product_data))
	session.commit()

	return product_data

@router.get("/read/{name}")
async def read_product(
	name: str,
	session: Session = Depends(get_session),
):
	product = get_product_by_name(name, session)
	if not product:
		raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Product not found")
	return product

@router.put("/update/{name}")
async def update_product(
	name: str,
	product: ProductRequest,
	session: Session = Depends(get_session),
):
	if not product_exists(name, session):
		raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Product not found")

	product_data = product.model_dump(exclude_unset=True)
	query = update(Product).where(Product.name == name).values(**product_data)

	session.execute(query)
	session.commit()

	return product_data

@router.delete("/delete/{name}")
async def delete_product(
	name: str,
	session: Session = Depends(get_session),
):
	product = get_product_by_name(name, session)
	if not product:
		raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Product not found")

	session.delete(product)
	session.commit()

	return {"message": "Product removed from database"}