from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.settings.database import get_session
from app.schemas.movement import MovementRequest
from app.models.movement import Movement, MovementType
from app.models.product import Product

router = APIRouter(prefix="/stock", tags=["Stock"])

@router.get("/details/{product_id}")
async def movement_details(
	product_id: int,
	session: Session = Depends(get_session),
):
	# Verifica se o produto existe
	product = session.get(Product, product_id)
	if not product:
		raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Product not found.")

	# Calcula entradas e saídas
	entrada = session.scalar(
		select(func.sum(Movement.quantity))
		.where(Movement.product_id == product_id, Movement.type == MovementType.entrada)
	) or 0

	saida = session.scalar(
		select(func.sum(Movement.quantity))
		.where(Movement.product_id == product_id, Movement.type == MovementType.saida)
	) or 0

	estoque = entrada - saida

	movements = session.scalars(
		select(Movement).where(Movement.product_id == product_id)
	).all()

	return {
		"produto": {
			"id": product.id,
			"nome": product.name,
			"descricao": product.description,
			"criado_em": product.created_at,
		},
		"resumo_estoque": {
			"entrada": entrada,
			"saida": saida,
			"saldo_atual": estoque,
		},
		"movimentacoes": [
			{
				"id": m.id,
				"tipo": m.type,
				"quantidade": m.quantity,
				"data": m.created_at,
			}
			for m in movements
		],
	}



