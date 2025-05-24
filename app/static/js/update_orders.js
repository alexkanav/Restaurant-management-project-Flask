let order_number = 0


const sendData = async () => {
    try {
        const response = await fetch('/admin/update-orders');
        const newOrders = await response.text();
        document.getElementById('order_content').innerHTML = newOrders;
    } catch (error) {
        console.error('Error updating orders:', error);
        document.getElementById('order_content').innerHTML = "<div class='error'> Зв'язок з сервером втрачено</div>";
        order_number = 0;
    }
};

const checkOrders = async () => {
    try {
        const response = await fetch('/admin/checking-new-orders');
        const newOrders = await response.json();

        if (order_number !== newOrders) {
            await sendData();
            order_number = newOrders;
        }
    } catch (error) {
        console.error('Error checking orders:', error);
        document.getElementById('order_content').innerHTML = "<div class='error'> Зв'язок з сервером втрачено</div>";
        order_number = 0;
    }
};

document.getElementById('order_content').addEventListener('click', async (event) => {
    const card = event.target.closest('.order-card');
    if (card) {
        const userConfirmed = confirm('Бажаєте закрити замовлення?');
        if (!userConfirmed) {
            return; // User clicked "No" (Cancel)
        }

        const orderId = card.getAttribute('data-order-id');
        const data = { order_id: orderId };
        try {
            await sendToServer(data, '/admin/closing-order');
            await sendData();
        } catch (error) {
            console.error('Error sending data to server:', error);
        }
    }
});

setInterval(checkOrders, 5000);
