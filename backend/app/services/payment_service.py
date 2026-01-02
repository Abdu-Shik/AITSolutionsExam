from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.payment import Payment, PaymentStatus, PaymentMethod
from app.models.booking import Booking, BookingStatus
from app.models.ticket import Ticket


def process_payment(
    db: Session,
    booking_id: int,
    transaction_id: str
) -> Payment:
    # Check for idempotency
    existing_payment = db.query(Payment).filter(
        Payment.transaction_id == transaction_id
    ).first()
    if existing_payment:
        return existing_payment
    
    # Get booking
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    if booking.status == BookingStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot process payment for cancelled booking"
        )
    
    # Check if payment already exists
    existing = db.query(Payment).filter(Payment.booking_id == booking_id).first()
    if existing:
        if existing.status == PaymentStatus.PAID:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment already processed"
            )
        # Update existing payment
        existing.status = PaymentStatus.PAID
        existing.transaction_id = transaction_id
        db.commit()
        db.refresh(existing)
        return existing
    
    # Calculate amount (mock: $100 per ticket)
    ticket_count = db.query(Ticket).filter(Ticket.booking_id == booking_id).count()
    amount = ticket_count * 100.0
    
    # Create payment (mock: always succeeds)
    payment = Payment(
        booking_id=booking_id,
        amount=amount,
        payment_method=PaymentMethod.CARD,
        status=PaymentStatus.PAID,
        transaction_id=transaction_id
    )
    db.add(payment)
    
    # Update booking status
    booking.status = BookingStatus.CONFIRMED
    
    db.commit()
    db.refresh(payment)
    return payment

