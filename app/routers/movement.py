from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.settings.database import get_session
from app.schemas.movement import MovementRequest
from app.models.movement import Movement, MovementType
from app.models.product import Product

router = APIRouter(prefix="/movement", tags=["Movement"])

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_movement(
	movement: MovementRequest,
	session: Session = Depends(get_session),
):
	# Verifica se o produto existe
	product = session.get(Product, movement.product_id)
	if not product:
		raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Product not found.")

	# Calcula o total de entradas e saídas atuais
	total_entrada = session.scalar(
		select(func.sum(Movement.quantity))
		.where(Movement.product_id == movement.product_id, Movement.type == MovementType.entrada)
	) or 0

	total_saida = session.scalar(
		select(func.sum(Movement.quantity))
		.where(Movement.product_id == movement.product_id, Movement.type == MovementType.saida)
	) or 0

	estoque_atual = total_entrada - total_saida

	# Se for uma saída, verifica se há estoque suficiente
	if movement.type == MovementType.saida and movement.quantity > estoque_atual:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=f"Not enough stock. Available: {estoque_atual}, Requested: {movement.quantity}"
		)


	movement_data = movement.model_dump()
	session.add(Movement(**movement_data))
	session.commit()

	return movement_data


@router.get("/all")
async def list_all_movements(session: Session = Depends(get_session)):
	movements = session.scalars(select(Movement)).all()
	return movements

