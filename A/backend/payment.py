import qrcode

def generate_payment_qr(upi_id, amount):
    """Generates a payment QR code with the given UPI ID and amount.

    Args:
        upi_id: The UPI ID of the receiver.
        amount: The amount to be paid.

    Returns:
        qrcode.QRCode: A QR code object.
    """

    # Format the UPI payment string (adjust if your UPI provider uses a different format)
    payment_string = f"upi://pay?pa={upi_id}&am={amount}&cu=INR"

    # Create the QR code object
    qr = qrcode.QRCode(
        version=1,  # A small version should be sufficient here
        error_correction=qrcode.constants.ERROR_CORRECT_L, # Use some error correction
        box_size=10, 
        border=4,
    )

    qr.add_data(payment_string)
    qr.make(fit=True)

    return qr

# Example usage
upi_id = "notalanjoseph@okaxis"
amount = 100.0

payment_qr = generate_payment_qr(upi_id, amount)

# Save the QR code as an image
img = payment_qr.make_image(fill_color='black', back_color='white')
img.save("payment_qr.png") 